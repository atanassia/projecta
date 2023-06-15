if(document.getElementById('type_status_tickets')){
    document.getElementById('send_ticket_types').addEventListener('click',  async () => await send_ticket_status('id_ticket_types', 'send_ticket_types'))
    document.getElementById('send_ticket_statuses').addEventListener('click',  async () => await send_ticket_status('id_ticket_statuses', 'send_ticket_statuses'))
}

if(document.getElementById('id_agreement_statuses')){
    document.getElementById('send_agreement_statuses').addEventListener('click',  async () => await send_ticket_status('id_agreement_statuses', 'send_agreement_statuses'))
}

if(document.getElementById('act_tickets')){
    document.getElementById('send_act_statuses').addEventListener('click',  async () => await send_ticket_status('id_act_statuses', 'send_act_statuses'))
    document.getElementById('send_check_statuses').addEventListener('click',  async () => await send_ticket_status('id_check_statuses', 'send_check_statuses'))
}
if(document.getElementById('send_ticket_execution_date')){
    document.getElementById('send_ticket_execution_date').addEventListener('click',  async () => await send_ticket_status('id_execution_date', 'send_ticket_execution_date', 'date'))
}

if(document.getElementById('change_comment')){
   document.getElementById('send_ticket_comment').addEventListener('click',  async () => await send_ticket_status('id_ticket_comment', 'send_ticket_comment'))
}

async function send_ticket_status(select_id, url_id, input_type='text'){
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
    
    document.getElementById('ticket_statuses_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert"><strong>'+ response.message[0] +'</strong>. ' + response.message[1] + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
    
    if (status == 202){
        if(input_type == 'date'){
            document.getElementById('data'+select_id.slice(2)).innerHTML = new Date(value_select).toLocaleDateString("fr-CH");
        }else{
            document.getElementById('data'+select_id.slice(2)).innerHTML = value_select;
        }

        await new Promise(r => setTimeout(r, 5000));
        document.getElementById("ticket_statuses_messages").replaceChildren();
    } 
}