$(function() {

    var ws_scheme = window.location.protocol == "https:" ? "wss" : "ws";
    var ws_path = ws_scheme + '://' + window.location.host + 'ws/celerytasks';
    var socket = new WebSocket('ws://' + window.location.host + '/ws/celerytasks');

    cancelTask = function(id) {
        var message = {
            action: "cancel_celery_task",
            id: id
        };
        socket.send(JSON.stringify(message));
    };

    socket.addEventListener('message', function(event) {
        var data = JSON.parse(event.data);
    });

    socket.onmessage = function(message) {
        var data = JSON.parse(message.data);

        if (data.message.action == "started") {
            $('#celery_task_list')
                .append('<tr id=' + data.message.id + '><td>' + data.message.id +
                    '</td><td>' + data.message.name +
                    '</td><td>' + data.message.created +
                    '</td><td id="' + data.message.id + '_finished">' + data.message.finished +
                    '</td><td id="' + data.message.id + '_status">' + data.message.status +
                    '</td><td><button id="' + data.message.id + '_cancel" class="btn btn-danger" ' +
                    'onclick="cancelTask(' + data.message.id + ')">Cancel</button></td></tr>'
                );
        }
        else if (data.message.action == "completed") {
            $('#' + data.message.id + '_status').html(data.message.status);
            $('#' + data.message.id + '_finished').html(data.message.finished);
            $('#' + data.message.id + '_cancel').attr('disabled', true);
        }
        else if (data.message.action == "canceled") {
            $('#' + data.message.id + '_status').html(data.message.status);
            $('#' + data.message.id + '_cancel').attr('disabled', true);
        }
    };

    $("#celery_task_form").on("submit", function(event) {
        var message = {
            action: "new_celery_task",
            name: $('#celery_task_name').val()
        };
        socket.send(JSON.stringify(message));
        $("#task_name").val('').focus();
        return false;
    });
});