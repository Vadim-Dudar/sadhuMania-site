function closeModal(){
    document.getElementById("custom-confirm").style.display = "none";
    document.body.classList.remove('body-frozen');
}

function sendModal(){
    if (validateInput()) {
        handleOrder();
        closeModal(); // ��������� �������� ����, ���� ���� ������ �� ���������� ���������
    }
}

function openModal(){
    document.getElementById("custom-confirm").style.display = "flex";
    document.getElementById("total-price").textContent = calculateTotal();
    document.body.classList.add('body-frozen');
}

function calculateTotal(){
    const priceEngraving = 200;
    let priceOfWare = parseFloat(document.getElementById("price-for-each").textContent || 0);
    let quantity = parseInt(document.getElementsByClassName("quantity-display")[0].textContent || 0);

    if(document.getElementById("engraving-select").value === "1"){
        return priceOfWare * quantity; 
    } else {
        return (priceOfWare + priceEngraving) * quantity;
    }
}

document.getElementById("engraving-select").addEventListener("change", function (){
    document.getElementById("total-price").textContent = calculateTotal();
});

function validateInput() {
    const inputs = document.querySelectorAll('#name-input, #surname-input, #phone-input, #address-input, #post-input');
    let isValid = true;
    inputs.forEach(input => {
        const label = input.closest('.col').previousElementSibling.querySelector('span');
        if (input.value.trim() === '') {
            input.classList.add('error');
            label.classList.add('error-text');
            isValid = false;
        } else {
            input.classList.remove('error');
            label.classList.remove('error-text');
        }
    });
    return isValid;
}

function handleOrder() {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    const name_of_product = document.getElementById('productName').textContent;
    const name = document.getElementById('name-input').value.trim();
    const surname = document.getElementById('surname-input').value.trim();
    const phone = document.getElementById('phone-input').value.trim();
    const address = document.getElementById('address-input').value.trim();
    const post = document.getElementById('post-input').value.trim();
    const engraving = document.getElementById('engraving-select').value;
    const quantity = parseInt(document.getElementsByClassName('quantity-display')[0].textContent.trim());
    const manager = document.getElementById('manager-check').checked;
    const comment = document.getElementById('comentar-area').value.trim();

    const deviceInfo = {
        platform: navigator.platform,
        userAgent: navigator.userAgent,
        screenWidth: window.screen.width,
        screenHeight: window.screen.height
    };

    const orderData = JSON.stringify({
        name_of_product,
        name,
        surname,
        phone,
        address,
        post,
        engraving,
        quantity,
        manager,
        comment,
        deviceInfo
    });

    console.log(orderData);

    fetch('/create-order/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            name_of_product,
            name,
            surname,
            phone,
            address,
            post,
            engraving,
            quantity,
            manager,
            comment,
            deviceInfo
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('Замовлення успішно створено!');
        } else {
            alert('Помилка: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Помилка:', error);
    });

}
