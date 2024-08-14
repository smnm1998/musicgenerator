# from django.shortcuts import render, redirect
# from google.cloud import storage
# from django.conf import settings
# from .forms import ImageUploadForm
# import os
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
#             return render(request, 'upload.html', {'form': form, 'uploaded_file_url': uploaded_file_url})
#     else:
#         form = ImageUploadForm()
#     return render(request, 'upload.html', {'form': form})
#
#
#

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

            # 이미지 파일을 읽어들여 업로드
            blob.upload_from_file(image.file, content_type=image.content_type)

            # 업로드된 파일의 URL 얻기
            uploaded_file_url = blob.public_url

            # 이미지 URL을 파이프라인에 전달하여 음악 생성
            generated_music_url = send_image_to_pipeline(uploaded_file_url)

            return render(request, 'result.html',
                          {'uploaded_file_url': uploaded_file_url, 'generated_music_url': generated_music_url})
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})


def send_image_to_pipeline(image_url):
    from google.cloud import aiplatform

    # 파이프라인 실행을 위한 설정
    project = 'your-gcp-project-id'
    region = 'your-gcp-region'
    pipeline_root = 'gs://your-bucket-name/pipeline-root'
    endpoint_id = 'your-endpoint-id'

    # 파이프라인 컴파일 및 제출
    pipeline_job = aiplatform.PipelineJob(
        display_name="music-generation-pipeline",
        template_path="gs://your-bucket-name/pipeline.json",
        pipeline_root=pipeline_root,
        parameter_values={
            "initial_prompt": "Generate music for the provided image.",
            "user_prompt": image_url,  # 이미지를 프롬프트로 전달
            "endpoint_id": endpoint_id,
            "project": project,
            "region": region
        }
    )

    # 파이프라인 실행
    pipeline_job.run()

    # 파이프라인 실행 완료 후 결과 URL 반환 (예시)
    generated_music_url = "https://storage.googleapis.com/your-bucket-name/generated_music.wav"
    return generated_music_url
