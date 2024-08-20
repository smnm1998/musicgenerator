from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from music import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('upload/')),  # 루트 URL을 /upload/로 리디렉션
    # path('', views.home, name='home'),  # 루트 URL에 대한 패턴 추가

    path('upload/', views.image_upload_page, name='upload_image_page'),
    path('result/', views.result_page, name='result_page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)