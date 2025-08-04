// Wangchuk added, 01-08-2025


/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let modalCopyExternalSection = document.getElementById("modal_copy_external_section");
let closeModalCopyExternalSection = modalCopyExternalSection.querySelector("#close_modal_btn");
let copySectionBtn = modalCopyExternalSection.querySelector("#commit_btn");
let quoteNameoptionSelectTag = modalCopyExternalSection.querySelector("#quote_name_options");
let sectionNameOptionSelectTag = modalCopyExternalSection.querySelector("#section_name_options");

let CurrentQuoteName = null;
let SelectedQuoteData = null;
let SelectedSectionData = null;

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

// Close modal 
if (closeModalCopyExternalSection != null) {
    closeModalCopyExternalSection.onclick = (e) => closeModal(modalCopyExternalSection.id);
}

function resetModalCopyExternalSection() {
    quoteNameoptionSelectTag.innerHTML = "";
    sectionNameOptionSelectTag.innerHTML = "";
    CurrentQuoteName = null;
    SelectedQuoteData = null;
    SelectedSectionData = null;

}

// Load Pick section name modal
async function loadModalCopyExternalSection(copyBtn) {
    resetModalCopyExternalSection();
    if (getSelectedSectionNamesFromDiv().length > 0) { await autoSaveSectionDetails(); }
    CurrentQuoteName = quoteNameElement.innerText.trim();
    let user_id = copyBtn.getAttribute('data-user_id')
    let QuotesByUserId = await GetQuotesByUserId(user_id);

    if (!isEmpty(QuotesByUserId)) {
        let optionsHTML = `<option value=""></option>`;
        let filterQuotes = QuotesByUserId.filter(quote => quote['quote_name'] != CurrentQuoteName)
        filterQuotes.forEach(item => optionsHTML += `<option value="${item['quote_id']}">  ${item['quote_name']} </option>`);
        quoteNameoptionSelectTag.innerHTML = optionsHTML;
        openModal(modalCopyExternalSection.id)
    }
}


async function QuoteNameOnChange() {
    hideElement(copySectionBtn)
    sectionNameOptionSelectTag.innerHTML = "";
    let selectedQuoteName = quoteNameoptionSelectTag.options[quoteNameoptionSelectTag.selectedIndex].innerText;

    if (!isEmpty(selectedQuoteName)) {
        SelectedQuoteData = await getQuoteDataFromDB(selectedQuoteName);

        if (!isEmpty(SelectedQuoteData)) {
            let sectionNames = SelectedQuoteData['section_names']

            if (!isEmpty(sectionNames)) {
                let optionsHTML = `<option value=""></option>`;
                sectionNames.forEach(item => optionsHTML += `<option value="${item}">  ${item} </option>`);
                sectionNameOptionSelectTag.innerHTML = optionsHTML;
            }
        }
    }

}

function SectionNameOptionOnChange() {
    hideElement(copySectionBtn)
    let selectedSectionName = sectionNameOptionSelectTag.options[sectionNameOptionSelectTag.selectedIndex].value;
    if (!isEmpty(selectedSectionName)) {
        SelectedSectionData = SelectedQuoteData['all_sections_data'][selectedSectionName];
        unHideElement(copySectionBtn)
    }

}


if (copySectionBtn != null) {
    copySectionBtn.onclick = (e) => CopySelectedSectionInDB();
}


async function CopySelectedSectionInDB(){
    let sectionImages = SelectedSectionData['section_image_full_names'];
    let sectionImageNamesAndSize = "";

    for(let i=0;i<sectionImages.length;i++){
        let image = sectionImages[i];
        let imageSizeInfo = image['image_size_info'];
        let imageSizeId =  imageSizeInfo['section_image_size_id']
        sectionImageNamesAndSize += `${image['image_full_name']};imageSizeId_${imageSizeId}`;
        if(i != sectionImages.length-1) {sectionImageNamesAndSize += "|";}
    }
    
    SelectedSectionData['quote_name'] = CurrentQuoteName;
    SelectedSectionData['section_image_full_names'] = sectionImageNamesAndSize;
    let data_to_post = SelectedSectionData;

    let data = await saveSectionDetailsInDB(data_to_post);

    if (data && data['saved']) {
        closeModal(modalPickSectionName.id);
    }
    else {
        alert(`Section not "copied")}. Try again!`)
        unHideElement(commitButton);
    }
}