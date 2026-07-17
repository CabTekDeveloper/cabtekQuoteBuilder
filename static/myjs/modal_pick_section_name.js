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
    AddNewSection: "AddNewSection",
    CopyCurrentSection: "CopyCurrentSection"
});

let commitButtonActionType = null;

const RESERVED_SECTION_WORDS = ['assembly', 'install', 'benchtop', 'bench', 'delivery'];


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


//Add new section
function AddNewSection() {
    resetModalPickSectionName();
    modalHeaderTag.innerText = "+ New Section"
    commitButton.innerText = "Add";
    commitButtonActionType = ActionTypes.AddNewSection
    loadModalPickSectionName();
}


//Copy current section
function copyCurrentSection() {
    resetModalPickSectionName();
    modalHeaderTag.innerText = `Copy section: ${getActiveSectionNameFromDiv()}`;
    commitButton.innerText = "Copy";
    commitButtonActionType = ActionTypes.CopyCurrentSection;
    loadModalPickSectionName();
}


// Load Pick section name modal
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
    let topOptions = `<option></option> <option disabled>-- Reserved section names --</option>`;
    let optionsHTML = `<option disabled> </option> <option value="" disabled>-- Joinery section names --</option>`;
    let selectedSectionNames = getSelectedSectionNamesFromDiv();

    filteredSectionNames = AllSectionNames.filter(item => !selectedSectionNames.includes(item['section_name']));

    filteredSectionNames.forEach(item => {
        if (item.is_active === "yes") {
            const nameLower = item.section_name.toLowerCase();
            const isReservedWord = RESERVED_SECTION_WORDS.some(rWord => nameLower.includes(rWord));
            if (isReservedWord) {
                topOptions += `<option value="${item['section_name']}">${item['section_name']} </option>`;
            }
            else {
                optionsHTML += `<option value="${item['section_name']}">${item['section_name']} </option>`;
            }
        }
    });
    optionSelectTag.insertAdjacentHTML('beforeend', topOptions + optionsHTML);
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
    addNewSectionNameBtn.onclick = async (e) => {
        // Wait for the function to resolve to a real true/false boolean value
        const addedNewSection = await getNewSectionNameAndAddToDBandSelectTag(sectionNameoptionSelectTag);

        if (addedNewSection) {
            unHideElement(commitButton);
        }
    };
}

// Get new section name from the user, add it to the database and update the select optins tag
async function getNewSectionNameAndAddToDBandSelectTag(optionSelectTag) {
    const reservedWordsWarningMessage = "The new Joinery section name cannot contain the following words, or similar words:\n- Assembly\n- Install \n- Bench \n- Benchtop\n- Delivery";
    let newSectionName = prompt(reservedWordsWarningMessage + "\n\n" + "Enter a new Joinery section name:");

    // Return false instead of just empty return
    if (newSectionName == null || newSectionName.trim().length === 0) {
        return false;
    }

    // => Check new section name contains letters and numbers only.
    let arrNewSectionName = newSectionName.split(" ").filter(Boolean);
    if (arrNewSectionName.every(item => isAlphaNumeric(item))) {
        newSectionName = arrNewSectionName.join(" ");
    } else {
        alert(`${newSectionName}\nSection name should be numbers and alphabets only!`);
        return false;
    }

    const lowerNewName = newSectionName.toLowerCase();

    // => Check the new section name does not contain the reserved names exactly
    const containsReservedSection = RESERVED_SECTION_WORDS.some(keyword => lowerNewName.includes(keyword));

    if (containsReservedSection) {
        alert(`The name "${newSectionName}" is not allowed.\n\n${reservedWordsWarningMessage}`);
        return false;
    }

    // => Check if the new section name closely matches the reserved section names
    const similarityThresholdPercentage = 70;
    let isTooSimilar = false;

    for (let word of arrNewSectionName) {
        let wordLower = word.toLowerCase();

        isTooSimilar = RESERVED_SECTION_WORDS.some(reserved => {
            return calculateTextSimilarityPercentage(wordLower, reserved) >= similarityThresholdPercentage;
        });

        if (isTooSimilar) break;
    }

    if (isTooSimilar) {
        alert(`The name "${newSectionName}" is not allowed. Please choose a more distinct name.\n\n${reservedWordsWarningMessage}.`);
        return false;
    }

    // => Save if a valid section name is entered.
    let data_to_post = { "new_section_name": newSectionName };
    let data = await saveNewSectionNameInDB(data_to_post);

    if (data && data["added"] === true) {
        let updatedSectionNames = data["all_section_names"];
        updateSectionNameOptionSelectTag(optionSelectTag, updatedSectionNames, newSectionName);
        optionSelectTag.selectedIndex = indexOfMatchingTextInSelectTag(optionSelectTag, newSectionName);
        return true;
    } else {
        alert(`'${newSectionName}' already exists in the list! \n\nTry another name.`);
        return false;
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
    let isNewSection = (commitButtonActionType == ActionTypes.AddNewSection) ? true : false;
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











