btn = document.getElementById("clean")
btn.addEventListener('click', () => {
    document.querySelectorAll('.form-control').forEach((item) =>{
        item.value = ''
    })
})