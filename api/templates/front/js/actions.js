function sendBlood(bloodpack) {
    var req = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/api/add_portion";
    req.open("POST", url);
    req.send(bloodpack);
    if (req.responseText == "True") {
        alert("Submitted successfully.");
    } else {
        alert("An error occured: " + req.responseText);
    }
}

function getBlood(bloodpack) {
    var req = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/api/get_portion";
    req.open("POST", url);
    req.send(bloodpack);
    if (req.responseText == "True") {
        alert("Pulled successfully.");
    } else {
        alert("An error occured: " + req.responseText);
    }
}

function mciReport(bloodpacks) {
    var req = new XMLHttpRequest();
    var url = "http://127.0.0.1:5000/api/get_portions";
    req.open("POST", url);
    req.send(bloodpacks);
    if (req.responseText == "True") {
        alert("Pulled successfully.");
    } else {
        alert("An error occured: " + req.responseText);
    }
}