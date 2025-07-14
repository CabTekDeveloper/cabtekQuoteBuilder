// Updated  : 14-03-2025
// By       : Wangchuk


function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}

function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}


function toggleMessageModal(message, showModal) {
    let modalShowMessage = document.getElementById("modal_show_message");


    if (showModal) {
        modalShowMessage.querySelector("#message").innerText = `${message}`;
        openModal(modalShowMessage.id)
    }
    else {
        setTimeout(() => closeModal(modalShowMessage.id), 1000);
    }
}


function hideElement(element) {
    if (!element.classList.contains("hide")) element.classList.add("hide")
}

function unHideElement(element) {
    if (element.classList.contains("hide")) element.classList.remove("hide");
}


function isEmpty(value) {
    return (
        value === null ||         // Checks for null
        value === undefined ||    // Checks for undefined
        value === '' ||           // Checks for empty string
        (Array.isArray(value) && value.length === 0) || //Checks for empty array
        (typeof value === 'object' && Object.keys(value).length === 0)    // Checks for empty object
    );
}



function isAlphaNumeric(text) {
    return /^[a-zA-Z0-9]*$/.test(text);
}


function deepCopyObject(obj) {
    return JSON.parse(JSON.stringify(obj));
}




function buildHTMLforSectionNameOption(sectionName) {
    return `<option value="${sectionName}">${sectionName}</option>`;

}



function filterOutSectionNames(AllSectionNames, filter) {
    let filteredSectionNames = [];
    filteredSectionNames = AllSectionNames.filter(item => !filter.includes(item['section_name']));
    return filteredSectionNames;
}



function buildHTMLforSectionNameBtn(sectionName) {
    return `<a href="#" onclick="sectionNameOnClick(this)" type="button" class="btn btn-sm d-inline-block bold">${sectionName}</a>`
}


// function addSectionNameBtnstoDiv(sectionNames) {
//     let sectionNameBtns = ""
//     sectionNames.forEach(sectionName => sectionNameBtns += buildHTMLforSectionNameBtn(sectionName));
//     sectionNamesDiv.innerHTML = sectionNameBtns;
//     addActiveStyleToSectionName(sectionNames[0]);
// }

function indexOfMatchingTextInSelectTag(optionSelectTag, text) {
    let index = null;
    let optionTags = optionSelectTag.getElementsByTagName("option");
    for (let i = 0; i < optionTags.length; i++) {
        if (optionTags[i].value == text) {
            return i;
        }
    }
    return index;
}

