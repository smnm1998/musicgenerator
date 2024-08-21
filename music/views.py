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


# 이미지 캡셔닝 생성 함수
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




def result_page(request):
    # 세션에서 이미지와 설명 가져오기
    image_data = request.session.get('image_data')
    image_description = request.session.get('image_description')

    return render(request, 'music/result_page.html', {
        'image_data': image_data,
        'image_description': image_description,
    })