document.addEventListener("DOMContentLoaded", function() {
    const playPauseButton = document.getElementById('play-pause-button');

    playPauseButton.addEventListener('click', function() {
        if (playPauseButton.textContent === '▶') {
            playPauseButton.textContent = '❚❚'; // 버튼을 누르면 일시정지 아이콘으로 변경
        } else {
            playPauseButton.textContent = '▶'; // 다시 누르면 재생 아이콘으로 변경
        }
    });
});
