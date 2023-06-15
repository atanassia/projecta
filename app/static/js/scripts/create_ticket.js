
document.getElementById('send_ticket').addEventListener('click',  async () => await create_ticket())


async function create_ticket(){
    url = document.getElementById('send_ticket').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_ticket');
    var data = JSON.stringify(Object.fromEntries(new FormData(form)));

    var schema = JSON.parse(data)
    var result = [];
    for(var i in schema)
        result.push([i, schema [i]]);
    
    let status;
    const response = await fetch(url, {
        method:"POST",
        headers:{
            "X-CSRFToken": csrf_token,
        },
        body: data,
    })
    .then(response => {
        status = response.status;
        return response.json()
    })
    .catch((error) => {
        document.getElementById('ticket_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
    });
    
    document.getElementById('ticket_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
    
    if (status == 201){
        await new Promise(r => setTimeout(r, 1000));
        var myModalEl = document.getElementById('addTicket');
        var modal = bootstrap.Modal.getInstance(myModalEl)
        modal.hide();
        
        if(document.getElementById("no-data")){
            document.getElementById('no-data').remove();
        }

        document.getElementById('ticket_messages').replaceChildren();

        var no_null_tickets = document.getElementById('no-tickets');
        if(no_null_tickets != null){
            no_null_tickets.remove();
        }

        if(document.getElementById('ticket_row')){
            var type_select = document.getElementById("id_ticket_type");
            var status_select = document.getElementById("id_status");
            var type_data = "";
            var status_data = ""
            for (var i = 0; i < type_select.length; i++) {
                if(type_select[i].value == result[1][1]){
                    type_data += '<option value="'+type_select[i].value+'" selected>'+type_select[i].value+'</option>'
                }else{
                    type_data += '<option value="'+type_select[i].value+'">'+type_select[i].value+'</option>'
                }
            }
            for (var i = 0; i < status_select.length; i++) {
                if(status_select[i].value == result[2][1]){
                    status_data += '<option value="'+status_select[i].value+'" selected>'+status_select[i].value+'</option>'
                }else{
                    status_data += '<option value="'+status_select[i].value+'">'+status_select[i].value+'</option>'
                }
            }

            var date = new Date();
            if(result[3][1]){
                date = new Date(result[3][1]).toLocaleDateString("fr-CH")
            }
            else{
                date = new Date(date.getFullYear(), date.getMonth() + 1, 0).toLocaleDateString("fr-CH")
            }


            document.getElementById('ticket_row').insertAdjacentHTML('afterbegin',
                '<div class="col mt-3">'+
                    '<div class="card">'+
                        '<div class="card-header text-bg-success">'+
                            '<div class="d-flex p-2">'+
                                '<div><strong>Заявка №'+ response.id +'</strong></div>'+
                                '<div class="ms-auto"><span class="badge text-bg-dark text-end" id="data_ticket_statuses_'+ response.id +'">'+ result[2][1] +'</span></div>'+
                            '</div>'+
                        '</div>'+
                        '<div class="card-body">'+
                            '<div class="card-text">'+
                                '<ul class="list-group-flush">'+
                                    '<li><strong>Тип</strong> - <span id="data_ticket_types_'+ response.id +'">'+ result[1][1] +'</li>'+
                                    '<li><strong>Дата выезда</strong> - ' + date +'</li>'+
                                    '<li><strong>Обновлено</strong> - '+ new Date().toLocaleString("ru-RU").slice(0, -3) +'</li>'+
                                    '<li><strong>Автор</strong> - '+ document.getElementById('usersname').getAttribute('data-value') +'</li>'+
                                '</ul>'+

                                    '<div class="d-flex">'+
                                    '<div class="ms-auto">'+
                                        '<a type="button" class="btn ms-auto" data-bs-toggle="modal" data-bs-target="#changeTicket'+ response.id +'Statuses" title="Обновить заявку">'+
                                            '<img src="/static/icons/update.svg" style="width: 18px;">'+
                                        '</a>'+

                                        '<div class="modal fade" id="changeTicket'+ response.id +'Statuses" tabindex="-1" aria-labelledby="changeTicket'+ response.id +'Statuses" aria-hidden="true">'+
                                            '<div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">'+
                                                '<div class="modal-content">'+
                            
                                                    '<div class="modal-header">'+
                                                        '<h1 class="modal-title fs-5" id="changeTicket'+ response.id +'StatusesHeader">Изменить статусы</h1>'+
                                                        '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'+
                                                    '</div>'+
                            
                                                    '<div class="modal-body">'+
                                                        '<form id="add_ticket_statuses">'+
                                                            // {% csrf_token %}
                
                                                            '<div class="row mb-3">'+
                                                                '<div class="col-8">'+
                                                                    '<label for="ticket_types">Тип заявки</label>'+
                                                                    '<select class="form-select" name="ticket_types" id="id_ticket_types_'+ response.id +'">'+
                                                                    '</select>'+
                                                                '</div>'+
                                                                '<div class="col-4 mt-auto d-grid">'+
                                                                    '<button onclick=\'send_ticket_status_agreement("id_ticket_types_'+ response.id +'", "'+ response.id +'", "send_act_types_'+ response.id +'", "data_ticket_types_'+ response.id +'")\' id="send_act_types_'+ response.id +'" type="button" data-url="/update/ticket_type/'+ response.id +'" class="btn btn-success">'+
                                                                        'Отправить'+
                                                                    '</button>'+
                                                                '</div>'+
                                                            '</div>'+
                
                                                            '<div class="row mb-3">'+
                                                                '<div class="col-8">'+
                                                                    '<label for="ticket_statuses">Статус заявки</label>'+
                                                                    '<select class="form-select" name="ticket_statuses" id="id_ticket_statuses_'+ response.id +'">'+
                                                                    '</select>'+
                                                                '</div>'+
                                                                '<div class="col-4 mt-auto d-grid">'+
                                                                    '<button onclick=\'send_ticket_status_agreement("id_ticket_statuses_'+ response.id +'", "'+ response.id +'", "send_act_statuses_'+ response.id +'", "data_ticket_statuses_'+ response.id +'")\' id="send_act_statuses_'+ response.id +'" type="button" data-url="/update/ticket_status/'+ response.id +'" class="btn btn-success">Отправить</button>'+
                                                                '</div>'+
                                                            '</div>'+
                
                                                        '</form>'+
                                                        '<div id="ticket_statuses_messages_'+ response.id +'"></div>'+
                                                    '</div>'+
                                                    
                                                    '<div class="modal-footer">'+
                                                        '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>'+
                                                    '</div>'+
                                                '</div>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>'+
                '</div>'
            );

            document.getElementById('id_ticket_types_'+ response.id).innerHTML = type_data
            document.getElementById('id_ticket_statuses_'+ response.id).innerHTML = status_data
        }

        if(document.getElementById('ticket-table-body')){
            var date_td = new Date();
            if(result[4][1]){
                date_td = new Date(result[4][1]).toLocaleDateString("fr-CH")
            }
            else{
                date_td = new Date(date_td.getFullYear(), date_td.getMonth() + 1, 0).toLocaleDateString("fr-CH")
            }
            var e = document.getElementById("agreement");
            document.getElementById('ticket-table-body').insertAdjacentHTML('afterbegin',
                '<tr class="position-relative table-success">'+
                    '<td><a class="stretched-link" href="/ticket/'+ response.id +'">'+ response.id +'</a></td>'+
                    '<td>'+ e.options[e.selectedIndex].text +'</td>'+
                    '<td> - </td>'+
                    '<td> - </td>'+
                    '<td>'+ result[2][1] +'</td>'+
                    '<td>'+ result[3][1] +'</td>'+
                    '<td>'+ date_td +'</td>'+
                '</tr>'
            );
        }

        document.getElementById("add_ticket").reset();
    }
}