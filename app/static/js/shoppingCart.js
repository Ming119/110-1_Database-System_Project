document.getElementById('credit').addEventListener('click', ()=> {
    var element = document.getElementById('creditInfo');
    element.classList.remove('d-none');
});

document.getElementById('cash').addEventListener('click', ()=> {
    console.log('click pament credit')
    var element = document.getElementById('creditInfo');
    element.classList.add('d-none');
});
