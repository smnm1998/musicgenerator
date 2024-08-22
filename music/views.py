from django.shortcuts import render, redirect
from django.conf import settings
import requests
import base64
import uuid
import openai

from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs

from django.http import FileResponse
import time
from google.cloud import storage

# 이미지 업로드 함수 -----------------------------
# def image_upload_page(request):
#     if request.method == 'POST':
#         # 사용자가 업로드한 이미지 파일을 가져옴
#         image = request.FILES['image']
#
#         # 이미지 파일을 메모리에서 처리 (저장하지 않음)
#         image_content = image.read()
#
#         # 이미지 데이터를 Base64 형식으로 인코딩
#         encoded_image = base64.b64encode(image_content).decode('utf-8')
#
#         # OpenAI GPT로 이미지에 대한 캡셔닝 문구 생성
#         try:
#             image_description = generate_image_caption(image_content)  # image_content 전달
#         except Exception as e:
#             image_description = "이미지 설명 생성 중 오류 발생: " + str(e)
#
#         # 세션에 이미지와 설명을 저장
#         request.session['image_data'] = encoded_image
#         request.session['image_description'] = image_description
#
#         # 결과 페이지로 리디렉션
#         return redirect('result_page')
#
#     # GET 요청 시 업로드 폼 표시
#     return render(request, 'music/image_upload_page.html')

def image_upload_page(request):
    if request.method == 'POST':
        # 사용자가 업로드한 이미지 파일을 가져옴
        image = request.FILES['image']

        # 이미지 파일을 메모리에서 처리 (저장하지 않음)
        image_content = image.read()

        # OpenAI GPT로 이미지에 대한 캡셔닝 문구 생성
        try:
            image_description = generate_image_caption(image_content)  # image_content 전달
        except Exception as e:
            image_description = "이미지 설명 생성 중 오류 발생: " + str(e)

        # 세션에 이미지와 설명을 저장
        request.session['image_data'] = base64.b64encode(image_content).decode('utf-8')
        request.session['image_description'] = image_description

        # 파이프라인 실행: 캡셔닝된 텍스트를 user_prompt로 전달
        try:
            unique_filename = run_music_generation_pipeline(image_description)
            request.session['unique_filename'] = unique_filename  # 고유 파일 이름 세션에 저장
        except Exception as e:
            request.session['pipeline_error'] = "파이프라인 실행 중 오류 발생: " + str(e)

        # 결과 페이지로 리디렉션
        return redirect('result_page')

    # GET 요청 시 업로드 폼 표시
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
    # Vertex AI 초기화
    aiplatform.init(project='andong-24-team-101', location='asia-northeast3')

    # 고유 파일 이름 생성 (UUID 사용)
    unique_filename = f"New_{uuid.uuid4()}.wav"

    # 파이프라인 제출
    pipeline_job = aiplatform.PipelineJob(
        display_name="music-generation-pipeline",
        template_path="music_generation_pipeline.json",
        pipeline_root="gs://test_music_team_101/test_pipeline",
        parameter_values={
            "initial_prompt": "Input Description of desire for musical expression!",
            "user_prompt": caption_text,  # 캡셔닝된 텍스트를 user_prompt로 전달
            "endpoint_id": "projects/535442247184/locations/asia-northeast3/endpoints/7748060528844472320",
            "project": "andong-24-team-101",
            "region": "asia-northeast3",
            "gcs_bucket_name": "test_music_team_101",  # GCS 버킷 이름
            "gcs_output_path": f"test_wav/{unique_filename}"  # f-string 사용하여 고유 파일 이름 삽입
        }
    )

    # 파이프라인 실행
    pipeline_job.submit()

    return unique_filename  # 고유 파일 이름 반환


def get_gcs_file_url(bucket_name, file_path):
    # GCS 클라이언트 생성
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(file_path)

    # 파일이 존재하는지 확인
    if blob.exists():
        # GCS 파일 URL 생성
        return f"https://storage.googleapis.com/{bucket_name}/{file_path}"
    else:
        return None


def result_page(request):
    # 세션에서 이미지와 설명, 고유 파일 이름 가져오기
    image_data = request.session.get('image_data')
    image_description = request.session.get('image_description')
    unique_filename = request.session.get('unique_filename')  # 고유 파일 이름

    # 파이프라인에서 생성된 음악 파일 경로
    gcs_bucket_name = "test_music_team_101"
    gcs_file_path = f"test_wav/{unique_filename}"

    # GCS 파일 URL 가져오기
    music_file_url = get_gcs_file_url(gcs_bucket_name, gcs_file_path)

    return render(request, 'music/result_page.html', {
        'image_data': image_data,
        'image_description': image_description,
        'music_file': music_file_url,
    })





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