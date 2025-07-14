

// JS : Edit Product Parts Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editProductPartsModal = document.getElementById("edit_product_parts_modal");
let selectedPartsDiv = editProductPartsModal.querySelector("#selected_items_div");
let notSelectedPartsDiv = editProductPartsModal.querySelector("#not_selected_items_div");
let saveNewProductPartBtn = editProductPartsModal.querySelector("#save_changes_btn");
let searchPartsInput = editProductPartsModal.querySelector("#search_items_input");
/* Functions ------------------------------------------------------------------------------------------------------------------------*/

async function closeEditProductPartsModal() {
    if (saveNewProductPartBtn.classList.contains("hide") == false) {
        if (confirm("You have made changes.\n\nHit 'OK' to save the changes.") == true) {
            await saveSelectedProductParts();
        }
    }
    closeModal(editProductPartsModal.id)
}


function LoadEditProductPartsModal() {
    searchPartsInput.value = "";
    hideElement(saveNewProductPartBtn);
    let selectedProductNameTag = document.querySelector("#selected_product_name");
    let selectedProductTypeNameTag = document.querySelector("#selected_product_type_name");

    let selectedParts = []
    let notSelectedParts = []
    let currentProductInfo = GlobalVariablesCP.SelectedProductInfo;
    let AllParts = GlobalVariablesCP.AllParts;

    if (!isEmpty(currentProductInfo)) {
        let selectedProductParts = currentProductInfo['parts'];
        openModal(editProductPartsModal.id)

        selectedProductNameTag.innerText = currentProductInfo['name'];
        selectedProductTypeNameTag.innerText = currentProductInfo['product_type'];

        AllParts.forEach(part => {
            let isSelected = selectedProductParts.some(el => part['id'] == el['id']);
            (isSelected) ? selectedParts.push(part) : notSelectedParts.push(part)
        });

        updateSelectedPartNamesDiv(selectedParts);
        updateNotSelectedPartNamesDiv(notSelectedParts);

    }

}

function updateSelectedPartNamesDiv(parts) {
    let html = "";
    parts.forEach(part => html += buildHtmlForPart(part, true));
    selectedPartsDiv.innerHTML = html;
}

function updateNotSelectedPartNamesDiv(parts) {
    let html = "";
    parts.forEach(part => html += buildHtmlForPart(part, false));
    notSelectedPartsDiv.innerHTML = html;
}


function addPartToProduct(clckedTag) {
    let clickedPartInfo = JSON.parse(clckedTag.dataset.part_info);
    let selectedParts = getSelectedPartsFromDiv();
    selectedParts.push(clickedPartInfo);
    let sortedArray = sortArrayObjects(selectedParts, "id");
    updateSelectedPartNamesDiv(sortedArray);
    unHideElement(saveNewProductPartBtn);
    // Remove the clicked part from the current list
    clckedTag.parentNode.remove();
}

function removePartFromProduct(clckedTag) {
    let clickedPartInfo = JSON.parse(clckedTag.dataset.part_info);
    let notSelectedParts = getNotSelectedPartsFromDiv();
    notSelectedParts.push(clickedPartInfo);
    let sortedArray = sortArrayObjects(notSelectedParts, "id");
    updateNotSelectedPartNamesDiv(sortedArray);
    unHideElement(saveNewProductPartBtn);
    // Remove the clicked part from the current list
    clckedTag.parentNode.remove();
}

function buildHtmlForPart(part, isSelected = false) {

    if (isSelected) {
        return `<li class="hover-text-red cursor-pointer mt-1" data-part_info='${JSON.stringify(part)}' >
                    <span data-part_info='${JSON.stringify(part)}' onclick="removePartFromProduct(this)" > ${part['name']} </span>
                </li>` ;
    }
    else {
        return `<li class="hover-text-blue cursor-pointer mt-1 hover-text-bold" data-part_info='${JSON.stringify(part)}' >
                    <span data-part_info='${JSON.stringify(part)}' onclick="addPartToProduct(this)" > ${part['name']}  </span>
                </li>` ;
    }

}


function getSelectedPartsFromDiv() {
    let selectedParts = [];
    let partsEl = [...selectedPartsDiv.childNodes]
    partsEl.forEach(el => selectedParts.push(JSON.parse(el.dataset.part_info)));
    return selectedParts;
}

function getNotSelectedPartsFromDiv() {
    let notSelectedParts = [];
    let partsEl = [...notSelectedPartsDiv.childNodes]
    partsEl.forEach(el => notSelectedParts.push(JSON.parse(el.dataset.part_info)));
    return notSelectedParts;
}

async function saveSelectedProductParts() {
    hideElement(saveNewProductPartBtn);
    let currentProductInfo = GlobalVariablesCP.SelectedProductInfo;
    let selectedParts = getSelectedPartsFromDiv();
    let dataToSave = {
        "id": currentProductInfo['id'],
        "name": currentProductInfo['name'],
        "product_type_id": currentProductInfo['product_type_id'],
        "product_type": currentProductInfo['product_type'],
        "parts": selectedParts
    }

    var updated = await updateProductPartsInDB(dataToSave)
    if (updated) {

        // Update Global variable with updated product info
        // Also populate product parts with the update info
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id'])
        populateProductParts(updatedProductInfo)
        GlobalVariablesCP.SelectedProductInfo = updatedProductInfo
    }
    else {
        alert("Failed to save!")
        unHideElement(saveNewProductPartBtn, false);
    }
}


if (searchPartsInput != null) {
    searchPartsInput.onkeyup = (e) => filterAndUpdateNotSelectedPartDiv();
}


function filterAndUpdateNotSelectedPartDiv() {
    let searchString = searchPartsInput.value.trim().toLowerCase();
    let filteredItems = fileterOutSelectedPartFromAllParts()
    if (!isEmpty(searchString)) {
        filteredItems = filteredItems.filter(item => item.name.toLowerCase().startsWith(searchString));
    }
    updateNotSelectedPartNamesDiv(filteredItems);
}

// This function will remove all the parts present in the selected div from AllParts array, and return the fileterd array of parts
function fileterOutSelectedPartFromAllParts() {
    let notSelectedItems = [];
    let AllParts = GlobalVariablesCP.AllParts;
    let selectedParts = getSelectedPartsFromDiv();

    AllParts.forEach(part => {
        let isSelected = selectedParts.some(selectedPart => part['id'] == selectedPart['id']);
        if (!isSelected) notSelectedItems.push(part)
    });

    return notSelectedItems;
}



async function addNewPartInDB() {
    
    let newItemName = prompt("\n\nEneter new part name:");

    if (newItemName != null && newItemName.trim() != "") {
        newItemName = newItemName.toUpperCase();
        let AllParts = GlobalVariablesCP.AllParts;
        let existsInDB = AllParts.some(item => item.name == newItemName)

        if (existsInDB) {
            alert(`\n${newItemName}\n\nPart not added!\nIt exists already in the database.`)
        }
        else {
            let dataToSave = {"name": newItemName }

            var added = await insertNewPartInDb(dataToSave);
            if (added) {
                GlobalVariablesCP.AllParts = await getAllPartNamesFromDB();
                filterAndUpdateNotSelectedPartDiv();
            }
        }

    }

}