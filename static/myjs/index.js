// 
// 
let savedQuotesDiv = document.getElementById('saved_quote_div')
let savedTemplateDiv = document.getElementById('saved_template_div')

let savedQuoteTable = document.getElementById('saved_quote_table')
let savedTemplateTable = document.getElementById('saved_template_table')

// index buttons and display divs
let savedQuoteBtn = document.getElementById('saved_quote_btn')
let createQuoteBtn = document.getElementById('create_quote_btn')
let SavedTemplateBtn = document.getElementById('saved_template_btn')

//-------------------------------------------------------------------------------------------------------------------------------------------------------
// TOGGLE COLOR OF ACTIVE AND INACTIVE BUTTONS, HIDE OR UNHIDE DISPLAY DIVS
function showSavedQuotesDiv() {
    addColorToActiveBtn(savedQuoteBtn)
    showActiveDisplayDiv(savedQuotesDiv)
}

function showSavedTemplateDiv() {
    addColorToActiveBtn(SavedTemplateBtn)
    showActiveDisplayDiv(savedTemplateDiv)
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
function addColorToActiveBtn(activeBtn) {
    let indexButtons = [savedQuoteBtn, createQuoteBtn, SavedTemplateBtn]
    indexButtons.forEach(el => {
        if (el == activeBtn) {
            el.classList.add('btn-dark')
        }
        else {
            el.classList.remove('btn-dark')
        }
    })

}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
function showActiveDisplayDiv(activeDisplayDiv) {
    let indexDisplayDivs = [savedQuotesDiv, savedTemplateDiv]
    indexDisplayDivs.forEach(el => {
        if (el == activeDisplayDiv) {
            el.classList.remove('hide')
        }
        else {
            el.classList.add('hide')
        }
    })
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
// DELETE QUOTE FROM TABLE
async function deleteQuote(quoteDeleteBtn) {
    let quoteId = quoteDeleteBtn.getAttribute('data-quote_id')
    let quoteName = quoteDeleteBtn.getAttribute('data-quote_name')
    let isTemplate = quoteDeleteBtn.getAttribute('data-is_template').trim()

    // Conmfirm and proceed
    if (confirm(`Are you sure you want to delete '${quoteName}'?`) == true) {
        toggleMessageModal("Deleting quote!", true);

        let res = await deleteQuoteFromDB({ "quote_id": quoteId });

        if (res && res.success) {
            window.location.href = `/index/${isTemplate}`;
        }
        else {
            alert("Quote not deleted!")
        }
        toggleMessageModal("", false);
    }
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
// COPY AND ADD THE COPIED QUOTE IN THE TOP ROW OF THE TABLE
async function copyQuoteAndDetails(copyBtn) {
    let quoteId = copyBtn.getAttribute('data-quote_id').trim();
    let quoteName = copyBtn.getAttribute('data-quote_name').trim();
    let isTemplate = copyBtn.getAttribute('data-is_template').trim();

    // Old quotes are missing new fields and require updating.
    const isOld = await handleOutdatedQuote(quoteName);
    if (isOld) return;

    // Confirm and proceed
    if (confirm(`Are you sure you want to make a copy of "${quoteName}"?`)) {
        toggleMessageModal("Copying quote!", true);
        let data_to_post = { "quote_id": quoteId };
        let data = await copyQuoteAndDetailsInDB(data_to_post);

        if (data && data.success) {
            window.location.href = `/index/${isTemplate}`;
        }
        else {
            alert("Failed to copy quote!");
        }
        toggleMessageModal("", false);  //Close modal
    }
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
