from django.shortcuts import render, redirect
from google.cloud import storage
from django.conf import settings
from .forms import ImageUploadForm
import os

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data['image']

            # Google Cloud Storage 클라이언트 설정
            client = storage.Client(credentials=settings.GS_CREDENTIALS)
            bucket = client.bucket(settings.GS_BUCKET_NAME)

            # 이미지 파일을 'uploads/image/' 디렉터리에 저장
            file_path = os.path.join('uploads/image/', image.name)
            blob = bucket.blob(file_path)
            blob.upload_from_file(image, content_type=image.content_type)

            # 업로드된 파일의 URL 얻기
            uploaded_file_url = blob.public_url

            return render(request, 'music/upload.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
    else:
        form = ImageUploadForm()
    return render(request, 'music/upload.html', {'form': form})
#
# #
# from django.shortcuts import render, redirect
# from google.cloud import storage
# from django.conf import settings
# from .forms import ImageUploadForm
# import os
# from google.cloud.aiplatform import pipeline_jobs
#
# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image = form.cleaned_data['image']
#
#             # Google Cloud Storage 클라이언트 설정
#             client = storage.Client(credentials=settings.GS_CREDENTIALS)
#             bucket = client.bucket(settings.GS_BUCKET_NAME)
#
#             # 이미지 파일을 'uploads/image/' 디렉터리에 저장
#             file_path = os.path.join('uploads/image/', image.name)
#             blob = bucket.blob(file_path)
#             blob.upload_from_file(image, content_type=image.content_type)
#
#             # 업로드된 파일의 URL 얻기
#             uploaded_file_url = blob.public_url
#
#             # 파이프라인 실행
#             pipeline_root = 'gs://test_music_team_101/pipeline-root'
#             pipeline_job = pipeline_jobs.PipelineJob(
#                 display_name="music-generation-pipeline",
#                 template_path="gs://test_music_team_101/pipeline.json",
#                 pipeline_root=pipeline_root,
#                 parameter_values={
#                     "initial_prompt": "Input Description of desire for musical expression!",
#                     "user_prompt": "A bit more energetic and uplifting",
#                     "endpoint_id": "projects/535442247184/locations/asia-northeast3/endpoints/7748060528844472320",
#                     "project": "andong-24-team-101",
#                     "region": "asia-northeast3"
#                 }
#             )
#             pipeline_job.run(sync=True)
#
#             # 파이프라인 실행 후 결과 파일 URL을 얻기
#             music_file_url = f'{pipeline_root}/path-to-generated-music.wav'
#
#             return render(request, 'upload.html', {
#                 'form': form,
#                 'uploaded_file_url': uploaded_file_url,
#                 'music_file_url': music_file_url,
#             })
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload.html', {'form': form})