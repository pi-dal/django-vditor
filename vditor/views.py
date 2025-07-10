import hashlib
import logging
import os
import time
from pathlib import Path
from collections import defaultdict

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from werkzeug.utils import secure_filename

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

# Performance metrics
_upload_metrics = defaultdict(lambda: {'count': 0, 'total_time': 0, 'total_size': 0})

# Configuration constants
MAX_FILE_SIZE = getattr(
    settings, "VDITOR_MAX_FILE_SIZE", 10 * 1024 * 1024
)  # 10MB default
ALLOWED_EXTENSIONS = getattr(
    settings, "VDITOR_ALLOWED_EXTENSIONS", {".jpg", ".jpeg", ".png", ".gif", ".webp"}
)
ALLOWED_MIME_TYPES = getattr(
    settings,
    "VDITOR_ALLOWED_MIME_TYPES",
    {
        "image/jpeg",
        "image/png",
        "image/gif",
        "image/webp",
    },
)

# Security constants
MAGIC_NUMBERS = {
    b"\xff\xd8\xff": "image/jpeg",
    b"\x89PNG\r\n\x1a\n": "image/png",
    b"GIF87a": "image/gif",
    b"GIF89a": "image/gif",
    b"RIFF": "image/webp",  # WebP files start with RIFF
}

MAX_FILENAME_LENGTH = 255
FORBIDDEN_FILENAME_CHARS = set('<>:"/\\|?*\0')
FORBIDDEN_FILENAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    "COM1",
    "COM2",
    "COM3",
    "COM4",
    "COM5",
    "COM6",
    "COM7",
    "COM8",
    "COM9",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
}


def update_upload_metrics(
    file_size: int, processing_time: float, success: bool = True
) -> None:
    """Update upload performance metrics.
    
    Args:
        file_size: Size of uploaded file in bytes
        processing_time: Time taken to process upload in seconds
        success: Whether upload was successful
    """
    try:
        metric_key = 'successful' if success else 'failed'
        _upload_metrics[metric_key]['count'] += 1
        _upload_metrics[metric_key]['total_time'] += processing_time
        _upload_metrics[metric_key]['total_size'] += file_size
    except Exception as e:
        logger.warning(f"Failed to update upload metrics: {e}")


def get_upload_metrics() -> dict:
    """Get current upload performance metrics.
    
    Returns:
        Dictionary with upload metrics
    """
    metrics = {}
    for key, data in _upload_metrics.items():
        if data['count'] > 0:
            metrics[key] = {
                'count': data['count'],
                'avg_time': data['total_time'] / data['count'],
                'total_size': data['total_size'],
                'avg_size': data['total_size'] / data['count']
            }
    return metrics


def _validate_filename_security(filename: str) -> tuple[bool, str]:
    """Validate filename for security issues.

    Args:
        filename: Original filename to validate

    Returns:
        tuple: (is_valid, error_message)
    """
    if not filename:
        return False, _("File must have a name.")

    if len(filename) > MAX_FILENAME_LENGTH:
        return False, _("Filename is too long.")

    # Check for forbidden characters
    if any(char in FORBIDDEN_FILENAME_CHARS for char in filename):
        return False, _("Filename contains forbidden characters.")

    # Check for Windows forbidden filenames
    name_without_ext = Path(filename).stem.upper()
    if name_without_ext in FORBIDDEN_FILENAMES:
        return False, _("Filename is reserved by the system.")

    # Check for path traversal attempts
    if ".." in filename or filename.startswith("/") or "~" in filename:
        return False, _("Invalid filename path.")

    return True, ""


def _detect_file_type_by_magic(file_content: bytes) -> str:
    """Detect file type by magic numbers for security.

    Args:
        file_content: First few bytes of the file

    Returns:
        Detected MIME type or empty string if unknown
    """
    for magic_bytes, mime_type in MAGIC_NUMBERS.items():
        if file_content.startswith(magic_bytes):
            return mime_type
    return ""


def _validate_uploaded_file(uploaded_file: UploadedFile) -> tuple[bool, str]:
    """Validate uploaded file for security and constraints.

    Returns:
        tuple: (is_valid, error_message)
    """
    # Validate filename
    is_valid_filename, error_msg = _validate_filename_security(uploaded_file.name)
    if not is_valid_filename:
        return False, error_msg

    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        size_mb = MAX_FILE_SIZE / (1024 * 1024)
        return False, _(f"File size exceeds maximum allowed size of {size_mb:.1f}MB.")

    # Check minimum file size (avoid empty files)
    if uploaded_file.size < 10:  # At least 10 bytes
        return False, _("File is too small or empty.")

    # Check file extension
    file_ext = Path(uploaded_file.name).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        allowed = ", ".join(sorted(ALLOWED_EXTENSIONS))
        return False, _(f"File type not supported. Allowed types: {allowed}")

    # Check declared MIME type
    content_type = uploaded_file.content_type
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        return False, _("Invalid file content type.")

    # Read first chunk to validate magic numbers
    try:
        uploaded_file.seek(0)  # Ensure we're at the beginning
        first_chunk = uploaded_file.read(32)  # Read first 32 bytes
        uploaded_file.seek(0)  # Reset for later use

        # Validate file magic numbers
        detected_type = _detect_file_type_by_magic(first_chunk)
        if detected_type and detected_type not in ALLOWED_MIME_TYPES:
            return False, _("File content does not match allowed types.")

        # Additional validation: ensure extension matches content
        if detected_type:
            expected_exts = {
                "image/jpeg": {".jpg", ".jpeg"},
                "image/png": {".png"},
                "image/gif": {".gif"},
                "image/webp": {".webp"},
            }
            if (
                detected_type in expected_exts
                and file_ext not in expected_exts[detected_type]
            ):
                return False, _("File extension does not match file content.")

    except Exception as e:
        logger.warning(f"Could not validate file magic numbers: {e}")
        # Don't fail validation just because we can't read magic numbers
        pass

    return True, ""


@csrf_exempt
@require_http_methods(["POST"])
@cache_control(no_cache=True, no_store=True, must_revalidate=True)
@vary_on_headers("X-Requested-With")
def vditor_images_upload_view(request: HttpRequest) -> JsonResponse:
    """Handle image uploads for Vditor editor.

    Args:
        request: HTTP request containing uploaded file

    Returns:
        JsonResponse with upload result
    """
    start_time = time.time()
    
    client_ip = request.META.get('REMOTE_ADDR', 'unknown')
    user_agent = request.META.get('HTTP_USER_AGENT', 'unknown')
    
    logger.info(
        f"Image upload request from {client_ip} - User-Agent: {user_agent[:100]}"
    )

    # Check if file was uploaded
    image_file = request.FILES.get("file[]")
    if not image_file:
        logger.warning(f"No file uploaded from {client_ip}")
        return JsonResponse(
            {
                "msg": _("No file uploaded."),
                "code": 1,
            },
            status=400,
        )

    # Validate uploaded file
    try:
        is_valid, error_msg = _validate_uploaded_file(image_file)
        if not is_valid:
            logger.warning(
                f"Invalid file upload attempt from {client_ip}: {error_msg}. "
                f"File: {image_file.name}, Size: {image_file.size}"
            )
            return JsonResponse(
                {
                    "msg": error_msg,
                    "code": 1,
                },
                status=400,
            )
    except Exception as e:
        logger.error(f"File validation error from {client_ip}: {e}")
        return JsonResponse(
            {
                "msg": _("File validation failed."),
                "code": 1,
            },
            status=500,
        )

    # Generate safe filename with hash for uniqueness
    original_filename = image_file.name
    try:
        safe_filename = secure_filename(original_filename)
        if not safe_filename:
            safe_filename = "unnamed_file.jpg"  # Default with extension

        # Create hash of file content for deduplication and security
        file_hash = hashlib.sha256()
        for chunk in image_file.chunks():
            file_hash.update(chunk)
        content_hash = file_hash.hexdigest()[:16]  # Use first 16 chars

        # Reset file pointer after hashing
        image_file.seek(0)

        # Generate unique filename with content hash
        file_stem = Path(safe_filename).stem[:50]  # Limit filename length
        file_ext = Path(safe_filename).suffix
        unique_filename = f"{content_hash}_{file_stem}{file_ext}"

        upload_path = Path(settings.MEDIA_ROOT)
        file_path = upload_path / unique_filename

        logger.info(
            f"Processing upload from {client_ip}: {original_filename} -> "
            f"{unique_filename} (hash: {content_hash}, size: {image_file.size})"
        )

        # Check if file already exists (deduplication)
        if file_path.exists():
            logger.info(f"File already exists, using existing: {unique_filename}")
            file_url = os.path.join(settings.MEDIA_URL, unique_filename)

            # Cache the response for successful duplicates
            response = JsonResponse(
                {
                    "msg": _("File uploaded successfully (deduplicated)."),
                    "code": 0,
                    "data": {
                        "errFiles": [],
                        "succMap": {
                            original_filename: file_url,
                        },
                    },
                }
            )
            response["Cache-Control"] = "public, max-age=3600"  # Cache for 1 hour
            
            processing_time = time.time() - start_time
            update_upload_metrics(image_file.size, processing_time, success=True)
            logger.info(
                f"Upload completed (deduplicated) in {processing_time:.3f}s "
                f"from {client_ip}"
            )
            return response

    except Exception as e:
        logger.error(
            f"Failed to process filename '{original_filename}' from {client_ip}: {e}"
        )
        return JsonResponse(
            {
                "msg": _("Invalid filename."),
                "code": 1,
            },
            status=400,
        )

    # Save file to disk
    try:
        # Ensure upload directory has secure permissions
        upload_path.mkdir(parents=True, exist_ok=True, mode=0o755)

        # Write file in chunks for memory efficiency with secure permissions
        bytes_written = 0
        temp_path = file_path.with_suffix(file_path.suffix + ".tmp")

        try:
            with open(temp_path, "wb") as f:
                for chunk in image_file.chunks():
                    f.write(chunk)
                    bytes_written += len(chunk)

            # Set secure file permissions
            os.chmod(temp_path, 0o644)

            # Atomic move to final location
            temp_path.rename(file_path)

        except Exception as e:
            # Clean up temp file on error
            temp_path.unlink(missing_ok=True)
            logger.error(f"File save error from {client_ip}: {e}")
            raise

        logger.info(
            f"Successfully saved file {unique_filename} ({bytes_written} bytes) "
            f"from {client_ip}"
        )

    except OSError as e:
        logger.error(
            f"Failed to create upload directory '{upload_path}' from {client_ip}: {e}"
        )
        return JsonResponse(
            {
                "msg": _("Failed to create upload directory."),
                "code": 1,
            },
            status=500,
        )
    except IOError as e:
        logger.error(f"Failed to write file '{file_path}' from {client_ip}: {e}")
        return JsonResponse(
            {
                "msg": _("Failed to save uploaded file."),
                "code": 1,
            },
            status=500,
        )
    except Exception as e:
        logger.error(f"Unexpected error during file save from {client_ip}: {e}")
        return JsonResponse(
            {
                "msg": _("An unexpected error occurred."),
                "code": 1,
            },
            status=500,
        )

    # Generate file URL
    try:
        file_url = os.path.join(settings.MEDIA_URL, unique_filename)
        logger.info(f"Upload completed successfully: {file_url}")

        response = JsonResponse(
            {
                "msg": _("Success!"),
                "code": 0,
                "data": {
                    "errFiles": [],
                    "succMap": {
                        original_filename: file_url,
                    },
                },
            }
        )
        # Cache successful uploads for better performance
        response["Cache-Control"] = "public, max-age=3600"  # Cache for 1 hour
        
        processing_time = time.time() - start_time
        update_upload_metrics(image_file.size, processing_time, success=True)
        logger.info(
            f"Upload completed successfully in {processing_time:.3f}s from {client_ip}"
        )
        return response
    except Exception as e:
        logger.error(f"Failed to generate file URL from {client_ip}: {e}")
        # Clean up the file if URL generation fails
        try:
            file_path.unlink(missing_ok=True)
        except Exception:
            pass
        return JsonResponse(
            {
                "msg": _("Failed to process uploaded file."),
                "code": 1,
            },
            status=500,
        )
