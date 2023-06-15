document.getElementById('send_agreement').addEventListener('click',  async () => await create_agreement())


async function create_agreement(){
    url = document.getElementById('send_agreement').dataset.url
    csrf_token = document.querySelector('input[name="csrfmiddlewaretoken"]').value

    var form = document.getElementById('add_agreement');
    var data = JSON.stringify(Object.fromEntries(new FormData(form)));

    var schema = JSON.parse(data)
    var result = [];

    for(var i in schema)
        result.push([i, schema [i]]);
    
    var empty_is = false;

    if(result[1][1].length === 0 || result[3][1].length === 0 || result[6][1].length === 0 || result[7][1].length === 0){
        empty_is = true;
    }

    var selects = document.getElementById("id_responsible");
    var selectedText = selects.options[selects.selectedIndex].text
    if (empty_is){
        document.getElementById('agreement_messages').insertAdjacentHTML('afterbegin', 
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
            document.getElementById('agreement_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-danger alert-dismissible fade show" role="alert">Что-то пошло не так, попробуйте позже.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>');
        });

        document.getElementById('agreement_messages').insertAdjacentHTML('afterbegin', '<div class="alert alert-' + response.status + ' alert-dismissible fade show" role="alert">' + response.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>')
        
        if (status == 201){
            await new Promise(r => setTimeout(r, 1000));
            var myModalEl = document.getElementById('addAgreement');
            var modal = bootstrap.Modal.getInstance(myModalEl)
            modal.hide();
    
            if(document.getElementById("no-data")){
                document.getElementById('no-data').remove();
            }

            if(document.getElementById('agreement-table-body')){
                document.getElementById('agreement-table-body').insertAdjacentHTML('afterbegin',
                    '<tr class="position-relative table-success">'+
                        '<td scope="row">'+
                            '<a class="stretched-link" href="/agreement/'+response.id+'">'+ '№'+ result[1][1]+' - '+'"-"'+'</a>'+
                        '</td>'+
                        '<td>'+ result[3][1] +'</td>'+
                        '<td>'+ result[4][1] +'</td>'+
                        '<td>'+ result[8][1] +'</td>'+
                        '<td>'+ result[10][1] +'</td>'+
                        '<td>'+ new Date(result[6][1]).toLocaleDateString("fr-CH") +'</td>'+
                        '<td>'+ new Date(result[7][1]).toLocaleDateString("fr-CH") +'</td>'+
                    '</tr>'
                );
            }

            document.getElementById('agreement_messages').replaceChildren();

            var no_null_agreements = document.getElementById('no-agreements');
            if(no_null_agreements != null){
                no_null_agreements.remove();
            }

            if(document.getElementById('agreements_row')){
                document.getElementById('agreements_row').insertAdjacentHTML('afterbegin',
                    '<div class="col mt-3">'+
                    '<div class="card">'+
        
                    '<div class="card-header text-bg-success">'+
                        '<div class="d-flex p-2">'+
                        '<div>'+
                            '<strong>Договор №'+ result[2][1] +'</strong>'+
                        '</div>'+
                        '<div class="ms-auto"><span class="badge text-bg-dark text-end">'+ result[4][1] +'</span></div>'+
                        '</div>'+
                    '</div>'+
        
                    '<div class="card-body">'+
                        '<div class="card-text">'+
                        '<ul class="list-group-flush">'+
                            '<li><strong>Адрес</strong> - '+ result[3][1] +'</li>'+
                            '<li><strong>Ответственный</strong> - '+ selectedText +'</li>'+
                            '<li>От <strong>'+ new Date(result[6][1]).toLocaleDateString("fr-CH") +'</strong> до <strong>'+ new Date(result[7][1]).toLocaleDateString("fr-CH") +'</strong></li>'+
                        '</ul>'+
                        '</div>'+
        
                        '<div class="d-flex">'+
                        '<a class="btn btn-dark btn-sm ms-auto" href="/agreement/'+ response.id +'" role="button">Подробнее</a>'+
                    '</div>'+
                    '</div>'+
                    '</div>'+
                '</div>'
                );
            }

            document.getElementById("add_agreement").reset();
        }
    }

}