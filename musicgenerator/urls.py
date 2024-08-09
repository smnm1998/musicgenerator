from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from music import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('upload/')),  # 루트 URL을 /upload/로 리디렉션
    # path('', views.home, name='home'),  # 루트 URL에 대한 패턴 추가

    path('upload/', views.upload_image, name='upload_image'),
]
