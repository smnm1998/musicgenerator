# from django.shortcuts import render, redirect
# from google.cloud import storage
# from django.conf import settings
# import openai
# import base64
#
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
#             image_description = generate_image_caption()
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
#
# def generate_image_caption(image_content):
#     openai.api_key = settings.OPENAI_API_KEY
#
#     # GPT-3에 대한 설명 요청
#     prompt = "이 이미지에 대한 설명을 제공해주세요."
#     response = openai.Completion.create(
#         engine="text-davinci-003",
#         prompt=prompt,
#         max_tokens=100
#     )
#     return response.choices[0].text.strip()
#
#
# # 결과 페이지 뷰
# def result_page(request):
#     # 세션에서 이미지와 설명 가져오기
#     image_data = request.session.get('image_data')
#     image_description = request.session.get('image_description')
#
#     return render(request, 'music/result_page.html', {
#         'image_data': image_data,
#         'image_description': image_description,
#     })
#

from django.shortcuts import render, redirect
from django.conf import settings
import requests
import base64
import openai

from google.cloud import aiplatform
from google.cloud.aiplatform import pipeline_jobs

from django.http import FileResponse
import time
from google.cloud import storage

# 이미지 업로드 함수 -----------------------------
def image_upload_page(request):
    if request.method == 'POST':
        # 사용자가 업로드한 이미지 파일을 가져옴
        image = request.FILES['image']

        # 이미지 파일을 메모리에서 처리 (저장하지 않음)
        image_content = image.read()

        # 이미지 데이터를 Base64 형식으로 인코딩
        encoded_image = base64.b64encode(image_content).decode('utf-8')

        # OpenAI GPT로 이미지에 대한 캡셔닝 문구 생성
        try:
            image_description = generate_image_caption(image_content)  # image_content 전달
        except Exception as e:
            image_description = "이미지 설명 생성 중 오류 발생: " + str(e)

        # 세션에 이미지와 설명을 저장
        request.session['image_data'] = encoded_image
        request.session['image_description'] = image_description

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
                    {"type": "text", "text": "Describe this image"},
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

    # 파이프라인 제출
    pipeline_job = pipeline_jobs.PipelineJob(
        display_name="music-generation-pipeline",
        template_path="music_generation_pipeline.json",
        pipeline_root="gs://test_music_team_101/test_pipeline",
        parameter_values={
            "initial_prompt": caption_text,  # 캡셔닝된 텍스트를 파이프라인에 전달
            "user_prompt": "A bit more energetic and uplifting",  # 사용자 정의 프롬프트
            "endpoint_id": "projects/535442247184/locations/asia-northeast3/endpoints/7748060528844472320",
            "project": "andong-24-team-101",
            "region": "asia-northeast3"
        }
    )

    # 파이프라인 실행
    pipeline_job.submit()

    return pipeline_job.name  # 파이프라인 Job 이름 반환


# 최종 결과 페이지 함수 -----------------------------
def result_page(request):
    # 세션에서 이미지와 설명 가져오기
    image_data = request.session.get('image_data')
    image_description = request.session.get('image_description')

    return render(request, 'music/result_page.html', {
        'image_data': image_data,
        'image_description': image_description,
    })


#
# def get_music_file_from_gcs(bucket_name, file_name):
#     client = storage.Client()
#     bucket = client.bucket(bucket_name)
#     blob = bucket.blob(file_name)
#     local_file_path = f"/tmp/{file_name}"
#     blob.download_to_filename(local_file_path)
#     return local_file_path
#
# def result_page(request):
#     # 세션에서 캡셔닝된 텍스트 가져오기
#     image_description = request.session.get('image_description')
#
#     # Vertex AI 파이프라인 실행
#     job_name = run_music_generation_pipeline(image_description)
#
#     # 파이프라인 완료 대기 (예: 60초 대기)
#     time.sleep(60)
#
#     # GCS에서 음악 파일 다운로드
#     bucket_name = "test_music_team_101"
#     music_file_path = get_music_file_from_gcs(bucket_name, "generated_music.wav")
#
#     # 음악 파일을 반환
#     return FileResponse(open(music_file_path, 'rb'), as_attachment=True, filename="generated_music.wav")