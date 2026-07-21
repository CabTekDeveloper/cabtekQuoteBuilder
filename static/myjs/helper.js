// Updated by Wangchuk on 14-03-2025
// Updated by Wangchuk on 22-07-2026

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

// Quick helper to stop company names with spaces/quotes/symbols from breaking your HTML
function escapeHtml(str) {
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&#039;");
}


// Calculates how similar two strings are using Levenshtein distance, returning a score from 0 to 100%
function calculateTextSimilarityPercentage(str1, str2) {
    const s1 = str1.toLowerCase().trim();
    const s2 = str2.toLowerCase().trim();

    if (s1 === s2) return 100;
    if (s1.length === 0 || s2.length === 0) return 0;

    const costs = [];
    for (let i = 0; i <= s1.length; i++) {
        let lastValue = i;
        for (let j = 0; j <= s2.length; j++) {
            if (i === 0) {
                costs[j] = j;
            } else if (j > 0) {
                let newValue = costs[j - 1];
                if (s1[i - 1] !== s2[j - 1]) {
                    newValue = Math.min(Math.min(newValue, lastValue), costs[j]) + 1;
                }
                costs[j - 1] = lastValue;
                lastValue = newValue;
            }
        }
        if (i > 0) costs[s2.length] = lastValue;
    }

    const distance = costs[s2.length];
    const maxLength = Math.max(s1.length, s2.length);
    return (1 - distance / maxLength) * 100;
}

// Trigger filedownd in the browser
function triggerFileDownload(blobFile, fileName) {
    const url = window.URL.createObjectURL(blobFile);
    const tempAnchorTag = document.createElement("a");
    tempAnchorTag.style.display = "none";
    tempAnchorTag.href = url;
    tempAnchorTag.download = fileName;

    document.body.appendChild(tempAnchorTag);
    tempAnchorTag.click();

    // Clean up
    window.URL.revokeObjectURL(url);
    tempAnchorTag.remove();
}


// 22-07-2026 Wangchuk
// Old quotes lack the 'is_trade_client' field and require updating.
// The quote is considered "old" if data exists but the specific field is empty/missing
async function handleOutdatedQuote(quoteName) {
    const resData = await getQuoteInfoDB(quoteName);
    const isOld = !isEmpty(resData) && isEmpty(resData?.is_trade_client);

    if (isOld) {
        const userChoice = confirm(
            "This is an older quote that requires updated information.\n" +
            "Please update the missing fields first, then try again.\n\n" +
            "Click 'OK' to edit the quote now."
        );

        if (userChoice) {
            window.location.href = `/edit_quote/${resData.quote_id}`;
        }
        return true;
    }
    return false
}