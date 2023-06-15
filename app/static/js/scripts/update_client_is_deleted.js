async function update_client_is_deleted_func(url){
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
    let status;
    const response = await fetch(url, {
        method:"PUT",
        headers:{
            "X-CSRFToken": csrf_token,
        },
    })
    .then(response => {
        status = response.status;
        return response.json()
    })

    if (status == 202){
        document.getElementById('breadcrumb_message').insertAdjacentHTML('beforeend',
        '<div class="row">'+
            '<div class="alert alert-danger" role="alert">Клиент успешно удален!!!</div>'+
        '</div>'
    );}
 
}