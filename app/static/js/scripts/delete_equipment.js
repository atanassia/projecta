
async function delete_equipment_func(url, equipment_id){
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
        document.getElementById(equipment_id).remove();
    }
    

}