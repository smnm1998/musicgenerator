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
import openai
import base64
from google.cloud import vision

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


def generate_image_caption(image_content):
    """
    이 함수는 OpenAI GPT를 사용해 사용자가 업로드한 이미지에 대한 설명을 생성합니다.
    이 경우 이미지를 직접 분석하지 않고, 텍스트로만 작업을 수행합니다.
    """
    # OpenAI GPT API 호출
    openai.api_key = settings.OPENAI_API_KEY

    # 이미지를 기반으로 GPT에게 단순히 이미지 설명을 요청
    prompt = "이 이미지는 무엇을 표현하는지 설명해 주세요."

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "이미지 설명 생성."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150
    )

    return response['choices'][0]['message']['content'].strip()


def result_page(request):
    # 세션에서 이미지와 설명 가져오기
    image_data = request.session.get('image_data')
    image_description = request.session.get('image_description')

    return render(request, 'music/result_page.html', {
        'image_data': image_data,
        'image_description': image_description,
    })