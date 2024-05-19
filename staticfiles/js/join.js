const button = document.getElementById("join-btn");
const input = document.getElementById("id-input");


button.addEventListener("click", function () {
    id = input.value;
    if(id.length != 8) {
        console.log("please enter a valid 8 digit ID (expected 8 digits, got " + id.length + " digits)");
        return;
    }
    window.location.href = window.location.protocol + "//" + window.location.host + "/lobby/" + id;
});