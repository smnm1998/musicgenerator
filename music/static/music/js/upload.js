document.addEventListener('DOMContentLoaded', function() {
    const fileUpload = document.getElementById('file-upload');

    fileUpload.addEventListener('change', function(event) {
        const file = event.target.files[0];
        const reader = new FileReader();

        reader.onload = function(e) {
            const previewImage = document.getElementById('preview-image');
            const previewText = document.getElementById('preview-text');
            const selectButton = document.getElementById('select-button');

            // 이미지 미리보기 설정
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
            previewText.style.display = 'none';

            // "사진 선택하기" 버튼 숨김
            selectButton.style.display = 'none';

            // 업로드 및 다시 선택하기 버튼 추가
            const actionButtons = document.getElementById('file-upload');
            actionButtons.innerHTML = `
                <button class="button" id="upload-button">업로드하기</button>
                <button class="button" id="reselect-button">다시 선택하기</button>
            `;

            // 다시 선택하기 버튼 클릭 시
            document.getElementById('reselect-button').addEventListener('click', function() {
                document.getElementById('file-upload').click();
            });

            // 업로드하기 버튼 클릭 시
            document.getElementById('upload-button').addEventListener('click', function() {
                document.getElementById('upload-form').submit();  // 폼 제출
            });
        };

        if (file) {
            reader.readAsDataURL(file);
        }
    });
});
