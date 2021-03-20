import os

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from formDecryption.models import ExcelFile


class DownloadFile(APIView):
    def get(self, request, pk):
        file_path = ExcelFile.objects.get(pk=pk).get_file_full_url()
        fp = os.path.join(settings.MEDIA_ROOT, file_path)
        with open(file_path, 'rb') as fh:
            response = HttpResponse(content_type="application/octet-stream")
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            response.write(fh.read())
            return response

    def post(self, request):
        for f in request.FILES:
            file = ExcelFile.objects.create(file=f, user=request.user)
            try:
                file.save()
            except Exception as e:
                return JsonResponse({'result': False, 'error': str(e.__str__())}, status=400)
            return JsonResponse({'result': True, 'file_url': file.get_file_full_url()}, status=400)
