
async function delete_ticket_photo_func(url, photo_id){
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    let status;
    const response = await fetch(url, {
        method:"DELETE",
        headers:{
            "X-CSRFToken": csrf_token,
        },
    })
    .then(response => {
        status = response.status;
        return status
    })
    
    if (status == 200){
        document.getElementById(photo_id).remove();
    }
    

}