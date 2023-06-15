
async function delete_contact_func(url, cont_id){
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
        return response.json()
    })
    
    if (status == 200){
        document.getElementById(cont_id).remove();
    }
    
}