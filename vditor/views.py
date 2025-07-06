import logging
import os
import uuid
from pathlib import Path
from typing import Any, Dict

from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from werkzeug.utils import secure_filename

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

# Configuration constants
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"}
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
    "image/svg+xml",
}


def _validate_uploaded_file(uploaded_file: UploadedFile) -> tuple[bool, str]:
    """Validate uploaded file for security and constraints.

    Returns:
        tuple: (is_valid, error_message)
    """
    if not uploaded_file.name:
        return False, _("File must have a name.")

    # Check file size
    if uploaded_file.size > MAX_FILE_SIZE:
        return False, _("File size exceeds maximum allowed size of 10MB.")

    # Check file extension
    file_ext = Path(uploaded_file.name).suffix.lower()
    if file_ext not in ALLOWED_EXTENSIONS:
        return False, _(
            "File type not supported. Allowed types: JPG, PNG, GIF, WebP, SVG."
        )

    # Check MIME type
    content_type = uploaded_file.content_type
    if content_type and content_type not in ALLOWED_MIME_TYPES:
        return False, _("Invalid file content type.")

    return True, ""


@csrf_exempt
@require_http_methods(["POST"])
def vditor_images_upload_view(request: HttpRequest) -> JsonResponse:
    """Handle image uploads for Vditor editor.

    Args:
        request: HTTP request containing uploaded file

    Returns:
        JsonResponse with upload result
    """
    logger.info(
        f"Image upload request from {request.META.get('REMOTE_ADDR', 'unknown')}"
    )

    # Check if file was uploaded
    image_file = request.FILES.get("file[]")
    if not image_file:
        logger.warning("Upload request received without file")
        return JsonResponse(
            {
                "msg": _("No file uploaded."),
                "code": 1,
            },
            status=400,
        )

    # Validate uploaded file
    is_valid, error_msg = _validate_uploaded_file(image_file)
    if not is_valid:
        logger.warning(
            f"Invalid file upload attempt: {error_msg}. File: {image_file.name}"
        )
        return JsonResponse(
            {
                "msg": error_msg,
                "code": 1,
            },
            status=400,
        )

    # Generate safe filename
    original_filename = image_file.name
    try:
        safe_filename = secure_filename(original_filename)
        if not safe_filename:
            safe_filename = "unnamed_file"
        unique_filename = f"{uuid.uuid4()}_{safe_filename}"
        upload_path = Path(settings.MEDIA_ROOT)
        file_path = upload_path / unique_filename

        logger.info(f"Processing upload: {original_filename} -> {unique_filename}")
    except Exception as e:
        logger.error(f"Failed to process filename '{original_filename}': {e}")
        return JsonResponse(
            {
                "msg": _("Invalid filename."),
                "code": 1,
            },
            status=400,
        )

    # Save file to disk
    try:
        upload_path.mkdir(parents=True, exist_ok=True)

        # Write file in chunks for memory efficiency
        bytes_written = 0
        with open(file_path, "wb") as f:
            for chunk in image_file.chunks():
                f.write(chunk)
                bytes_written += len(chunk)

        logger.info(
            f"Successfully saved file {unique_filename} ({bytes_written} bytes)"
        )

    except OSError as e:
        logger.error(f"Failed to create upload directory '{upload_path}': {e}")
        return JsonResponse(
            {
                "msg": _("Failed to create upload directory."),
                "code": 1,
            },
            status=500,
        )
    except IOError as e:
        logger.error(f"Failed to write file '{file_path}': {e}")
        return JsonResponse(
            {
                "msg": _("Failed to save uploaded file."),
                "code": 1,
            },
            status=500,
        )
    except Exception as e:
        logger.error(f"Unexpected error during file save: {e}")
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

        return JsonResponse(
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
    except Exception as e:
        logger.error(f"Failed to generate file URL: {e}")
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
