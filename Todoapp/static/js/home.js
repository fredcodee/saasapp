var user = '{{request.user}}'

function getToken(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getToken('csrftoken');

var checkBtn = document.getElementsByClassName('edit');

for (i = 0; i < checkBtn.length; i++) {
    checkBtn[i].addEventListener("click", function () {
        var taskId = this.dataset.task;
        var action = this.dataset.action;
        console.log('working')
        check(taskId, action)
    });
}

function check(taskId, action) {
    var url = '/check/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,

        },
        body: JSON.stringify({ 'taskId': taskId, 'action': action })
    })

    .then((Response) => {
        return Response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })
}




var deleteBtn = document.getElementsByClassName('delete');

for (i = 0; i < deleteBtn.length; i++) {
    deleteBtn[i].addEventListener("click", function () {
        var taskId = this.dataset.task;
        deletetask(taskId)
        
    });
}


function deletetask(taskId){
    var url = '/delete/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        },
        body: JSON.stringify({'taskId': taskId})
    })
    .then((Response) => {
        return Response.json()
    })

    .then((data) => {
        console.log('data:', data)
        location.reload()
    })

}