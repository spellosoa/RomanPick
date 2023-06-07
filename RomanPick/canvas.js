// 캔버스 요소와 컨텍스트 설정
var canvas = document.getElementById('textCanvas');
var ctx = canvas.getContext('2d');

// 텍스트 배열
var texts = [
    { text: '텍스트 1', link: 'https://example.com' },
    { text: '텍스트 2', link: 'https://example.com' },
    { text: '텍스트 3', link: 'https://example.com' },
    { text: '텍스트 4', link: 'https://example.com' },
    { text: '텍스트 5', link: 'https://example.com' }
];

// 텍스트 객체 생성
var textObjects = [];
var textWidth = 100; // 텍스트 너비
var textHeight = 30; // 텍스트 높이
for (var i = 0; i < texts.length; i++) {
    var textObj = {
        text: texts[i].text,
        link: texts[i].link,
        x: Math.random() * (canvas.width - textWidth), // x 좌표 랜덤 설정
        y: Math.random() * (canvas.height - textHeight), // y 좌표 랜덤 설정
        width: textWidth,
        height: textHeight,
        dx: (Math.random() - 0.5) * 2, // x 방향 속도
        dy: (Math.random() - 0.5) * 2 // y 방향 속도
    };
    textObjects.push(textObj);
}

// 링크 클릭 시 동작할 함수
function handleClick(link) {
    window.open(link, '_blank');
}

// 캔버스 클릭 이벤트 핸들러
canvas.addEventListener('click', function(event) {
    var mouseX = event.pageX - canvas.offsetLeft;
    var mouseY = event.pageY - canvas.offsetTop;

    for (var i = 0; i < textObjects.length; i++) {
        var textObj = textObjects[i];

        if (
            mouseX > textObj.x &&
            mouseX < textObj.x + textObj.width &&
            mouseY > textObj.y &&
            mouseY < textObj.y + textObj.height
        ) {
            handleClick(textObj.link);
            break; // 텍스트를 클릭한 경우, 반복문 종료
        }
    }
});

// 애니메이션 프레임 실행
function animate() {
    requestAnimationFrame(animate);
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (var i = 0; i < textObjects.length; i++) {
        var textObj = textObjects[i];

        // 텍스트 위치 업데이트
        textObj.x += textObj.dx;
        textObj.y += textObj.dy;

        // 벽 충돌 체크
        if (textObj.x < 0 || textObj.x > canvas.width - textObj.width) {
            textObj.dx *= -1;
        }
        if (textObj.y < 0 || textObj.y > canvas.height - textObj.height) {
            textObj.dy *= -1;
        }

        // 텍스트 그리기
        ctx.fillStyle = '#000';
        ctx.font = '18px sans-serif';
        ctx.fillText(textObj.text, textObj.x, textObj.y);
    }
}

animate();
