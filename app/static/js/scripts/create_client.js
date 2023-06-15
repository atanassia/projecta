
document.getElementById('send_client').addEventListener('click',  async () => await create_client())


async function create_client(){
    url = document.getElementById('send_client').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_client');
    var data = JSON.stringify(Object.fromEntries(new FormData(form)));
    
    var schema = JSON.parse(data)
    var result = [];
    for(var i in schema)
        result.push([i, schema [i]]);
    
    var empty_is = false;
    if(result[1][1].length === 0 || result[4][1].length === 0 || result[8][1].length === 0){
        var empty_is = true;
    }

    if (empty_is){
        document.getElementById('client_messages').insertAdjacentHTML('afterbegin', 
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
            document.getElementById('client_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });
    
        document.getElementById('client_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addClient');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
            
            if(document.getElementById("no-data")){
                document.getElementById('no-data').remove();
            }

            document.getElementById('client-table-body').insertAdjacentHTML('afterbegin',
                '<tr class="position-relative table-success">'+
                    '<td scope="row">'+
                        '<a class="stretched-link" href="/client/'+response.id+'">'+ result[3][1]+' "'+result[4][1]+'"'+'</a>'+
                    '</td>'+
                    '<td>'+ result[1][1] +'</td>'+
                    '<td>'+ result[2][1] +'</td>'+
                    '<td>'+ result[6][1] +'</td>'+
                    '<td>'+ result[8][1] +'</td>'+
                    '<td>'+ result[9][1] +'</td>'+
                '</tr>'
            );

            document.getElementById("add_client").reset();
        }
    }

}