import os
import uuid

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from .configs import VditorConfig


VDITOR_CONFIGS = VditorConfig('default')


@require_http_methods(['POST'])
@method_decorator(csrf_exempt)
def VditorImagesUploadView(request):
    VditorImagesUpload = request.FILES.get('file[]', None)
    VditorImagesNameList = VditorImagesUpload.name.split('.')
    VditorImagesName = '.'.join(VditorImagesNameList)
    VditorImagesUploadPath = os.path.join(settings.MEDIA_ROOT)
    VditorImagesNameFull = '%s_%s' % (uuid.uuid4(), VditorImagesName)
    if not VditorImagesNameList:
        print('No picture')
    else:
        if not os.path.exists(VditorImagesUploadPath):
            try:
                os.makedirs(VditorImagesUploadPath)
            except Exception as err:
                print("upload failed：%s" % str(err))
        else:
            with open(os.path.join(VditorImagesUploadPath, VditorImagesNameFull), 'wb+') as file:
                for chunk in VditorImagesUpload.chunks():
                    file.write(chunk)
            return JsonResponse(
                {
                    "msg": "Success!",
                    "code": 0,
                    "data": {
                    "errFiles": [],
                    "succMap": {
                        VditorImagesName: os.path.join(settings.MEDIA_URL, VditorImagesNameFull),
                        }
                    }
                }
            )
