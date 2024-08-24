from django.shortcuts import render, redirect
from django.http import JsonResponse
import threading

from django.conf import settings
import requests
import base64
import uuid
import openai
from django.http import JsonResponse

from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs

from django.http import FileResponse
import time
from google.cloud import storage

from django.views.decorators.csrf import csrf_exempt


# @csrf_exempt
# def image_upload_page(request):
#     if request.method == 'POST':
#         # 사용자가 업로드한 이미지 파일을 가져옴
#         image = request.FILES['image']
#
#         # 이미지 파일을 메모리에서 처리 (저장하지 않음)
#         image_content = image.read()
#
#         # OpenAI GPT로 이미지에 대한 캡셔닝 문구 생성
#         try:
#             image_description = generate_image_caption(image_content)  # image_content 전달
#         except Exception as e:
#             image_description = "이미지 설명 생성 중 오류 발생: " + str(e)
#
#         # 세션에 이미지와 설명을 저장
#         request.session['image_data'] = base64.b64encode(image_content).decode('utf-8')
#         request.session['image_description'] = image_description
#
#         # 파이프라인 실행: 캡셔닝된 텍스트를 user_prompt로 전달
#         try:
#             unique_filename = run_music_generation_pipeline(image_description)
#             request.session['unique_filename'] = unique_filename  # 고유 파일 이름 세션에 저장
#         except Exception as e:
#             request.session['pipeline_error'] = "파이프라인 실행 중 오류 발생: " + str(e)
#
#         # 결과 페이지로 리디렉션
#         return redirect('result_page')
#
#     # GET 요청 시 업로드 폼 표시
#     return render(request, 'music/image_upload_page.html')


# GCS에 이미지 업로드 함수
def upload_image_to_gcs(image_content):
    storage_client = storage.Client()
    bucket_name = 'test_music_team_101'
    bucket = storage_client.bucket(bucket_name)

    # 고유 이미지 이름 생성
    unique_filename = f"test_image/{uuid.uuid4()}.jpg"
    blob = bucket.blob(unique_filename)

    # 이미지 업로드
    blob.upload_from_string(image_content, content_type='image/jpeg')

    # 이미지 URL 반환
    image_url = blob.public_url
    return unique_filename, image_url

@csrf_exempt
def image_upload_page(request):
    if request.method == 'POST':
        image = request.FILES['image']
        image_content = image.read()

        # 이미지를 GCS에 업로드
        unique_filename, image_url = upload_image_to_gcs(image_content)

        # OpenAI GPT로 이미지에 대한 캡셔닝 문구 생성
        try:
            image_description = generate_image_caption(image_content)  # image_content를 전달하여 캡셔닝 생성
        except Exception as e:
            image_description = "이미지 설명 생성 중 오류 발생: " + str(e)

        # 세션에 이미지 URL과 설명을 저장
        request.session['image_url'] = image_url
        request.session['image_description'] = image_description

        # 파이프라인 실행: 캡셔닝된 텍스트를 user_prompt로 전달
        try:
            generated_music_filename = run_music_generation_pipeline(image_description)  # 캡셔닝된 텍스트를 파이프라인에 전달
            request.session['generated_music_filename'] = generated_music_filename  # 음악 파일명 저장

            # 로딩 페이지로 리디렉션
            return redirect('loading_page')
        except Exception as e:
            return redirect('loading_page')

    return render(request, 'music/image_upload_page.html')

# 이미지 캡셔닝 생성 함수 -----------------------------
def generate_image_caption(image_content):
    # 이미지를 base64로 인코딩
    base64_image = base64.b64encode(image_content).decode('utf-8')

    # OpenAI API 키 설정
    api_key = settings.OPENAI_API_KEY

    # OpenAI API 요청 헤더
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # OpenAI API 요청 페이로드
    payload = {
        "model": "gpt-4o-mini",  # 적절한 모델을 사용하세요
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "A detailed portrait of a person standing in a serene outdoor environment. The individual is wearing a casual outfit with a comfortable sweater and jeans, conveying a relaxed and approachable demeanor. They have short, neatly styled brown hair and are smiling warmly, with their eyes showing kindness and a hint of curiosity. Their posture is confident yet relaxed, with one hand casually resting in their pocket. The background features a soft, blurred landscape, emphasizing the focus on the person and their friendly expression."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ],
        "max_tokens": 100
    }

    # OpenAI API 요청
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # 응답 확인 및 처리
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "이미지 설명 생성 중 오류 발생"


# 파이프라인 전송 함수
def run_music_generation_pipeline(caption_text):
    aiplatform.init(project='andong-24-team-101', location='asia-northeast3')
    unique_filename = f"New_{uuid.uuid4()}.wav"

    # 로그 추가: user_prompt에 전달되는 캡셔닝 텍스트를 출력
    print(f"user_prompt로 전달되는 캡셔닝 텍스트: {caption_text}")

    pipeline_job = aiplatform.PipelineJob(
        display_name="music-generation-pipeline",
        template_path="music_generation_pipeline.json",
        pipeline_root="gs://test_music_team_101/test_pipeline",
        parameter_values={
            "initial_prompt": "Input Description of desire for musical expression!",
            "user_prompt": caption_text,
            "endpoint_id": "projects/535442247184/locations/asia-northeast3/endpoints/7748060528844472320",
            "project": "andong-24-team-101",
            "region": "asia-northeast3",
            "gcs_bucket_name": "test_music_team_101",
            "gcs_output_path": f"test_wav/{unique_filename}"
        }
    )

    pipeline_job.submit()
    return unique_filename  # 생성된 음악 파일명 반환


# GCS 파일 존재 여부 확인 함수
def file_exists_in_gcs(bucket_name, file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)
    return blob.exists()

# 파일 존재 여부 체크 API
# 파일 존재 여부 체크 API
def check_file_in_gcs(request):
    generated_music_filename = request.session.get('generated_music_filename')
    if generated_music_filename:
        file_path = f'test_wav/{generated_music_filename}'
        file_exists = file_exists_in_gcs('test_music_team_101', file_path)
        print(f"Checking if file exists: {file_exists}")  # 로그 추가
        if file_exists:
            return JsonResponse({'file_exists': True})
    return JsonResponse({'file_exists': False})

# 로딩 페이지
def loading_page(request):
    return render(request, 'music/loading_page.html')

# 결과 페이지
def result_page(request):
    image_url = request.session.get('image_url')
    generated_music_filename = request.session.get('generated_music_filename')

    # GCS에서 생성된 음악 파일 URL 가져오기
    music_file_url = get_gcs_file_url('test_music_team_101', f'test_wav/{generated_music_filename}')

    return render(request, 'music/result_page.html', {
        'image_url': image_url,
        'music_file': music_file_url,
    })

def get_gcs_file_url(bucket_name, file_path):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)

    if blob.exists():
        return blob.public_url
    return None























# def result_page(request):
#     # 세션에서 이미지와 설명, 고유 파일 이름 가져오기
#     image_data = request.session.get('image_data')
#     image_description = request.session.get('image_description')
#     unique_filename = request.session.get('unique_filename')  # 고유 파일 이름
#
#     # 파이프라인에서 생성된 음악 파일 경로
#     gcs_bucket_name = "test_music_team_101"
#     gcs_file_path = f"test_wav/{unique_filename}"
#
#     # GCS 파일 URL 가져오기
#     music_file_url = get_gcs_file_url(gcs_bucket_name, gcs_file_path)
#
#     return render(request, 'music/result_page.html', {
#         'image_data': image_data,
#         'image_description': image_description,
#         'music_file': music_file_url,
#     })





# # 최종 결과 페이지 함수 -----------------------------
# def result_page(request):
#     # 세션에서 이미지와 설명 가져오기
#     image_data = request.session.get('image_data')
#     image_description = request.session.get('image_description')
#
#     return render(request, 'music/result_page.html', {
#         'image_data': image_data,
#         'image_description': image_description,
#     })