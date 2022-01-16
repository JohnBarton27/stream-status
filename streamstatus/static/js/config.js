let configured_apps_elem = null;

function init() {
    update_app_table();
    update_welcome_video_display();
}

function update_app_table() {
    configured_apps_elem = document.getElementById('app-table')

    fetch('/api/configured_apps').then(function(response) {
        return response.text();
    }).then(function(html) {
        configured_apps_elem.innerHTML = html;
        setup_create_app_button();
    });
}

function update_welcome_video_display() {
    welcome_video_elem = document.getElementById('welcome-video')

    fetch('/api/configured_welcome_video').then(function(response) {
        return response.text();
    }).then(function(html) {
        welcome_video_elem.innerHTML = html;
        setup_save_wv_button();
    });
}

function setup_create_app_button() {
    document.getElementById("new-app-create").addEventListener("click", function () {
        let formData = new FormData();
        formData.append('name', document.getElementById("new-app-name").value);
        formData.append('hostname', document.getElementById("new-app-hostname").value);
        formData.append('port', document.getElementById("new-app-port").value);

        fetch('application', {
            method: 'PUT',
            body: formData
        }).then(function () {
            update_app_table();
        });
    });
}

function setup_save_wv_button() {
    document.getElementById("wv-update").addEventListener("click", function () {
        let formData = new FormData();
        formData.append('filepath', document.getElementById("welcome-video-path").value);

        fetch('welcome_video', {
            method: 'PUT',
            body: formData
        }).then(function () {
            update_welcome_video_display();
        });
    });

}