// Wangchuk added, 08-05-2025
// Wangchuk modified 01-08-2025

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let modalPickSectionName = document.getElementById("modal_pick_section_name");
let closeModalPickSectionName = modalPickSectionName.querySelector("#close_modal_btn");
let modalHeaderTag = modalPickSectionName.querySelector("#modal_header");
let sectionNameoptionSelectTag = modalPickSectionName.querySelector("#section_name_options");
let addNewSectionNameBtn = modalPickSectionName.querySelector("#add_new_section_name_btn");
let commitButton = modalPickSectionName.querySelector("#commit_btn");

const ActionTypes = Object.freeze({
    Add: "Add",
    Copy: "Copy"
});

let commitButtonActionType = null;
/* Functions ------------------------------------------------------------------------------------------------------------------------*/

// Close modal 
if (closeModalPickSectionName != null) {
    closeModalPickSectionName.onclick = (e) => closeModal(modalPickSectionName.id);
}


// Reset modal
function resetModalPickSectionName() {
    sectionNameoptionSelectTag.innerHTML = "";
    modalHeaderTag.innerText = "";
    commitButton.innerText = "";
    commitButtonActionType = null;
}


function AddNewSection() {
    resetModalPickSectionName();
    modalHeaderTag.innerText = "+ New Section"
    commitButton.innerText = "Add";
    commitButtonActionType = ActionTypes.Add
    loadModalPickSectionName();
}


function copyCurrentSection() {
    resetModalPickSectionName();
    modalHeaderTag.innerText = `Copy section: ${getActiveSectionNameFromDiv()}`;
    commitButton.innerText = "Copy";
    commitButtonActionType = ActionTypes.Copy;
    loadModalPickSectionName();
}


// Load modal
async function loadModalPickSectionName() {
    let AllSectionNames = await GetAllSectionNamesFromDB();
    if (getSelectedSectionNamesFromDiv().length > 0) { await autoSaveSectionDetails(); }

    if (!isEmpty(AllSectionNames)) {
        openModal(modalPickSectionName.id)
        updateSectionNameOptionSelectTag(sectionNameoptionSelectTag, AllSectionNames)
    }
}

function updateSectionNameOptionSelectTag(optionSelectTag, AllSectionNames) {
    optionSelectTag.innerHTML = "";
    let filteredSectionNames = [];
    let optionsHTML = `<option value=""></option>`;
    let selectedSectionNames = getSelectedSectionNamesFromDiv();

    filteredSectionNames = AllSectionNames.filter(item => !selectedSectionNames.includes(item['section_name']));
    filteredSectionNames.forEach(item => {
        option = `<option value="${item['section_name']}">  ${item['section_name']} </option>`;
        optionsHTML += option;
    });
    optionSelectTag.insertAdjacentHTML('beforeend', optionsHTML);
}


// Event: Section name option on change
if (sectionNameoptionSelectTag != null) {
    sectionNameoptionSelectTag.onchange = (e) => {
        var val = sectionNameoptionSelectTag.options[sectionNameoptionSelectTag.selectedIndex].value.trim();
        isEmpty(val) ? hideElement(commitButton) : unHideElement(commitButton);
    };
}

// Button: To add a new section name to the database and update Section names select options.
if (addNewSectionNameBtn != null) {
    addNewSectionNameBtn.onclick = (e) => {
        getNewSectionNameAndAddToDBandSelectTag(sectionNameoptionSelectTag);
        unHideElement(commitButton);
    };
}

// Get new section name from the user, add it to the database and update the select optins tag
async function getNewSectionNameAndAddToDBandSelectTag(optionSelectTag) {
    let newSectionName = (prompt("Save new section name to database?\n\nEnter a new section name:"))
    if (newSectionName == null || newSectionName.trim().length == 0) return
    // Split section name into an array and remove the empty items.
    //Then, check if the items contain only alphabets and numbers only
    let arrNewSectionName = newSectionName.split(" ").filter(Boolean);
    if (arrNewSectionName.every(item => isAlphaNumeric(item))) {
        newSectionName = arrNewSectionName.join(" ");
    }
    else {
        alert(`${newSectionName}\nSection name can contain numbers and alphabets only!`)
        return;
    }

    let data_to_post = { "new_section_name": newSectionName }
    let data = await saveNewSectionNameInDB(data_to_post);

    if (data && data["added"] == true) {
        let updatedSectionNames = data["all_section_names"];
        updateSectionNameOptionSelectTag(optionSelectTag, updatedSectionNames, newSectionName)
        optionSelectTag.selectedIndex = indexOfMatchingTextInSelectTag(optionSelectTag, newSectionName)
    }
    else {
        alert(`'${newSectionName}' already exists in the list! \n\nTry another name.`)
    }
}

// Button: To copy and add section to the database and also an empty section template to the DOM. Users can then add section details rows.
if (commitButton != null) {
    commitButton.onclick = (e) => addcopyCurrentSectionToDBandDIV();
}

// Add or Copy section to database and Div
async function addcopyCurrentSectionToDBandDIV() {
    hideElement(commitButton);
    let newSectionName = sectionNameoptionSelectTag.options[sectionNameoptionSelectTag.selectedIndex].value.trim();
    let isNewSection = (commitButtonActionType == ActionTypes.Add) ? true : false;
    let preparedSectionData = prepareSectionDataToSave(isNewSection);
    preparedSectionData['section_name'] = newSectionName

    let data_to_post = preparedSectionData;
    let data = await saveSectionDetailsInDB(data_to_post);

    if (data && data['saved']) {
        addNewSectionNameBtnToDiv(newSectionName);
        if (isNewSection) {
            addEmptySectionDetailsRowTemplate();
            quoteImageDiv.innerText = "";     
            if (getSelectedSectionNamesFromDiv().length == 1) { window.location.href = (`/add_quote_details/${data_to_post['quote_name']}`); }
        }
        closeModal(modalPickSectionName.id);
    }
    else {
        alert(`Section not ${(isNewSection ? "added" : "copied")}. Try again!`)
        unHideElement(commitButton);
    }

}











