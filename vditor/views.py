import logging
import os
import uuid
from pathlib import Path
from typing import Any

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from werkzeug.utils import secure_filename

from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)


@csrf_exempt
@require_http_methods(["POST"])
def vditor_images_upload_view(request: HttpRequest) -> JsonResponse:
    image_file = request.FILES.get("file[]")

    if not image_file:
        return JsonResponse(
            {
                "msg": _("No file uploaded."),
                "code": 1,
            },
            status=400,
        )

    original_filename = image_file.name
    safe_filename = secure_filename(original_filename)
    unique_filename = f"{uuid.uuid4()}_{safe_filename}"
    upload_path = Path(settings.MEDIA_ROOT)
    file_path = upload_path / unique_filename

    try:
        upload_path.mkdir(parents=True, exist_ok=True)
        with open(file_path, "wb+") as f:
            for chunk in image_file.chunks():
                f.write(chunk)
    except IOError as e:
        logger.error(f"Failed to write file: {e}")
        return JsonResponse(
            {
                "msg": _("Failed to save uploaded file."),
                "code": 1,
            },
            status=500,
        )

    file_url = os.path.join(settings.MEDIA_URL, unique_filename)

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
