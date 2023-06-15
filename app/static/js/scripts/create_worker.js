
document.getElementById('send_worker').addEventListener('click',  async () => await create_worker())


async function create_worker(){
    url = document.getElementById('send_worker').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_worker');
    var data = JSON.stringify(Object.fromEntries(new FormData(form)));

    var schema = JSON.parse(data)
    var result = [];
    for(var i in schema)
        result.push([i, schema [i]]);

    var empty_is = false;

    if(result[0][1].length === 0 || result[1][1].length === 0 || result[2][1].length === 0 || result[4][1].length === 0 || result[5][1].length === 0){
        var empty_is = true;
    }

    if (empty_is){
        document.getElementById('worker_messages').insertAdjacentHTML('afterbegin', 
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
            document.getElementById('worker_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });
    
        document.getElementById('worker_messages').insertAdjacentHTML('afterbegin','<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addWorker');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
            
            if(document.getElementById("no-data")){
                document.getElementById('no-data').remove();
            }

            if(document.getElementById('worker-table-body')){
                var position = document.getElementsByClassName("select-position-form")[0];
                document.getElementById('worker-table-body').insertAdjacentHTML('afterbegin',
                    '<tr class="table-success">'+
                        '<th scope="row">'+ result[1][1]+' '+result[2][1] +' '+ result[3][1] +'</th>'+
                        '<td>'+ result[5][1] +'</td>'+
                        '<td>'+ result[6][1] +'</td>'+
                        '<td>'+ position.options[position.selectedIndex].text +'</td>'+
                        '<td class="text-center">'+
                            '<a href="/user/update/'+ response.id +'">'+
                                '<img src="/static/icons/update.svg" style="width: 18px;">'+
                            '</a>'+
                        '</td>'+
                    '</tr>'
                );
            }

            document.getElementById("add_worker").reset();
        }
    }
}