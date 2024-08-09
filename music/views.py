# music/views.py

from django.shortcuts import render, redirect
from .forms import ImageUploadForm

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('success_url')  # 성공 시 리디렉션할 URL
    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})