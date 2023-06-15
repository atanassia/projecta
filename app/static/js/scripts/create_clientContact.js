
document.getElementById('send_contact').addEventListener('click',  async () => await create_contact())


async function create_contact(){
    url = document.getElementById('send_contact').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_conatct');
    var data = JSON.stringify(Object.fromEntries(new FormData(form)));
    
    var schema = JSON.parse(data)
    var result = [];
    for(var i in schema)
        result.push([i, schema [i]]);

    var empty_is = false;
    if(result[2][1].length === 0 || result[3][1].length === 0 || result[4][1].length === 0){
        var empty_is = true;
    }

    if (empty_is){
        document.getElementById('contact_messages').insertAdjacentHTML('afterbegin', 
                '<div class="alert alert-danger alert-dismissible fade show" role="alert">Заполните пустые поля!<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
    }else{
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
            document.getElementById('contact_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });
    
        document.getElementById('contact_messages').insertAdjacentHTML('afterbegin','<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addClientContact');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
    
            document.getElementById("add_conatct").reset();
            document.getElementById('contact_messages').replaceChildren();

            var no_null_contacts = document.getElementById('no-contacts');
            if(no_null_contacts != null){
                no_null_contacts.remove();
            }

            if(result[5][1]){
                var email_and_phone = 
                '<div>'+
                    '<img src="/static/icons/phone.svg" class="me-2" style="width: 15px;">'+
                    result[4][1]+
                '</div>'+
                '<div>'+
                    '<img src="/static/icons/email.svg" class="me-2" style="width: 15px;">'+
                    result[5][1]+
                '</div>'
            }else{
                var email_and_phone = 
                '<div>'+
                    '<img src="/static/icons/phone.svg" class="me-2" style="width: 15px;">'+
                    result[4][1]+
                '</div>'
            }

            document.getElementById('contacts_row').insertAdjacentHTML('afterbegin',
                '<div class="col mt-3" id="contact_card_'+ response.id +'">'+
                    '<div class="card h-100">'+
                    '<div class="card-body">'+
                    '<span class="position-absolute top-0 start-50 translate-middle badge rounded-pill bg-success">Новая запись</span>'+
                        '<div class="d-flex justify-content-between align-items-start">'+
                        '<h5 class="card-title fw-bold me-auto">'+ result[2][1] +'</h5>'+
                        '<span class="badge bg-dark rounded-pill" title="Приоритет контакта">'+ result[3][1] +'</span>'+
                        '</div>'+
                        '<div class="card-text">'+
                        '<li class="list-group-item">'+
                            '<div class="ms-2 me-auto">'+
                                email_and_phone+ 
                            '</div>'+
                        '</li>'+
                        '<div class="d-flex">'+
                            '<div class="ms-auto">'+

                                '<a href="/contacts/update/'+ response.id +'" title="Обновить контакт" class="me-2">'+
                                    '<img src="/static/icons/update.svg" style="width: 18px;">'+
                                '</a>'+

                                '<button type="button" class="btn" style="padding:0;" title="Удалить контакт" data-bs-toggle="modal" data-bs-target="#modalContact'+ response.id +'">'+
                                    '<img src="/static/icons/delete.svg" style="width: 18px;">'+
                                '</button>'+
                            
                            '</div>'+

                            '<div class="modal fade" id="modalContact'+ response.id +'" tabindex="-1" aria-labelledby="'+ response.id +'Label" aria-hidden="true">'+
                            '<div class="modal-dialog">'+
                                '<div class="modal-content">'+
                                '<div class="modal-header">'+
                                    '<h1 class="modal-title fs-5" id="'+ response.id +'Label">Точно хотите удалить контакт?</h1>'+
                                    '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'+
                                '</div>'+
                                '<div class="modal-body">'+
                                    '<h5 class="card-title fw-bold me-auto">'+ result[2][1] +'</h5>'+
                                    '<li class="list-group-item">'+
                                    '<div class="ms-2 me-auto">'+
                                        email_and_phone+
                                    '</div>'+
                                    '</li>'+
                                '</div>'+

                                '<div class="modal-footer">'+
                                    '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>'+
                                    '<button onclick="delete_contact_func(\'/delete/contact/' + response.id + '\', \'contact_card_'+ response.id +'\')" id="delete_contact" type="button" class="btn btn-danger"'+
                                        'data-bs-dismiss="modal">Удалить</button>'+
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
        }
    
    }

}