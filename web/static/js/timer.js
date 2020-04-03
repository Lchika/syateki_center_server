var point;
var sec;
var seconds;
var min;
var hour;
var start;
var now;
var time;
var idTimeCount;
var idFetchScore;
const playMinute = 1;

document.getElementById('start').addEventListener('click', function () {
    if (document.getElementById('start').innerHTML === 'START') {
        start = new Date();
        idTimeCount = setInterval(runTimer, 10);
        idFetchScore = setInterval(fetchScore, 1000);
        document.getElementById('start').innerHTML = 'STOP';

        document.getElementById('start-button-box').classList.remove('button');
        document.getElementById('start-button-box').classList.add('pushed-button');
    } else {
        clearInterval(idTimeCount);
        clearInterval(idFetchScore);
        document.getElementById('start').innerHTML = 'START';
        document.getElementById('timer').innerHTML = '0' + String(playMinute) + ':00:00';

        document.getElementById('start-button-box').classList.remove('pushed-button');
        document.getElementById('start-button-box').classList.add('button');
        drawCircle(100);
    }
});

var runTimer = function () {
    now = new Date();
    time = now.getTime() - start.getTime();

    point = Math.floor(time / 10);
    sec = Math.floor(time / 1000);
    min = Math.floor(sec / 60);
    hour = Math.floor(min / 60);
    seconds = Math.floor(time / 1000);

    if (seconds < playMinute * 60) {
        point = 99 - (point - sec * 100);
        sec = 59 - (sec - min * 60);
        min = (playMinute - 1) - (min - hour * 60);

        point = addZero(point);
        sec = addZero(sec);
        min = addZero(min);

        document.getElementById('timer').innerHTML = min + ':' + sec + ':' + point;

        drawCircle(100 * (playMinute * 60 - seconds) / (playMinute * 60));
    } else {
        clearInterval(idTimeCount);
        document.getElementById('timer').innerHTML = '0' + String(playMinute) + ':00:00';
        //document.getElementById('timer').style.color = 'white';
        document.getElementById('start').innerHTML = 'START';

        document.getElementById('start-button-box').classList.remove('pushed-button');
        document.getElementById('start-button-box').classList.add('button');

        drawCircle(100);
    }

}

var addZero = function (value) {
    if (value < 10) {
        value = '0' + value;
    }
    return value;
}

var drawCircle = function (persent) {
  const canvas = document.getElementById('canvas-timer');
  const context = canvas.getContext('2d');
  
  context.clearRect(0, 0, canvas.width, canvas.height);
  
  context.beginPath();

  context.arc(100, 100, 50, -90 * Math.PI / 180, (270 * persent / 100) * Math.PI / 180, false);
  context.strokeStyle = "red";
  context.lineWidth = 40;
  context.stroke();
}

var fetchScore = function () {
    if(document.getElementById("bullet_1") != null){
        axios.get('/score/1').then(function (response) {
            if(response.status == 200){
                document.getElementById("bullet_1").innerHTML = response.data.bullet;
                document.getElementById("score_1").innerHTML = response.data.point;
            }
        })
    }
}