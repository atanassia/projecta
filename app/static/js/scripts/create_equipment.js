
document.getElementById('send_equipment').addEventListener('click',  async () => await create_equipment())

async function create_equipment(){
    url = document.getElementById('send_equipment').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_equipment');
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
        document.getElementById('equipment_messages').insertAdjacentHTML('afterbegin', 
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
            document.getElementById('equipment_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });
        
        document.getElementById('equipment_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addEquipment');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();

            if(document.getElementById("no-data")){
                document.getElementById('no-data').remove();
            }
    
            document.getElementById('equipment_messages').replaceChildren();

            if(document.getElementById('equipment-table-body')){
                document.getElementById('equipment-table-body').insertAdjacentHTML('afterbegin',
                    '<tr class="position-relative table-success">'+
                        '<td scope="row">'+ '№'+ result[1][1]+' - '+'" ----- "'+'</a>'+
                        '</td>'+
                        '<td>'+ result[2][1] +'</td>'+
                        '<td>'+ result[6][1] +'</td>'+
                        '<td class="text-center">'+ result[3][1] +'</td>'+
                        '<td class="text-center">'+ new Date(result[4][1]).toLocaleDateString("fr-CH") +' - '+ new Date(result[5][1]).toLocaleDateString("fr-CH") +'</td>'+
                    '</tr>'
                );
            }
            
            if(document.getElementById('equipment_row')){
                var no_null_equipment = document.getElementById('no-equipment')
                if(no_null_equipment != null){
                    no_null_equipment.remove();
                }
                document.getElementById('equipment_row').insertAdjacentHTML('afterbegin',
                '<div class="col mt-3" id="equipment_card_' + response.id + '"> <div class="card"> <div class="card-body">'+
                '<span class="position-absolute top-0 start-50 translate-middle badge rounded-pill bg-success">Новая запись</span>'+
                '<div class="d-flex">'+
                    '<div><strong>'+ result[2][1] +'</strong></div>'+
                        '<div class="ms-auto">'+
                            '<a href="/equipment/update/' + response.id + '" title="Обновить данные оборудования" class="me-2">'+
                                '<img src="/static/icons/update.svg" style="width: 18px;">' +
                            '</a>' +
                                    
                            '<button type="button" class="btn" style="padding:0;" title="Удалить оборудование" data-bs-toggle="modal" data-bs-target="#modalEquipment'+ response.id +'">'+
                            '<img src="/static/icons/delete.svg" style="width: 18px;"></button></div>'+

                                '<div class="modal fade" id="modalEquipment'+ response.id +'" tabindex="-1" aria-labelledby="'+ response.id +'EquipmentLabel" aria-hidden="true">'+
                                    '<div class="modal-dialog">'+
                                        '<div class="modal-content">'+
                                            '<div class="modal-header">'+
                                                '<h1 class="modal-title fs-5" id="'+ response.id +'EquipmentLabel">Точно хотите удалить оборудование?</h1>'+
                                                '<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>'+
                                            '</div>'+

                                            '<div class="modal-body">'+
                                                '<h5 class="card-title fw-bold me-auto">'+ result[2][1] +'</h5>'+
                                                '<li class="list-group-item">'+
                                                    '<div class="ms-2 me-auto">'+
                                                        'Количество - ' + result[3][1] +
                                                    '</div>'+
                                                '</li>'+
                                            '</div>'+
                
                                            '<div class="modal-footer">'+
                                                '<button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>'+
                                                
                                                '<button onclick="delete_equipment_func(\'/delete/equipment/'+ response.id +'\', \'equipment_card_'+ response.id +'\')"'+
                                                    'id="delete_equipment" type="button" class="btn btn-danger" data-bs-dismiss="modal">'+
                                                    'Удалить'+
                                                '</button>'+
                                            '</div>'+
                                        '</div>'+
                                    '</div>'+
                                '</div>'+
                            '</div>'+
                            '<h6 class="card-subtitle mb-2 mt-1">От <strong>'+ new Date(result[4][1]).toLocaleDateString("fr-CH") +'</strong> до <strong>'+ new Date(result[5][1]).toLocaleDateString("fr-CH") +'</strong></h6>'+
                            '<h6 class="card-subtitle mb-2 text-muted">Количество: '+ result[3][1] +'</h6>'+
                            '<div class="card-text">'+
                                    result[6][1]+
                            '</div>'+
                        '</div>'+
                    '</div>'+
                '</div>'
                );
            }

            document.getElementById("add_equipment").reset();
        }
    }  
}