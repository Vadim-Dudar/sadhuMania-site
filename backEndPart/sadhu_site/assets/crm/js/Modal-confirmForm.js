function closeModal(){

    //edit eng
    const addEng = document.getElementById("addEng");
    if (addEng) addEng.style.display = "none";

    // edit site
    const deleteItem = document.getElementById("deleteItem");
    if (deleteItem) deleteItem.style.display = "none";

    const addCarousel = document.getElementById("addCarousel");
    if (addCarousel) addCarousel.style.display = "none";

    const editSite = document.getElementById("editSite");
    if (editSite) editSite.style.display = "none";

    const addCategory = document.getElementById("addCategory");
    if (addCategory) addCategory.style.display = "none";

    const formReport = document.getElementById("formReport");
    if (formReport) formReport.style.display = "none";

    const addExpense = document.getElementById("addExpense");
    if (addExpense) addExpense.style.display = "none";

    const addAvailability = document.getElementById("addAvailability");
    if (addAvailability) addAvailability.style.display = "none";

    const addProduct = document.getElementById("addProduct");
    if (addProduct) addProduct.style.display = "none";

    const addOrder = document.getElementById("addOrder");
    if (addOrder) addOrder.style.display = "none";

    //------------
    const openMenu = document.getElementById("openMenu");
    if (openMenu) openMenu.style.display = "block";

    document.body.classList.remove('body-frozen');
}

function sendModal(){
    return
}

let modalContext = null;

function openModal(modalId, context = {}){
    modalContext = context;
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = "flex";
        document.getElementById("openMenu").style.display = "none";
        document.getElementById("offcanvas-menu").style.display = "none";
        document.body.classList.add('body-frozen');
    }
}