const lobbyId = document.getElementById('lobby_id').dataset.name;
let url = 'ws://' + window.location.host + '/ws/jeopardy/' + lobbyId + "/";

const GUESSDIGITS = 3;

let socket = new WebSocket(url);

const Board = document.getElementById('board')
const Question = document.getElementById('question');
const Users = document.getElementById('players');

function removeAllChildren(element) {
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}


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

document.getElementById('buzzer').addEventListener("click", () => {
    socket.send(JSON.stringify({
        "type": "buzzer"
    }))
});

socket.onmessage = function(e) {
    var text_data = e.data;
    var data = JSON.parse(text_data);
    var typ = data["type"];
    if(typ == "question") {
        Board.classList.add("hidden");
        Question.classList.remove("hidden");
        document.getElementById("buzzer").classList.remove("hidden");
        document.getElementById("category").innerHTML = data["category"]
        document.getElementById("question-field").innerHTML = data["question"]
        document.getElementById("points").innerHTML = data["points"]
        //document.getElementById("board").classList.remove("hidden");
    }else if(typ == "update_board"){
        var exclude = data["exclude"];

        exclude.forEach(element => {
            document.getElementById(element).disabled = true
            document.getElementById(element).classList.add("done");
        });

        Board.classList.remove("hidden");
        Question.classList.add("hidden");
        document.getElementById("buzzer").classList.add("hidden");
        Answer.classList.add("hidden");
        Select.classList.add("hidden");
    }else if(typ == "update_users"){
        updateUsers(data["users"]);
        console.log(data["users"]);
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
