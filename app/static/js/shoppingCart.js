document.getElementById('credit').addEventListener('click', ()=> {
    var element = document.getElementById('creditInfo');
    element.classList.remove('d-none');
});

document.getElementById('cash').addEventListener('click', ()=> {
    console.log('click pament credit')
    var element = document.getElementById('creditInfo');
    element.classList.add('d-none');
});

function getShippingFee(originalTotalAmount) {
    var amount = +(originalTotalAmount.slice(1, originalTotalAmount.length));
    return (amount * 0.05).toString();
}

function getNewTotalAmount(originalTotalAmount, fee) {
    var a = +(originalTotalAmount.slice(1, originalTotalAmount.length));
    var f = +(fee);
    return (a+f).toString();
}

let originalTotalAmount = document.getElementById('amount').getElementsByTagName('strong')[0].innerText;
let fee = getShippingFee(originalTotalAmount)
let newTotalAmount = getNewTotalAmount(originalTotalAmount, fee)

document.getElementById('shippingFee').getElementsByTagName('span')[0].innerText = "$" + fee;

document.getElementById('amount').getElementsByTagName('strong')[0].innerText = "$" + newTotalAmount;
