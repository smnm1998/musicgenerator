document.addEventListener("DOMContentLoaded", function() {
    const audioPlayer = document.getElementById('audio-player');
    const playPauseButton = document.getElementById('play-pause-button');
    const prevButton = document.getElementById('prev-button');
    const nextButton = document.getElementById('next-button');
    const currentTimeElement = document.getElementById('current-time');
    const totalDurationElement = document.getElementById('total-duration');
    const progBar = document.querySelector('.prog-bar');
    const progBarInner = document.querySelector('.prog-bar-inner');
    const albumArtImage = document.getElementById('albumart-image');

    // 음악 재생 시간 업데이트
    audioPlayer.addEventListener('timeupdate', function() {
        const currentTime = audioPlayer.currentTime;
        const duration = audioPlayer.duration;

        if (!isNaN(duration)) {
            const progressPercent = (currentTime / duration) * 100;
            progBarInner.style.width = `${progressPercent}%`;
            currentTimeElement.textContent = formatTime(currentTime);
        }
    });

    // 음악 총 길이 설정
    audioPlayer.addEventListener('loadedmetadata', function() {
        const duration = audioPlayer.duration;
        totalDurationElement.textContent = formatTime(duration);
    });

    // 재생/일시정지 버튼 클릭 시 동작
    playPauseButton.addEventListener('click', function() {
        if (audioPlayer.paused) {
            audioPlayer.play();
            playPauseButton.textContent = '❚❚'; // 버튼을 누르면 일시정지 아이콘으로 변경
            albumArtImage.style.animationPlayState = 'running'; // CD 회전 애니메이션 재개
        } else {
            audioPlayer.pause();
            playPauseButton.textContent = '▶'; // 다시 누르면 재생 아이콘으로 변경
            albumArtImage.style.animationPlayState = 'paused'; // CD 회전 애니메이션 일시정지
        }
    });

    // -10초 건너뛰기
    prevButton.addEventListener('click', function() {
        audioPlayer.currentTime = Math.max(0, audioPlayer.currentTime - 10);
    });

    // +10초 건너뛰기
    nextButton.addEventListener('click', function() {
        audioPlayer.currentTime = Math.min(audioPlayer.duration, audioPlayer.currentTime + 10);
    });

    // 프로그레스 바 클릭 시 시간 이동 기능 추가
    progBar.addEventListener('click', function(event) {
        const rect = progBar.getBoundingClientRect();
        const offsetX = event.clientX - rect.left; // 프로그레스 바의 시작 지점에서부터 클릭한 지점까지의 거리
        const width = rect.width; // 프로그레스 바의 전체 너비
        const clickPositionPercent = offsetX / width; // 클릭한 위치를 백분율로 계산
        const duration = audioPlayer.duration;
        audioPlayer.currentTime = duration * clickPositionPercent; // 재생 시간을 클릭된 위치에 맞춰 설정
    });

    // 시간을 mm:ss 형식으로 변환하는 함수
    function formatTime(time) {
        const minutes = Math.floor(time / 60);
        const seconds = Math.floor(time % 60);
        return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
});
