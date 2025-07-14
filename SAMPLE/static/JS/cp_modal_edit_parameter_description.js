

// JS : Edit CncConde Parameters Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editParameterDescriptionModal = document.getElementById("edit_parameter_description_modal");
let parameterDescriptionModalTextArea = editParameterDescriptionModal.querySelector("#description")
let saveParameterDescriptionBtn = editParameterDescriptionModal.querySelector("#save_changes_btn");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

async function closeEditParameterDescriptionModal() {
    if (saveParameterDescriptionBtn.classList.contains("hide") == false) {
        if (confirm("You have made changes.\n\nHit 'OK' to save the changes.") == true) {
            await saveParameterDescription();
        }
    }
    closeModal(editParameterDescriptionModal.id)
}


function LoadEditParameterDescription() {
    hideElement(saveParameterDescriptionBtn)
    let currentParameterInfo = GlobalVariablesCP.SelectedParameterInfo;

    if (!isEmpty(currentParameterInfo)) {
        openModal(editParameterDescriptionModal.id)
        let selectedParameterNameTag = editParameterDescriptionModal.querySelector("#selected_parameter_name");

        selectedParameterNameTag.innerText = currentParameterInfo['name'];
        parameterDescriptionModalTextArea.innerHTML = currentParameterInfo['description'];
    }

}

if (parameterDescriptionModalTextArea != null) {
    parameterDescriptionModalTextArea.onkeyup = (e) => unHideElement(saveParameterDescriptionBtn);
}




async function saveParameterDescription() {
    hideElement(saveParameterDescriptionBtn);
    let currentProductInfo = GlobalVariablesCP.SelectedProductInfo;
    let currentParameterInfo = GlobalVariablesCP.SelectedParameterInfo

    let description = parameterDescriptionModalTextArea.value.trimEnd();
    let dataToSave = {
        "parameter_id": currentParameterInfo['id'],
        "description": description
    }

    var updated = await updateParameterDescriptionInDB(dataToSave)
    if (updated) {
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id'])
        updateParameterDescriptionDiv(description)
        GlobalVariablesCP.SelectedProductInfo   = updatedProductInfo
        GlobalVariablesCP.AllParameters = await getAllParameterFromDB();
        GlobalVariablesCP.SelectedParameterInfo   = await getParameterInfoFromDB(currentParameterInfo['id'])  
    }
    else {
        alert("Failed to save!")
        unHideElement(saveParameterDescriptionBtn);
    }
}



