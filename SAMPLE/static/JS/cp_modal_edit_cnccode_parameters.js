

// JS : Edit CncConde Parameters Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editCnccodeParametersModal = document.getElementById("edit_cnccode_parameters_modal");
let selectedParametersDiv = editCnccodeParametersModal.querySelector("#selected_items_div");
let notSelectedParametersDiv = editCnccodeParametersModal.querySelector("#not_selected_items_div");
let saveSelectedParametersBtn = editCnccodeParametersModal.querySelector("#save_changes_btn");
let searchParametersInput = editCnccodeParametersModal.querySelector("#search_items_input");


/* Functions ------------------------------------------------------------------------------------------------------------------------*/

async function closeEditCnccodeParametersModal() {
    if (saveSelectedParametersBtn.classList.contains("hide") == false) {
        if (confirm("You have made changes.\n\nHit 'OK' to save the changes.") == true) {
            await saveSelectedParameters();
        }
    }
    closeModal(editCnccodeParametersModal.id)
}


function LoadEditCnccodeParameters() {
    searchParametersInput.value = "";
    let currentCnccodeInfo = GlobalVariablesCP.SelectedCnccodeInfo;
    let selectedParameters = []
    let notSelectedParameters = []
    let AllParameters = GlobalVariablesCP.AllParameters;
    hideElement(saveSelectedParametersBtn)

    if (!isObjectEmpty(currentCnccodeInfo)) {
        let selectedCnccodeParameters = currentCnccodeInfo['parameters']
        let selectedCnccodeNameTag = editCnccodeParametersModal.querySelector("#selected_cnccode_name");
        selectedCnccodeNameTag.innerText = currentCnccodeInfo['name'];

        openModal(editCnccodeParametersModal.id)

        AllParameters.forEach(parameter => {
            let isSelected = selectedCnccodeParameters.some(el => parameter['id'] == el['id']);
            (isSelected) ? selectedParameters.push(parameter) : notSelectedParameters.push(parameter)
        });
        updateSelectedParametersDiv(selectedParameters);
        updateNotSelectedParametersDiv(notSelectedParameters);

    }

}

function updateSelectedParametersDiv(parameters) {
    let html = "";
    parameters.forEach(parameter => html += buildHtmlForParameter(parameter, true));
    selectedParametersDiv.innerHTML = html;
}

function updateNotSelectedParametersDiv(parameters) {
    let html = "";
    parameters.forEach(parameter => html += buildHtmlForParameter(parameter, false));
    notSelectedParametersDiv.innerHTML = html;
}


function addParameterToCnccode(clickedBtn) {
    let clickedParameterInfo = JSON.parse(clickedBtn.dataset.parameter_info);
    let selectedParameters = getSelectedParametersFromDiv();
    selectedParameters.push(clickedParameterInfo);
    let sortedArray = sortArrayObjects(selectedParameters, "id");
    updateSelectedParametersDiv(sortedArray);
    unHideElement(saveSelectedParametersBtn);
    // Remove the clicked part from the current list
    clickedBtn.parentNode.remove();
}


function removeParameterFromCnccode(clickedBtn) {
    let clickedParameterInfo = JSON.parse(clickedBtn.dataset.parameter_info);
    let notSelectedParameters = getSelectedNotParametersFromDiv();
    notSelectedParameters.push(clickedParameterInfo);
    let sortedArray = sortArrayObjects(notSelectedParameters, "id");
    updateNotSelectedParametersDiv(sortedArray);
    unHideElement(saveSelectedParametersBtn);
    // Remove the clicked part from the current list
    clickedBtn.parentNode.remove();
}

function buildHtmlForParameter(parameter, isSelected = false) {
    if (isSelected) {
        return `<li class="hover-text-red cursor-pointer mt-1" data-parameter_info = '${JSON.stringify(parameter)}' >
                    <span data-parameter_info='${JSON.stringify(parameter)}'  onclick="removeParameterFromCnccode(this)" > ${parameter['name']}</span>
                </li>` ;
    }
    else {
        return `<li class="hover-text-teal cursor-pointer mt-1 hover-text-bold" data-parameter_info ='${JSON.stringify(parameter)}'  >
                    <span data-parameter_info='${JSON.stringify(parameter)}'  onclick="addParameterToCnccode(this)" >${parameter['name']} </span>
                </li>` ;
    }
}

function getSelectedParametersFromDiv() {
    let items = [];
    let partsEl = [...selectedParametersDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.parameter_info)));
    return items;
}

function getSelectedNotParametersFromDiv() {
    let items = [];
    let partsEl = [...notSelectedParametersDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.parameter_info)));
    return items;
}

async function saveSelectedParameters() {
    hideElement(saveSelectedParametersBtn);
    let currentProductInfo = GlobalVariablesCP.SelectedProductInfo;
    let currentCnccodeInfo = GlobalVariablesCP.SelectedCnccodeInfo
    let selectedParameters = getSelectedParametersFromDiv();

    let dataToSave = {
        "cnccode_id": currentCnccodeInfo['id'],
        "parameters": selectedParameters
    }

    var updated = await updateCnccodeParametersInDB(dataToSave)
    if (updated) {
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id'])
        updateCnccodeParametersDiv(selectedParameters)
        GlobalVariablesCP.SelectedProductInfo = updatedProductInfo
        GlobalVariablesCP.AllCncCodes = await getAllCncCodesFromDB();
        GlobalVariablesCP.SelectedCnccodeInfo = await getCnccodeInfoFromDB(currentCnccodeInfo['id'])
    }
    else {
        alert("Failed to save!")
        unHideElement(saveSelectedParametersBtn);
    }
}



if (searchParametersInput != null) {
    searchParametersInput.onkeyup = (e) => filterAndUpdateNotSelectedParametersDiv();
}

function filterAndUpdateNotSelectedParametersDiv() {
    let searchString = searchParametersInput.value.trim().toLowerCase();
    let filteredItems = fileterOutSelectedParameters()

    if (!isEmpty(searchString)) {
        filteredItems = filteredItems.filter(item => item.name.toLowerCase().startsWith(searchString));
    }
    updateNotSelectedParametersDiv(filteredItems);
}

// This function will remove all the parts present in the selected div from AllParts array, and return the fileterd array of parts
function fileterOutSelectedParameters() {
    let notSelectedItems = [];
    let AllParameters = GlobalVariablesCP.AllParameters;
    let selectedParameters = getSelectedParametersFromDiv();

    AllParameters.forEach(parameter => {
        let isSelected = selectedParameters.some(selectedParameter => parameter['id'] == selectedParameter['id']);
        if (!isSelected) notSelectedItems.push(parameter)
    });

    return notSelectedItems;
}



async function addNewParameterInDB() {
    let searchString = searchParametersInput.value.trim().toLowerCase();

    let newParameterName = prompt("\n\nEneter new parameter:",searchString);
    if (newParameterName != null && newParameterName.trim() != "") {
        newParameterName = newParameterName.toUpperCase();
        let AllParameters = GlobalVariablesCP.AllParameters;
        let existsInDB = AllParameters.some(parameter => parameter.name == newParameterName)

        if (existsInDB) {
            alert(`\n${newParameterName}\n\nParameter not added!\nIt exists already in the database.`)
        }
        else {
            let dataToSave = { "name": newParameterName }

            var added = await insertNewParameterInDb(dataToSave);
            if (added) {
                GlobalVariablesCP.AllParameters = await getAllParameterFromDB();
                filterAndUpdateNotSelectedParametersDiv();
            }
        }

    }

}