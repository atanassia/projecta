
document.getElementById('send_act').addEventListener('click',  async () => await create_act())


async function create_act(){
    url = document.getElementById('send_act').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_act');
    var data = JSON.stringify(Object.fromEntries(new FormData(form)));

    var schema = JSON.parse(data)
    var result = [];
    for(var i in schema)
        result.push([i, schema [i]]);
    
    var empty_is = false;

    if(result[0][1].length === 0 || result[1][1].length === 0 || result[2][1].length === 0 || result[3][1].length === 0 || result[5][1].length === 0 || result[6][1].length === 0){
        var empty_is = true;
    }

    if (empty_is){
        document.getElementById('act_messages').insertAdjacentHTML('afterbegin', 
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
            document.getElementById('act_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });

        document.getElementById('act_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addAct');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
            
            if(document.getElementById("no-data")){
                document.getElementById('no-data').remove();
            }
            
            document.getElementById('act_messages').replaceChildren();
            var no_null_act = document.getElementById('no-acts')

            if(document.getElementById('act-table-body')){
                document.getElementById('act-table-body').insertAdjacentHTML('afterbegin',
                    '<tr class="position-relative table-success">'+
                        '<td scope="row">'+ '№'+ result[1][1]+' - '+'" ----- "'+'</a>'+
                        '</td>'+
                        '<td>'+ result[2][1] +'</td>'+
                        '<td>'+ result[3][1] +'</td>'+
                        '<td>'+ result[4][1] +'</td>'+
                        '<td>'+ result[5][1] +'</td>'+
                        '<td>'+ new Date(result[6][1]).toLocaleDateString("fr-CH") +'</td>'+
                    '</tr>'
                );
            }

            if(no_null_act != null){
                no_null_act.remove()
            }
            
            if(document.getElementById('act_row')){
                document.getElementById('act_row').insertAdjacentHTML('afterbegin',
                    '<div class="col mt-3">'+
                        '<div class="card ">'+
                            '<div class="card-header text-bg-success">'+
                                '<div class="d-flex p-2">'+
                                    '<div><strong>Акт №'+result[2][1]+'</strong></div>'+
                                    '<div class="ms-auto"><span class="badge text-bg-dark text-end">'+ result[3][1] +'</span></div>'+
                                '</div>'+
                            '</div>'+
                            '<div class="card-body">'+
                                '<div class="card-text">'+
                                    '<ul class="list-group-flush">'+
                                        '<li><strong>Номер счёта</strong> - '+ result[4][1] +'</li>'+
                                        '<li><strong>Статус счёта</strong> - '+ result[5][1] +'</li>'+
                                        '<li><strong>Дата</strong> - '+ new Date(result[6][1]).toLocaleDateString("ru-RU") +'</li>'+
                                        '<li><strong>Обновлено</strong> - '+ new Date().toLocaleString("ru-RU").slice(0, -3) +'</li>'+
                                        '<li><strong>Автор</strong> - '+ document.getElementById('usersname').getAttribute('data-value') +'</li>'+
                                    '</ul>'+
                                    '<div class="d-flex">'+
                                        '<div class="ms-auto">'+
                                            '<a href="/act/update/'+ response.id +'" title="Обновить акт" class="me-2">'+
                                                '<img src="/static/icons/update.svg" style="width: 18px;">'+
                                            '</a>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                        '</div>'+
                    '</div>'
                );
            }

            document.getElementById("add_act").reset();
        }
    }
}