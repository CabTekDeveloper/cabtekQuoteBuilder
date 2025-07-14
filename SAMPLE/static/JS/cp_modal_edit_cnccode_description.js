


// JS : Edit CncConde Parameters Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editCnccodeDescriptionModal = document.getElementById("edit_cnccode_description_modal");
let cnccodeDescriptionModalTextArea = editCnccodeDescriptionModal.querySelector("#description")
let saveCnccodeDescriptionBtn = editCnccodeDescriptionModal.querySelector("#save_changes_btn");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

async function closeEditCnccodeDescriptionModal() {
    if (saveCnccodeDescriptionBtn.classList.contains("hide") == false) {
        if (confirm("You have made changes.\n\nHit 'OK' to save the changes.") == true) {
            await saveCnccodeDescription();
        }
    }
    closeModal(editCnccodeDescriptionModal.id)
}


function LoadEditCnccodeDescription() {
    hideElement(saveCnccodeDescriptionBtn)
    let currentCnccodeInfo = GlobalVariablesCP.SelectedCnccodeInfo;

    if (!isEmpty(currentCnccodeInfo)) {
        openModal(editCnccodeDescriptionModal.id)
        let selectedCnccodeNameTag = editCnccodeDescriptionModal.querySelector("#selected_cnccode_name");

        selectedCnccodeNameTag.innerText = currentCnccodeInfo['name'];
        cnccodeDescriptionModalTextArea.innerHTML = currentCnccodeInfo['description'];
        
    }

}

if (cnccodeDescriptionModalTextArea != null) {
    cnccodeDescriptionModalTextArea.onkeyup = (e) => unHideElement(saveCnccodeDescriptionBtn);
}

async function saveCnccodeDescription() {
    hideElement(saveCnccodeDescriptionBtn);
    let currentProductInfo = GlobalVariablesCP.SelectedProductInfo;
    let currentCnccodeInfo = GlobalVariablesCP.SelectedCnccodeInfo
    let description = cnccodeDescriptionModalTextArea.value.trimEnd();
    let dataToSave = {
        "cnccode_id": currentCnccodeInfo['id'],
        "description": description
    }

    var updated = await updateCnccodeDescriptionInDB(dataToSave)
    if (updated) {
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id'])
        updateCnccodeDescriptionDiv(description)
        GlobalVariablesCP.SelectedProductInfo = updatedProductInfo
        GlobalVariablesCP.AllCncCodes = await getAllCncCodesFromDB();
        GlobalVariablesCP.SelectedCnccodeInfo = await getCnccodeInfoFromDB(currentCnccodeInfo['id'])
    }
    else {
        alert("Failed to save!")
        unHideElement(saveCnccodeDescriptionBtn);
    }
}



