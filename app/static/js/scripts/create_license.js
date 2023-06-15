document.getElementById('send_license').addEventListener('click',  async () => await create_license())

async function create_license(){
    url = document.getElementById('send_license').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_license');
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
        document.getElementById('license_messages').insertAdjacentHTML('afterbegin', 
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
            document.getElementById('license_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });
        
        document.getElementById('license_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addLicense');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
    
            document.getElementById("add_license").reset();
            document.getElementById('license_messages').replaceChildren();

            var no_null_license = document.getElementById('no-license')
            if(no_null_license != null){
                no_null_license.remove();
            }

            document.getElementById('license_row').insertAdjacentHTML('afterbegin',
                '<div class="col mt-2">'+
                    '<div class="card">'+
                        '<div class="card-body">'+
                        '<span class="position-absolute top-0 start-50 translate-middle badge rounded-pill bg-success">Новая запись</span>'+
                            '<div class="d-flex">'+
                                '<h6 class="card-subtitle mb-2 text-muted">Дата регистрации - '+ new Date(result[1][1]).toLocaleDateString("fr-CH") +'</h6>'+
                                '<div class="ms-auto">'+
                                    '<a href="/license/update/'+ response.id +'" title="Обновить данные лицензии" class="me-2">'+
                                        '<img src="/static/icons/update.svg" style="width: 18px;">'+
                                    '</a>'+
                                '</div>'+
                            '</div>'+
                            '<p class="card-text">Номер лицензии: '+result[2][1]+'<br>Класс опасности: '+result[3][1]+'</p>'+
                        '</div>'+
                    '</div>'+
                '</div>'
            );
        }
    }
}