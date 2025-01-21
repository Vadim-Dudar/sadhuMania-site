// function closeModal(){
//     document.getElementById("custom-confirm").style.display = "none";
//     document.body.classList.remove('body-frozen');
// }

// function sendModal(){
//     validateInput() && handleOrder(); // �������� ���� ����� �����������
// }

// function openModal(){
//     document.getElementById("custom-confirm").style.display = "flex";
//     document.getElementById("total-price").textContent = calculateTotal();
//     document.body.classList.add('body-frozen');
//     document.getElementById("modalFoto").src = document.querySelector("#carousel-1 .carousel-item img").src;
// }

// function calculateTotal(){
//     const priceEngraving = 200;

//     let priceOfWare = parseFloat(document.getElementById("price-for-each").textContent || 0);
//     let quantity = parseInt(document.getElementsByClassName("quantity-display")[0].textContent || 0);

//     if(document.getElementById("engraving-select").value == "1"){
//         return priceOfWare * quantity; 
//     }else{
//         return (priceOfWare + priceEngraving) * quantity;
//     }
// }

// document.getElementById("engraving-select").addEventListener("change", function (){
//     document.getElementById("total-price").textContent = calculateTotal();
// });

// function validateInput() {
//     let isValid = true;
//     const inputs = document.querySelectorAll('#name-input, #surname-input, #phone-input, #address-input, #post-input'); // �������� ��� ���������� ����
//     inputs.forEach(input => {
//         if (input.value.trim() === '') {
//             input.classList.add('error');
//             document.querySelector('.row .col input').closest('.row').querySelector('.col span').style.color = 'red';
//             isValid = false;
//         } else {
//             input.classList.remove('error');
//         }
//     });
//     return isValid;
// }

// function handleOrder() {
//     if (!validateInput()) return; // �������� �������� ����
    
//     const name = document.getElementById('name-input').value.trim();
//     const surname = document.getElementById('surname-input').value.trim();
//     const phone = document.getElementById('phone-input').value.trim();
//     const address = document.getElementById('address-input').value.trim();
//     const post = document.getElementById('post-input').value.trim();
//     const engraving = document.getElementById('engraving-select').value;
//     const quantity = document.getElementsByClassName('quantity-display')[0].textContent.trim();
//     const manager = document.getElementById('manager-check').checked; // �������� �� ������� ��������
//     const comentar = document.getElementById('comentar-area').value.trim();

//     const deviceInfo = {
//         platform: navigator.platform,
//         userAgent: navigator.userAgent,
//         screenWidth: window.screen.width,
//         screenHeight: window.screen.height
//     };

//     const orderData = JSON.stringify({
//         name,
//         surname,
//         phone,
//         address,
//         post,
//         engraving,
//         quantity,
//         manager,
//         comentar,
//         deviceInfo
//     }, null, 4);

//     console.log(orderData);
// }


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
    document.getElementById("modalFoto").src = document.querySelector("#carousel-1 .carousel-item img").src;
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
    }, null, 4);

    console.log(orderData);
}
