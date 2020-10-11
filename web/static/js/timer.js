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
axios.defaults.withCredentials = true;

document.getElementById('start').addEventListener('click', function () {
    if (document.getElementById('start').innerHTML === 'START') {
        start = new Date();
        initScore();
        idTimeCount = setInterval(runTimer, 10);
        idFetchScore = setInterval(fetchScore, 1000);
        document.getElementById('start').innerHTML = 'STOP';

        document.getElementById('start-button-box').classList.remove('button');
        document.getElementById('start-button-box').classList.add('pushed-button');
        
        setBgm("/static/audio/MusMus-BGM-045.mp3")
    } else {
        clearInterval(idTimeCount);
        clearInterval(idFetchScore);
        initScore();
        resetDisplay();
    }
});

var runTimer = async function () {
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
        if (seconds > playMinute * 60) {
            seconds = playMinute * 60;
        }
        resetDisplay();
        uploadScore(seconds, await getScore(1));
        jumpToResultPage(1, await getAllScore(1), seconds);
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

  context.arc(300, 200, 150, -90 * Math.PI / 180, ((360 * persent / 100) - 90) * Math.PI / 180, false);
  context.strokeStyle = "red";
  context.lineWidth = 80;
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

// player_num = 1 ~ 4
var getScore = async function (player_num) {
    const data = await axios.get('/score/' + String(player_num));
    return data.data.point;
}

var getAllScore = async function (player_num) {
    var scores = [];
    for (let i = 1; i <= player_num; i++) {
        scores.push({ 'score': await getScore(i) });
    }
    console.log(scores);
    return scores;
}

var initScore = function () {
    axios.get('/init').then(function (response) {
        if(response.status == 200){
            console.log('initScore Success');
        }
    })
}

var uploadScore = function (time, score) {
    axios.post('https://lchika.club/platform/shooting_scores', {
        score: {
            time: time,
            miss: -1,
            score: score,
            name: 'test',
            player_num: 1
        }
    }).then(function (response) {
        if(response.status == 201){
            console.log('uploadScore Success');
        }else{
            console.log('faild to uploadScore');
        }
    })
}

var resetDisplay = function () {
    clearInterval(idTimeCount);
    document.getElementById('timer').innerHTML = '0' + String(playMinute) + ':00:00';
    //document.getElementById('timer').style.color = 'white';
    document.getElementById('start').innerHTML = 'START';

    document.getElementById('start-button-box').classList.remove('pushed-button');
    document.getElementById('start-button-box').classList.add('button');

    drawCircle(100);
}

var setBgm = function (src) {
    document.querySelector("#bgm source").src = src;
    document.querySelector("#bgm").load();
}

var jumpToResultPage = function (player_num, scores, time) {
    var url = 'result?player_num=' + String(player_num);
    for (let i = 0; i < player_num; i++) {
        url += '&score' + String(i) + '=' + String(scores[i]['score']);
        url += '&time' + String(i) + '=' + String(time);
    }
    //console.log(url)
    window.location.href = url;
}