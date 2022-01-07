document.getElementById('paymentType-1').addEventListener('click', ()=> {
    var element = document.getElementById('creditInfo');
    element.classList.remove('d-none');
});

document.getElementById('paymentType-0').addEventListener('click', ()=> {
    console.log('click pament credit')
    var element = document.getElementById('creditInfo');
    element.classList.add('d-none');
});

function getShippingFee(originalTotalAmount) {
    var amount = +(originalTotalAmount.slice(1));
    return (Math.round((amount * 0.05)*100)/100).toString();
}

function getNewTotalAmount(originalTotalAmount, fee, discount) {
    var d = 0;
    if (discount != null) {
        d = +(discount.slice(1, -1))
    }
    var a = +(originalTotalAmount.slice(1));
    var f = +(fee);
    return (Math.round(((a+f) * (1-d/100))*100)/100).toString();
}

let originalTotalAmount = document.getElementById('subTotal').getElementsByTagName('strong')[0].innerText;
let shippingFee = document.getElementById('shippingFee').getElementsByTagName('span')[0];
let discount = document.getElementById('discount');

var fee = 0;
if (shippingFee.innerText !== '$0') {
    fee = getShippingFee(originalTotalAmount);
    shippingFee.innerText = "$" + fee;
}

if (discount !== null) {
    discount = discount.getElementsByTagName('span')[0].innerText;
}

let newTotalAmount = getNewTotalAmount(originalTotalAmount, fee, discount);

document.getElementById('totalAmount').getElementsByTagName('strong')[0].innerText = "$" + newTotalAmount;
