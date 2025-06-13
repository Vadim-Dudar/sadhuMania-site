// === Глобальна змінна для контексту модалки ===
let modalContext = null;



// === ФУНКЦІЯ ЗАКРИТТЯ МОДАЛКИ ===
function closeModal() {
    const modalIds = [
        "addEng", "deleteItem", "addCarousel", "editSite", "addCategory",
        "formReport", "addExpense", "addAvailability", "addProduct", "addOrder"
    ];
    for (let id of modalIds) {
        const el = document.getElementById(id);
        if (el) el.style.display = "none";
    }
    document.getElementById("openMenu").style.display = "block";
    document.body.classList.remove('body-frozen');
    modalContext = null; // очищаємо контекст при закритті
}
