const lobbyId = document.getElementById('lobby_id').dataset.name;
let url = 'ws://' + window.location.host + '/ws/jeopardy/' + lobbyId + "/";

const GUESSDIGITS = 3;

let socket = new WebSocket(url);

let Countdown = 7;

const Board = document.getElementById('board')
const Question = document.getElementById('question');
const Answer = document.getElementById('answer');
const Users = document.getElementById('players');
const Select = document.getElementById('select');
let Points = 0

function questionClick(btn) {
    console.log(btn);
    socket.send(JSON.stringify({
        "type" : "question", "index" : btn
    }));
}
function removeAllChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}


document.getElementById('right').addEventListener('click', function(e) {
    socket.send(JSON.stringify({
        'type' : 'right',
        'points' : Points
    }));
});
document.getElementById('wrong').addEventListener('click', function(e) {
    socket.send(JSON.stringify({
        'type' : 'wrong',
        'points' : Points
    }));

})
document.getElementById('skip').addEventListener('click', function(e) {
    socket.send(JSON.stringify({
        'type' : 'skip',
    }));
})






function updateUsers(users){
    removeAllChildren(Users)
    for(let i = 0; i < users.length; i++)
    {
        let user = document.createElement("div");
        user.innerHTML = users[i]["name"] + ": " + users[i]["points"];
        user.classList.add("player");
        if(users[i]["buzzered"] == 1) {
            user.style.backgroundColor = "#FFA500";
        }
        Users.appendChild(user);
    }
}
let answer = ""
let startTime = new Date().getTime();
function timer() {

    var elapsed = (new Date().getTime() - startTime)/1000

    Answer.innerHTML = answer + "(" + (Countdown-elapsed).toFixed(2) + "s)";
    if(elapsed > Countdown)
    {
        Answer.innerHTML = answer;
        return;
    }
    setTimeout(timer, 50);
}

socket.onmessage = function(e) {
    var text_data = e.data;
    var data = JSON.parse(text_data);
    var typ = data["type"];
    if(typ == "question") {
        Board.classList.add("hidden");
        Question.classList.remove("hidden");
        Answer.classList.remove("hidden");
        document.getElementById("category").innerHTML = data["category"];
        document.getElementById("question-field").innerHTML = data["question"];
        document.getElementById("points").innerHTML = data["points"];
        Points = data["points"];
        Select.classList.remove("hidden");
        Answer.innerHTML = data["answer"];
        answer = data["answer"];
    }else if(typ == "update_users"){
        updateUsers(data["users"]);
        if(data["timer"] == 1)
        {
            startTime = new Date().getTime();
            timer()
        }
        //document.getElementById("board").classList.remove("hidden");
    }else if(typ == "update_board"){
        var exclude = data["exclude"];

        exclude.forEach(element => {
            document.getElementById(element).disabled = true
            document.getElementById(element).classList.add("done");
        });

        Board.classList.remove("hidden");
        Question.classList.add("hidden");
        Answer.classList.add("hidden");
        Select.classList.add("hidden");
    }else if(typ == "debug")
    {
        var text = data["message"];
        console.log("Server message: " + text);
    }
}
socket.onclose = function(e) {
    console.log("Connection closed");
    console.log(e);
}
socket.onopen = function(e) {
    console.log("Client connection established");
}
