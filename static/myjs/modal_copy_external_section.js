// Wangchuk added, 01-08-2025


/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let modalCopyExternalSection = document.getElementById("modal_copy_external_section");
let closeModalCopyExternalSection = modalCopyExternalSection.querySelector("#close_modal_btn");
let confirmCopyBtn = modalCopyExternalSection.querySelector("#commit_btn");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

// Close modal 
if (closeModalCopyExternalSection != null) {
    closeModalCopyExternalSection.onclick = (e) => closeModal(modalCopyExternalSection.id);
}



// Load Pick section name modal
async function loadModalCopyExternalSection(copyBtn) {
    if (getSelectedSectionNamesFromDiv().length > 0) { await autoSaveSectionDetails(); }

    let user_id = copyBtn.getAttribute('data-user_id')
    let QuotesByUserId = await GetQuotesByUserId(user_id);

    if (!isEmpty(QuotesByUserId)) {
        openModal(modalCopyExternalSection.id)
        // updateSectionNameOptionSelectTag(sectionNameoptionSelectTag, AllSectionNames)
    }
    
    
}

