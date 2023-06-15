document.getElementById('send_insurance_policy').addEventListener('click',  async () => await create_insurance_policy())

async function create_insurance_policy(){
    url = document.getElementById('send_insurance_policy').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_insurance_policy');
    var data = JSON.stringify(Object.fromEntries(new FormData(form)));

    var schema = JSON.parse(data)
    var result = [];
    for(var i in schema)
        result.push([i, schema [i]]);
    
    var empty_is = false;

    for(var i in result){
        if(result[i][1].length === 0){
            var empty_is = true;
        }
    }

    if (empty_is){
        document.getElementById('insurance_policy_messages').insertAdjacentHTML('afterbegin', 
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
            document.getElementById('insurance_policy_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });
        
        document.getElementById('insurance_policy_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addInsurancePolicy');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();

            if(document.getElementById("no-data")){
                document.getElementById('no-data').remove();
            }
    
            document.getElementById('insurance_policy_messages').replaceChildren();

            if(document.getElementById('policy-table-body')){
                document.getElementById('policy-table-body').insertAdjacentHTML('afterbegin',
                    '<tr class="position-relative table-success">'+
                        '<td scope="row">'+ '№'+' " ----- "'+' - '+'" ----- "'+
                        '</td>'+
                        '<td>'+ result[2][1] +'</td>'+
                        '<td>'+ new Date(result[3][1]).toLocaleDateString("fr-CH") +'</td>'+
                        '<td>'+ new Date(result[4][1]).toLocaleDateString("fr-CH") +'</td>'+
                        '<td class="text-center">-----</td>'+
                    '</tr>'
                );
            }

            if(document.getElementById('insurance_policy_row')){
                var no_null_insurances = document.getElementById('no-insurance_policies');
                if(no_null_insurances != null){
                    no_null_insurances.remove();
                }
                document.getElementById('insurance_policy_row').insertAdjacentHTML('afterbegin',
                    '<div class="col mt-3" id="insurance_policy_card_'+ response.id +'">'+
                        '<div class="card">'+
                            '<div class="card-header text-bg-success">'+
                                '<div class="d-flex p-2">'+
                                    '<div><strong>Страховой полис от "'+ result[2][1] +'"</strong></div>'+
                                '</div>'+
                            '</div>'+
    
                            '<div class="card-body">'+
                                '<div class="card-text">'+
                                    '<ul class="list-group-flush">'+
                                        '<li><strong>Дата начала</strong> - '+ new Date(result[3][1]).toLocaleDateString("fr-CH") +'</li>'+
                                        '<li><strong>Дата завершения</strong> - '+ new Date(result[4][1]).toLocaleDateString("fr-CH") +'</li>'+
                                    '</ul>'+
                                '</div>'+
                                '<div class="d-flex">'+
                                    '<div class="ms-auto">'+
                                        '<a href="/insurance_policy/update/'+ response.id +'" title="Обновить страховой полис" class="me-2">'+
                                            '<img src="/static/icons/update.svg" style="width: 18px;">'+
                                        '</a>'+
                                        '<button type="button" class="btn" style="padding:0;" title="Удалить страховой полис" data-bs-toggle="modal" data-bs-target="#modalContact'+ response.id +'">'+
                                            '<img src="/static/icons/delete.svg" style="width: 18px;">'+
                                        '</button>'+
                                    '</div>'+
                                    '<div class="modal fade" id="modalContact'+ response.id +'" tabindex="-1" aria-labelledby="'+ response.id +'Label" aria-hidden="true">'+
                                        '<div class="modal-dialog">'+
                                            '<div class="modal-content">'+
                                                '<div class="modal-header">'+
                                                    '<h1 class="modal-title fs-5" id="'+ response.id +'Label">Точно хотите удалить страховой полис?</h1>'+
                                                    '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'+
                                                '</div>'+
                                                '<div class="modal-body">'+
                                                    '<h5 class="card-title fw-bold me-auto">'+ result[2][1] +'</h5>'+
                                                    '<li><strong>Дата начала</strong> - '+ new Date(result[3][1]).toLocaleDateString("fr-CH") +'</li>'+
                                                    '<li><strong>Дата завершения</strong> - '+ new Date(result[3][1]).toLocaleDateString("fr-CH") +'</li>'+
                                                '</div>'+
            
                                                '<div class="modal-footer">'+
                                                    '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>'+
                                                    '<!-- это не ошибка, по-другому переменную эту туда не загнать -->'+
                                                    '<button onclick="delete_insurance_policy_func(\'/delete/insurance_policy/'+ response.id +'\', \'insurance_policy_card_'+ response.id +'\')" id="delete_insurance_policy" type="button" class="btn btn-danger" data-bs-dismiss="modal">Удалить</button>'+
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
    
            document.getElementById("add_insurance_policy").reset();
        }
    
    }
}