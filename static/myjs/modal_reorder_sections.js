// Modal: Reorder sections


/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let ACTIVE_SECTION = null
let modalReorderSections = document.getElementById("modal_reorder_section");
let saveReorderedSectionBtn = modalReorderSections.querySelector('#save_reordered_section')
let reorderBtnsDiv = modalReorderSections.querySelector('#reorder_btns_div')
let allSectionsDiv = modalReorderSections.querySelector('#all_sections_div')
let closeModalReorderSectionBtn = modalReorderSections.querySelector('#close_modal_btn')

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

// Close modal 
if (closeModalReorderSectionBtn != null) {
    closeModalReorderSectionBtn.onclick = (e) => {
        // let quoteName = quoteNameElement.innerText
        // window.location.href = (`/add_quote_details/${quoteName}`)
        closeModal(modalReorderSections.id)
    }
}



// Reset modal
function resetReorderSectionModal() {
    hideElement(saveReorderedSectionBtn);
    allSectionsDiv.innerHTML = "";
}

async function loadModalReorderSections() {
    await autoSaveSectionDetails();

    resetReorderSectionModal();
    let selectedSectionNames = getSelectedSectionNamesFromDiv();

    if (!isEmpty(selectedSectionNames)) {
        openModal(modalReorderSections.id)
        let sectionNamesHtml = ""
        selectedSectionNames.forEach(item => {
            sectionNamesHtml += `<button type="button" class="btn  btn-info d-block text-left my-1 w-100 " onclick="sectionNameSelected(this)">${item}</button>`;
        });

        allSectionsDiv.innerHTML = sectionNamesHtml;
    }

}

function sectionNameSelected(selectedSection) {
    // First, we will make apply same background color to all the section names
    Array.from(allSectionsDiv.getElementsByTagName('button')).forEach(btn => btn.classList.add('btn-info'))

    // Set the global variable. Set the global variable to 'selectedSection' only after the background class has been removed from it.
    // change bg color of selected section 
    selectedSection.classList.remove('btn-info')
    ACTIVE_SECTION = selectedSection

    // show reorder buttons
    disableReorderBtns(false)

}





function moveSectionUp() {
    let previousSection = ACTIVE_SECTION.previousElementSibling
    if (previousSection != null) {
        unHideElement(saveReorderedSectionBtn);
        previousSection.insertAdjacentElement('beforebegin', ACTIVE_SECTION)
    }
}

function moveSectionDown() {
    let nextSection = ACTIVE_SECTION.nextElementSibling
    if (nextSection != null) {
        unHideElement(saveReorderedSectionBtn);
        nextSection.insertAdjacentElement('afterend', ACTIVE_SECTION)
    }
}



//Show or hide up or down buttons
function disableReorderBtns(disable) {
    Array.from(reorderBtnsDiv.getElementsByTagName('button')).forEach(btn => btn.disabled = disable)
}


// UPDATE THE SECTION ORDER ID IN THE DATABASE
async function updateSectionOrderID() {
    ACTIVE_SECTION.classList.add('btn-info')
    let quoteName = quoteNameElement.innerText
    let orderedSectionNames = []

    disableReorderBtns(true)
    hideElement(saveReorderedSectionBtn);


    // Get new ordering of section names
    Array.from(allSectionsDiv.getElementsByTagName('button')).forEach((sectionName) => orderedSectionNames.push(sectionName.innerText))

    let data_to_post = {
        "quote_name": quoteName,
        "ordered_section_names": orderedSectionNames
    }
    let data = await reorderSectionNamesInDB(data_to_post)

    if (data && data['reordered']) {
        window.location.href = (`/add_quote_details/${quoteName}`)
    }
    else {
        alert("Section not reordered!\n\nRefresh the page and try again.")
    }

}

