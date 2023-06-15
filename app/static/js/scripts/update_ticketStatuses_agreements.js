async function send_ticket_status_agreement(select_id, ticket_id, url_id, span_id, input_type='text'){
    var url = document.getElementById(url_id).dataset.url
    var csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value
    var value_select = document.getElementById(select_id).value
    var data = {'status':value_select}
    
    var status;
    const response = await fetch(url, {
        method:"PUT",
        headers:{
            "X-CSRFToken": csrf_token,
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        status = response.status;
        return response.json()
    })
    
    document.getElementById('ticket_statuses_messages_'+ticket_id).insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert"><strong>'+ response.message[0] +'</strong>. ' + response.message[1] + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
    
    if (status == 202){
        if(input_type == 'date'){
            document.getElementById(span_id).innerHTML = new Date(value_select).toLocaleDateString("fr-CH");
        }else{
            document.getElementById(span_id).innerHTML = value_select;
        }

        await new Promise(r => setTimeout(r, 5000));
        document.getElementById('ticket_statuses_messages_'+ticket_id).replaceChildren();
    }
}
