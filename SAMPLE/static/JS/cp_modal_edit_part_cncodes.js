

// JS : Edit Part CncCondes Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editPartCncCodesModal = document.getElementById("edit_part_cnccodes_modal");
let selectedCnccodesDiv = editPartCncCodesModal.querySelector("#selected_items_div");
let notSelectedCnccodesDiv = editPartCncCodesModal.querySelector("#not_selected_items_div");
let saveSelectedCnccodesBtn = editPartCncCodesModal.querySelector("#save_changes_btn");
let searchCnccodesInput = editPartCncCodesModal.querySelector("#search_items_input");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

async function closeEditPartCnccodesModal() {
    if (saveSelectedCnccodesBtn.classList.contains("hide") == false) {
        if (confirm("You have made changes.\n\nHit 'OK' to save the changes.") == true) {
            await saveSelectedPartCncCodes();
        }
    }
    closeModal(editPartCncCodesModal.id)
}

function LoadEditPartCncCodes(clickedPartTag) {
    searchCnccodesInput.value = "";
    hideElement(saveSelectedCnccodesBtn)

    let clickedPartInfo = JSON.parse(clickedPartTag.dataset.part_info)
    GlobalVariablesCP.SelectedPartInfo = clickedPartInfo;   //Update gloabal variable

    let selectedCnccodes = []
    let notSelectedCnccodes = []
    let AllCnccodes = GlobalVariablesCP.AllCncCodes;
    let currentProductInfo = GlobalVariablesCP.SelectedProductInfo;

    let selectedPartNameTag = editPartCncCodesModal.querySelector("#selected_part_name");
    let selectedProductNameTag = editPartCncCodesModal.querySelector("#selected_product_name");
    let selectedProductTypeNameTag = editPartCncCodesModal.querySelector("#selected_product_type_name");

    if (!isObjectEmpty(clickedPartInfo)) {
        openModal(editPartCncCodesModal.id)

        let selectedPartCnccodes = clickedPartInfo['cnccodes']

        selectedPartNameTag.innerText = clickedPartInfo['name'];
        selectedProductNameTag.innerText = currentProductInfo['name'];
        selectedProductTypeNameTag.innerText = currentProductInfo['product_type'];

        AllCnccodes.forEach(cnccode => {
            let isSelected = selectedPartCnccodes.some(el => cnccode['id'] == el['id']);
            (isSelected) ? selectedCnccodes.push(cnccode) : notSelectedCnccodes.push(cnccode)
        });

        updateSelectedCnccodeDiv(selectedCnccodes);
        updateNotSelectedCnccodeDiv(notSelectedCnccodes);
    }

}

function updateSelectedCnccodeDiv(cnccodes) {
    let html = "";
    cnccodes.forEach(cnccode => html += buildHtmlForCnccode(cnccode, true));
    selectedCnccodesDiv.innerHTML = html;
}

function updateNotSelectedCnccodeDiv(cnccodes) {
    let html = "";
    cnccodes.forEach(cnccode => html += buildHtmlForCnccode(cnccode, false));
    notSelectedCnccodesDiv.innerHTML = html;
}


function addCnccodeToPart(clickedCnccodeBtn) {
    let clickedCnccodeInfo = JSON.parse(clickedCnccodeBtn.dataset.cnccode_info);
    let selectedCnccodes = getSelectedCnccodesFromDiv();
    selectedCnccodes.push(clickedCnccodeInfo);
    let sortedArray = sortArrayObjects(selectedCnccodes, "id");
    updateSelectedCnccodeDiv(sortedArray);
    unHideElement(saveSelectedCnccodesBtn);
    // Remove the clicked part from the current list
    clickedCnccodeBtn.parentNode.remove();
}

function removeCnccodeFromPart(clickedCnccodeBtn) {
    let clickedCnccodeInfo = JSON.parse(clickedCnccodeBtn.dataset.cnccode_info);
    let notSelectedCnccodes = getNotSelectedCnccodesFromDiv();
    notSelectedCnccodes.push(clickedCnccodeInfo);
    let sortedArray = sortArrayObjects(notSelectedCnccodes, "id");
    updateNotSelectedCnccodeDiv(sortedArray);
    unHideElement(saveSelectedCnccodesBtn);
    // Remove the clicked part from the current list
    clickedCnccodeBtn.parentNode.remove();
}

function buildHtmlForCnccode(cnccode, isSelected = false) {

    if (isSelected) {
        return `<li class="hover-text-red cursor-pointer mt-1" data-cnccode_info ='${JSON.stringify(cnccode)}' >
                    <span data-cnccode_info='${JSON.stringify(cnccode)}' onclick="removeCnccodeFromPart(this)" >${cnccode['name']} </span>
                </li>` ;
    }
    else {
        return `<li class="hover-text-orange cursor-pointer mt-1 hover-text-bold" data-cnccode_info='${JSON.stringify(cnccode)}' >
                    <span data-cnccode_info='${JSON.stringify(cnccode)}' data-part_name="${cnccode['name']}" onclick="addCnccodeToPart(this)" >${cnccode['name']} </span>
                </li>` ;
    }

}


function getSelectedCnccodesFromDiv() {
    let items = [];
    let partsEl = [...selectedCnccodesDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.cnccode_info)));
    return items;
}

function getNotSelectedCnccodesFromDiv() {
    let items = [];
    let partsEl = [...notSelectedCnccodesDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.cnccode_info)));
    return items;
}

async function saveSelectedPartCncCodes() {
    hideElement(saveSelectedCnccodesBtn);
    let currentProductInfo = GlobalVariablesCP.SelectedProductInfo;
    let currentPartInfo = GlobalVariablesCP.SelectedPartInfo;
    let selectedCnccodes = getSelectedCnccodesFromDiv();

    let dataToSave = {
        "product_id": currentProductInfo['id'],
        "part_id": currentPartInfo['id'],
        "cnccodes": selectedCnccodes
    }

    var updated = await updatePartCnccodesInDB(dataToSave)
    if (updated) {

        // Update Global variable with updated product info
        // Also populate product parts with the update info
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id'])
        populateProductParts(updatedProductInfo)
        GlobalVariablesCP.SelectedProductInfo = updatedProductInfo
        GlobalVariablesCP.SelectedPartInfo = updatedProductInfo['parts'].find(part => part['id'] == currentPartInfo['id'])
    }
    else {
        alert("Failed to save!")
        unHideElement(saveSelectedCnccodesBtn);
    }
}



if (searchCnccodesInput != null) {
    searchCnccodesInput.onkeyup = (e) => filterAndUpdateNotSelectedCnccodeDiv();
}

// 28-04-2025 *Please note  : 
                        //  : GlobalVariablesCP.AllCncCodes gets updated in the function addNewCnccodeInDB when a new cnccode is added.
                        //  : However, the GlobalVariablesCP.AllCncCodes still retains it's old in the function below
                        //  : Once this issue is resolved, you can remove this comment.
function filterAndUpdateNotSelectedCnccodeDiv() {
    // Filter out selected cnccodes from all cnccodes
    let AllCnccodes = GlobalVariablesCP.AllCncCodes;
    let selectedCnccodes = getSelectedCnccodesFromDiv();
    let notSelectedItems = [];
    AllCnccodes.forEach(cnccode => {
        let isSelected = selectedCnccodes.some(selectedCnccode => cnccode['id'] == selectedCnccode['id']);
        if (!isSelected) notSelectedItems.push(cnccode)
    });

    // Filter further the not selected cncocdes using the filter string
    let filterString = searchCnccodesInput.value.trim().toLowerCase();
    let filteredItems = [];
    if (isEmpty(filterString)) {
        filteredItems = notSelectedItems;
    }
    else{
        filteredItems = notSelectedItems.filter(item => item.name.toLowerCase().startsWith(filterString));
    }

    // Finally, update the not selcted ite div
    updateNotSelectedCnccodeDiv(filteredItems);
}




async function addNewCnccodeInDB() {

    let newItemName = prompt("\n\nEneter new cnccode:");

    if (newItemName != null && newItemName.trim() != "") {
        newItemName = newItemName.toUpperCase();
        let AllCnccodes = GlobalVariablesCP.AllCncCodes;
        let existsInDB = AllCnccodes.some(item => item.name == newItemName)

        if (existsInDB) {
            alert(`\n${newItemName}\n\nCnccode not added!\nIt exists already in the database.`)
        }
        else {
            let dataToSave = {  "name": newItemName }
            let added = await insertNewCnccodeInDb(dataToSave);
            
            if (added) {
                GlobalVariablesCP.AllCnccodes = await getAllCncCodesFromDB();
                filterAndUpdateNotSelectedCnccodeDiv();
            }
        }

    }

}