let quantity = 1; // Початкова кількість

function incrementQuantity() {
        if (quantity < 10) {
        quantity++;
        updateDisplay()
    }
}

function decrementQuantity() {
    if (quantity > 1) {
        quantity--;
        updateDisplay()
    }
}

function updateDisplay() {
    let displays = document.getElementsByClassName("quantity-display");
    Array.from(displays).forEach(function(display) {
        display.textContent = quantity;
    });
    document.getElementById("total-price").textContent = calculateTotal();
}