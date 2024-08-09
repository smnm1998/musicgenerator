from django.shortcuts import render
from google.cloud import storage
from django.conf import settings
from .forms import ImageUploadForm

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            # Google Cloud Storage 클라이언트 설정
            client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)

            # 이미지 업로드
            blob = bucket.blob(image.name)
            blob.upload_from_file(image, content_type=image.content_type)

            # 업로드된 파일의 URL 얻기
            uploaded_file_url = blob.public_url

            return render(request, 'upload.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})
