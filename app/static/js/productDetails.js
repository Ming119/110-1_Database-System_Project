function quantityStepUp(node) {
    node.parentNode.parentNode.querySelector('input[type=number]').stepUp();
}

function quantityStepDown(node) {
    quantity = node.parentNode.parentNode.querySelector('input[type=number]').value;
    if (quantity > 0) {
        node.parentNode.parentNode.querySelector('input[type=number]').stepDown();
    }
}
