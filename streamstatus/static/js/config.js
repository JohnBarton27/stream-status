let configured_apps_elem = null;

function init() {
    update_app_table();
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