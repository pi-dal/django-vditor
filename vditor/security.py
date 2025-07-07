"""
Security utilities for Django Vditor.

This module provides security-related functionality including
file validation, content sanitization, and upload protection.
"""

import logging
import re
from pathlib import Path
from typing import Dict

from django.conf import settings
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

# Default security settings
DEFAULT_MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
DEFAULT_ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
DEFAULT_ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
}

# Dangerous file patterns to block
DANGEROUS_EXTENSIONS = {
    ".php",
    ".php3",
    ".php4",
    ".php5",
    ".phtml",
    ".phps",
    ".asp",
    ".aspx",
    ".jsp",
    ".jspx",
    ".exe",
    ".bat",
    ".cmd",
    ".com",
    ".scr",
    ".pif",
    ".sh",
    ".bash",
    ".zsh",
    ".fish",
    ".js",
    ".vbs",
    ".ps1",
    ".py",
    ".rb",
    ".pl",
    ".html",
    ".htm",
    ".xhtml",
    ".xml",
    ".svg",
    ".jar",
    ".war",
    ".ear",
}

# Suspicious filename patterns
SUSPICIOUS_PATTERNS = [
    r"\.\./",  # Path traversal
    r'[<>:"|?*]',  # Windows forbidden chars
    r"^\.",  # Hidden files
    r"~$",  # Backup files
    r"\.tmp$",  # Temporary files
]


class SecurityValidator:
    """Validates files and content for security issues."""

    def __init__(self):
        self.max_file_size = getattr(
            settings, "VDITOR_MAX_FILE_SIZE", DEFAULT_MAX_FILE_SIZE
        )
        self.allowed_extensions = getattr(
            settings, "VDITOR_ALLOWED_EXTENSIONS", DEFAULT_ALLOWED_EXTENSIONS
        )
        self.allowed_mime_types = getattr(
            settings, "VDITOR_ALLOWED_MIME_TYPES", DEFAULT_ALLOWED_MIME_TYPES
        )

    def validate_filename(self, filename: str) -> tuple[bool, str]:
        """Validate filename for security issues.

        Args:
            filename: Filename to validate

        Returns:
            tuple: (is_valid, error_message)
        """
        if not filename:
            return False, _("Filename cannot be empty")

        # Check for dangerous extensions
        file_ext = Path(filename).suffix.lower()
        if file_ext in DANGEROUS_EXTENSIONS:
            return False, _("File type is not allowed for security reasons")

        # Check for suspicious patterns
        for pattern in SUSPICIOUS_PATTERNS:
            if re.search(pattern, filename):
                return False, _("Filename contains suspicious patterns")

        # Check filename length
        if len(filename) > 255:
            return False, _("Filename is too long")

        return True, ""

    def validate_file_content(self, content: bytes) -> tuple[bool, str]:
        """Validate file content for security issues.

        Args:
            content: File content bytes

        Returns:
            tuple: (is_valid, error_message)
        """
        if not content:
            return False, _("File content is empty")

        # Check for suspicious content patterns
        dangerous_patterns = [
            b"<?php",
            b"<%",
            b"<script",
            b"javascript:",
            b"vbscript:",
            b"data:text/html",
        ]

        content_lower = content.lower()
        for pattern in dangerous_patterns:
            if pattern in content_lower:
                return False, _("File contains potentially dangerous content")

        return True, ""


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for safe storage.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    if not filename:
        return "unnamed_file"

    # Remove path components
    filename = Path(filename).name

    # Replace dangerous characters
    filename = re.sub(r'[<>:"|?*\\]', "_", filename)

    # Remove control characters
    filename = re.sub(r"[\x00-\x1f\x7f-\x9f]", "", filename)

    # Limit length
    if len(filename) > 200:
        stem = Path(filename).stem[:150]
        suffix = Path(filename).suffix
        filename = f"{stem}{suffix}"

    # Ensure we have a valid filename
    if not filename or filename.startswith("."):
        filename = f"file_{filename}"

    return filename


def get_safe_upload_path(base_path: Path, filename: str) -> Path:
    """Get a safe upload path preventing directory traversal.

    Args:
        base_path: Base upload directory
        filename: Sanitized filename

    Returns:
        Safe absolute path for upload
    """
    # Ensure base path is absolute
    base_path = base_path.resolve()

    # Sanitize filename
    safe_filename = sanitize_filename(filename)

    # Construct safe path
    safe_path = base_path / safe_filename

    # Ensure the path is within base directory
    try:
        safe_path.resolve().relative_to(base_path)
    except ValueError:
        # Path is outside base directory, use safe fallback
        safe_path = base_path / f"safe_{safe_filename}"

    return safe_path


def log_security_event(event_type: str, details: Dict, request=None):
    """Log security-related events.

    Args:
        event_type: Type of security event
        details: Event details
        request: HTTP request object if available
    """
    log_data = {
        "event_type": event_type,
        "details": details,
    }

    if request:
        log_data.update(
            {
                "ip": request.META.get("REMOTE_ADDR", "unknown"),
                "user_agent": request.META.get("HTTP_USER_AGENT", "unknown"),
                "user": str(getattr(request, "user", None)),
            }
        )

    logger.warning(f"Security event: {log_data}")
