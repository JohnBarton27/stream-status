function updateCheckboxStatus(checkbox) {
    const checkboxId = checkbox.id;
    const isChecked = checkbox.checked;

    const labelElem = document.getElementById(checkboxId + "_LABEL")

    if (isChecked) {
        labelElem.classList.add("strikethrough")
    } else {
        labelElem.classList.remove("strikethrough")
    }

    // Send the API request to localhost:8001/api/update_checkbox_status
    // Replace this URL with your actual server endpoint
    const apiUrl = 'http://localhost:8001/api/update_checkbox_status';

    const requestData = {
        id: checkboxId,
        checked: isChecked
    };

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(requestData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Failed to update checkbox status.');
        }
        console.log('Checkbox status updated successfully!');
    })
    .catch(error => {
        console.error(error);
    });
}