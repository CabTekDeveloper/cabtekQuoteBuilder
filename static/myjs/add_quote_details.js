
//
let globalVar = {
    "activeSectionRowImageInpName": null,
    "clickedAddRemoveRowImgBtn": null
}
let page_path = window.location.pathname;

// declare global variables here for the html tags
let addQuoteDetailDiv = document.getElementById("add_quote_details_div");
let addResourcesDiv = document.getElementById("add_resources_div");
let quoteImageDiv = document.getElementById("quote_image_div")
let imageSearchDiv = document.getElementById('image_serach_div')
let imageSearchResultDiv = document.getElementById('imageSearchResultDiv')
let formImgUpload = document.getElementById('form_img_upload')
let imageFileInput = document.getElementById("image_file_input")
let imageTagNameInp = document.getElementById('image_tag_name_inp')
let fileUploadMsgDiv = document.getElementById('file_Upload_Msg_Div');
let uploadImageDiv = document.getElementById('uploadImageDiv')
let showUploadImageBtn = document.getElementById('showUploadImageBtn')
let imageTagNameDiv = document.getElementById('image_tag_name_div')
let deleteSectionBtn = document.getElementById('delete_section_btn')
// let addNewSectionNameBtn = document.getElementById('add_new_section_name_btn')
let addImageDiv = document.getElementById('addImageDiv')
let addTextDiv = document.getElementById('addTextDiv')
let addTextBtn = document.getElementById('addTextBtn')
let addImageBtn = document.getElementById('addImageBtn')
let sectionDetailsDiv = document.getElementById('section_details_div');
let addEoTextBtn = document.getElementById('addEoTextBtn')
let addEoExcelTextDiv = document.getElementById('addEoExcelTextDiv')
let eoExcelTextSerachDiv = document.getElementById('eo_excel_text_serach_div')
let uploadEoExcelDiv = document.getElementById('uploadEoExcelDiv')
let showUploadEoExcelBtn = document.getElementById('showUploadEoExcelBtn')
let eoExcelTextResultDiv = document.getElementById('eoExcelTextResultDiv')
let eoExcelTextSearchInput = document.getElementById('eo_excel_text_search_input')
let eoExcelFileInput = document.getElementById('eo_excel_file_input')
let eoExcelFileUploadMsgDiv = document.getElementById('eo_excel_file_Upload_Msg_Div')
let formEoExcelUpload = document.getElementById('form_eo_excel_upload')
let eoExcelTextUlBlock = document.getElementById('eo_excel_text_ul_block')
let textDisplayDiv = document.getElementById('text_display_div')
let textULblock = document.getElementById('text_ul_block')
let frequentlyUsedTextUlBlock = document.getElementById('frequently_used_text_ul_block')
let textSearchInput = document.getElementById("text_search_input")
let sectionNameDiv = document.getElementById("section_name_div")
let quoteNameElement = document.getElementById('quote_name')
let sectionNamesDiv = document.getElementById('section_names_div')
let saveSectionBtn = document.getElementById('save_section_btn')
let copyCurrentSectionBtn = document.getElementById('copy_current_section_btn')
let reorderSectionsBtn = document.getElementById('reorder_section_btn')



function getSectionNameButtonsFromDiv() {
    return sectionNamesDiv.getElementsByTagName('a');
}

function getSelectedSectionNamesFromDiv() {
    let selectedSectionNames = []
    let sectionNamesDivBtns = getSectionNameButtonsFromDiv()
    for (var btn of sectionNamesDivBtns) {
        selectedSectionNames.push(btn.innerText)
    }
    return selectedSectionNames;
}

// This function will get the active section name from add_quote_details.html
// The section name button containing the class "btn-dark" will be the active section name.
function getActiveSectionNameFromDiv() {
    let currentSectionName = "";
    let sectionNamesDivBtns = getSectionNameButtonsFromDiv()
    for (var btn of sectionNamesDivBtns) {
        if (btn.classList.contains("btn-dark")) {
            currentSectionName = btn.innerText
        }
    }
    return currentSectionName;
}

// ADD ROW IMAGE
function addRemoveRowImage(clickedAddRemoveRowImgBtn) {
    // set gloabl variable value
    let addRowImgBtnText = clickedAddRemoveRowImgBtn.innerText
    let sectionRowImageInpName = clickedAddRemoveRowImgBtn.dataset.img_inp_name;
    let sectionRowImageInp = sectionDetailsDiv.querySelector(`input[name = ${sectionRowImageInpName} ]`)

    globalVar.clickedAddRemoveRowImgBtn = clickedAddRemoveRowImgBtn

    if (addRowImgBtnText == '+Image') {
        globalVar.activeSectionRowImageInpName = sectionRowImageInpName
        sectionRowImageInp.placeholder = "Select image"
        sectionRowImageInp.style.backgroundColor = 'yellow'
        clickedAddRemoveRowImgBtn.innerHTML = "<small class='text-red'>Cancel</small>"
    }
    else if (addRowImgBtnText == '-Image') {
        globalVar.activeSectionRowImageInpName = null
        sectionRowImageInp.value = ""
        sectionRowImageInp.placeholder = ""
        sectionRowImageInp.style.backgroundColor = '#f5f5f5'
        clickedAddRemoveRowImgBtn.innerHTML = "<small>+Image</small>"
    }
    else {
        globalVar.activeSectionRowImageInpName = null
        sectionRowImageInp.placeholder = ""
        sectionRowImageInp.style.backgroundColor = '#f5f5f5'
        clickedAddRemoveRowImgBtn.innerHTML = "<small>+Image</small>"
    }

}


// DELETE SELECTED SECTION
async function deleteSelectedSection() {
    let sectionName = getActiveSectionNameFromDiv();
    let quoteName = quoteNameElement.innerText;

    
    if (sectionName == null || sectionName.trim().length == 0) return

    if (confirm(`Are you sure you want to delete ''${sectionName}?`)) {
        let data_to_post = {
            'quote_name': quoteName.trim(),
            'section_name': sectionName.trim()
        }

        let data = await deleteSectionFromDB(data_to_post)

        if (data && data['deleted'] == true) {
            window.location.href = (`/add_quote_details/${quoteName}`)
        }
    }
}
// END 

// 
async function sectionNameOnClick(clickedBtn) {
    let activeSectionName = getActiveSectionNameFromDiv();
    let clickedSectionName = clickedBtn.innerText;

    if (activeSectionName != clickedSectionName) {
        let quote_name = quoteNameElement.innerText;
        await autoSaveSectionDetails();
        window.location.href = (`/add_quote_details/${quote_name}/no/${clickedSectionName}`)
    }
}


//AUTO SAVE SECTION DETAILS TO DB
// Modified: 23-01-2024
async function autoSaveSectionDetails(goToViewQuote = false, goToIndexPage = false) {
    let curren_section_details = prepareSectionDataToSave()
    let current_section_name = curren_section_details['section_name']
    let quote_name = curren_section_details['quote_name']

    let quote_data_db = {
        'quote_name': "",
        'section_name': "",
        'section_image_full_names': "",
        'section_detail_rows': []
    }

    // Exit if no section name is selected
    if (current_section_name == null || current_section_name.trim().length == 0) {
        window.location.href = (`/index`)
        return
    }

    // get quote data from db
    let data_db = await getQuoteDataFromDB(quote_name);


    // if the current section name is not in the database, it means the secion is new and we will ask users if they want to save it. 
    if (!(data_db['section_names'].includes(current_section_name))) {
        if (confirm(`You have added a new section '${current_section_name}.'\n\nHit Ok to save the new section.`) == true) {
            let quote_id = quote_data_db['quote_id'];
            await saveCurrentSectionDetailsToDB();
            window.location.reload();
            window.location.href = (`/add_quote_details/${quote_name}/"no"/${current_section_name}`);
            return;
        }
    }

    // build new object from data returned from the server
    let section_image_full_names = data_db['all_sections_data'][current_section_name]['section_image_full_names']
    let image_names = ''
    for (let i = 0; i < section_image_full_names.length; i++) {
        image_names += section_image_full_names[i]['image_full_name'] + ";imageSizeId_" + section_image_full_names[i]['image_size_info']['section_image_size_id']
        if (i != section_image_full_names.length - 1) {
            image_names += "|"
        }
    }

    quote_data_db['quote_name'] = data_db["quote_name"]
    quote_data_db['section_name'] = data_db['section_names'].includes(current_section_name) ? current_section_name : ""
    quote_data_db['section_image_full_names'] = image_names
    quote_data_db['section_detail_rows'] = data_db['section_names'].includes(current_section_name) ? data_db['all_sections_data'][current_section_name]['section_detail_rows'] : []

    // Compare the section details rows to check if any changes were made.
    let altered_section = false

    if (altered_section == false && curren_section_details['section_image_full_names'] == quote_data_db['section_image_full_names']) {
        altered_section = false
    } else {
        altered_section = true
    }

    if (altered_section == false && curren_section_details['section_detail_rows'].length == quote_data_db['section_detail_rows'].length) {
        for (let i = 0; i < curren_section_details['section_detail_rows'].length; i++) {
            if (curren_section_details['section_detail_rows'][i]['section_sub_heading'] != quote_data_db['section_detail_rows'][i]['section_sub_heading']) {
                altered_section = true
                break
            }
            else if (curren_section_details['section_detail_rows'][i]['section_image_row'] != quote_data_db['section_detail_rows'][i]['section_image_row']) {
                altered_section = true
                break
            }
            else if (curren_section_details['section_detail_rows'][i]['section_text'] != quote_data_db['section_detail_rows'][i]['section_text']) {
                altered_section = true
                break
            }
            else if (curren_section_details['section_detail_rows'][i]['section_qty_row'] != quote_data_db['section_detail_rows'][i]['section_qty_row']) {
                altered_section = true
                break
            }
            else if (curren_section_details['section_detail_rows'][i]['section_unit_cost_row'] != quote_data_db['section_detail_rows'][i]['section_unit_cost_row']) {
                altered_section = true
                break
            }
            else if (curren_section_details['section_detail_rows'][i]['section_total_cost_row'] != quote_data_db['section_detail_rows'][i]['section_total_cost_row']) {
                altered_section = true
                break
            }
        }
    } else {
        altered_section = true
    }

    //Save the changes to db
    if (altered_section) {
        if (confirm(`You have made changes to the section '${current_section_name}.'\n\nHit Ok to save the changes.`) == true) {
            await saveCurrentSectionDetailsToDB()
        }
    }

    // Stay on same page or go to index page or view quote page
    if (goToIndexPage) window.location.href = (`/index`);
    if (goToViewQuote) window.location.href = (`/view_quote/${quote_name}`)

}



// SAVE SECTION DETAIL TO DB
async function saveCurrentSectionDetailsToDB() {
    let sectionName = getActiveSectionNameFromDiv();
    if (isEmpty(sectionName)) {
        alert("Select a section name!");
        return;
    }

    toggleMessageModal("Saving data!", true);

    let data_to_post = prepareSectionDataToSave();

    // console.log(data_to_post);

    let data = await saveSectionDetailsInDB(data_to_post);

    if (data['saved'] == true) {
        // Add the new section name to "section Names Div" if it does not exist already in the "section Names Div"
        let selectedSectionNames = getSelectedSectionNamesFromDiv()

        if (!selectedSectionNames.includes(sectionName)) {
            addNewSectionNameBtnToDiv(sectionName);
        }
    }
    else {
        alert("Data not saved. Try again!")
    }

    toggleMessageModal("", false);

}





function addNewSectionNameBtnToDiv(sectionName) {
    let newSectionNameBtn = buildHTMLforSectionNameBtn(sectionName);

    sectionNamesDiv.insertAdjacentHTML('beforeend', newSectionNameBtn);
    unHideElement(saveSectionBtn);
    unHideElement(deleteSectionBtn);
    unHideElement(copyCurrentSectionBtn);
    if (getSelectedSectionNamesFromDiv().length > 1) unHideElement(reorderSectionsBtn);

    addActiveStyleToSectionName(sectionName);

}

function addActiveStyleToSectionName(sectionName) {
    let sectionNamesDivBtns = getSectionNameButtonsFromDiv()
    // change color of the selected section or the newly added section
    for (let i = 0; i < sectionNamesDivBtns.length; i++) {
        if (sectionNamesDivBtns[i].innerText == sectionName) {
            sectionNamesDivBtns[i].classList.add('btn-dark')
        } else {
            sectionNamesDivBtns[i].classList.remove('btn-dark')
            sectionNamesDivBtns[i].classList.add('text-dark')
            sectionNamesDivBtns[i].classList.add('underline')
        }
    }
}


function prepareSectionDataToSave(isNewSection = false) {
    let sectionDetailsData = {}
    // create data to post to flask app which will then save in the db
    sectionDetailsData["quote_name"] = quoteNameElement.innerText
    sectionDetailsData["section_name"] = (isNewSection) ? "" : getActiveSectionNameFromDiv();
    sectionDetailsData["section_image_full_names"] = getSectionImageFullNames(isNewSection);
    sectionDetailsData["section_detail_rows"] = getSectionDetailRows(isNewSection);

    return sectionDetailsData
}

function getSectionImageFullNames(isNewSection = false) {
    let section_image_full_names = ""

    if (!isNewSection) {
        let imgContainerDivs = quoteImageDiv.getElementsByClassName('img-container')
        if (imgContainerDivs.length != 0) {
            for (let i = 0; i < imgContainerDivs.length; i++) {
                let quoteImageTag = imgContainerDivs[i].getElementsByTagName('img')[0]
                let imgFullName = quoteImageTag.getAttribute('src').split('/').pop()

                let imgSizeSelectTag = imgContainerDivs[i].getElementsByTagName('select').length > 0 ? imgContainerDivs[i].getElementsByTagName('select')[0] : ''
                let sectionImageSizeId = imgSizeSelectTag != '' ? imgSizeSelectTag.options[imgSizeSelectTag.selectedIndex].value : 0

                // finally concat image names and image size id
                section_image_full_names += `${imgFullName};imageSizeId_${sectionImageSizeId}`
                if (i != imgContainerDivs.length - 1) {
                    section_image_full_names += "|"
                }
            }
        }
    }
    return section_image_full_names
}




function getSectionDetailRows(isNewSection = false) {
    let sectionDetailRowData = [];
    let sectionRowInfo = {
        "section_sub_heading": "",
        "section_image_row": "",
        "section_text": "",
        "section_qty_row": 0,
        "section_unit_cost_row": 0,
        "section_total_cost_row": 0
    }

    if (isNewSection) {
        sectionDetailRowData.push(sectionRowInfo);
    }
    else {
        let sectionDetailRows = sectionDetailsDiv.getElementsByClassName('section_detail_row')

        for (var row of sectionDetailRows) {
            let inputs = row.getElementsByTagName('input');

            sectionRowInfo = {
                "section_sub_heading": inputs[0].value,
                "section_image_row": inputs[1].value,
                "section_text": inputs[2].value,
                "section_qty_row": inputs[3].value.trim().length == 0 ? 0 : parseInt(inputs[3].value),
                "section_unit_cost_row": inputs[4].value.trim().length == 0 ? 0 : parseFloat(inputs[4].value),
                "section_total_cost_row": inputs[3].value.trim().length != 0 && inputs[4].value.trim().length != 0 ? (parseInt(inputs[3].value) * parseFloat(inputs[4].value)) : 0
            }

            sectionDetailRowData.push(sectionRowInfo);
        }

    }

    return sectionDetailRowData
}





// BUTTONS TO ADD TEXT, IMAGE AND EZE ORDER TEXT
function showAddImageDiv() {
    let ImageSearchInput = imageSearchDiv.querySelector("#image_search_input")
    hideUploadImageDiv()
    ImageSearchInput.value = ''
    addImageBtn.classList.add('btn-dark')
    unHideElement(addImageDiv)
    addTextBtn.classList.remove('btn-dark')
    hideElement(addTextDiv)
    addEoTextBtn.classList.remove('btn-dark')
    hideElement(addEoExcelTextDiv)
}

function showAddTextDiv() {
    textSearchInput.value = ''
    addTextBtn.classList.add('btn-dark')
    unHideElement(addTextDiv);
    addImageBtn.classList.remove('btn-dark')
    hideElement(addImageDiv);
    addEoTextBtn.classList.remove('btn-dark')
    hideElement(addEoExcelTextDiv);
}

function showAddEoTextDiv() {
    hideUploadEoExcelDiv()
    eoExcelTextSearchInput.value = ''
    addEoTextBtn.classList.add('btn-dark')
    unHideElement(addEoExcelTextDiv)
    addTextBtn.classList.remove('btn-dark')
    hideElement(addTextDiv);
    addImageBtn.classList.remove('btn-dark')
    hideElement(addImageDiv);

}
// END 


// ADD TEXT EVENT FUNCTIONS
async function saveTextToDb(section_detail_row_id, section_text_input_name) {
    let currentSectionDetailRow = sectionDetailsDiv.querySelector("#" + section_detail_row_id)
    let currentSectionTextInput = currentSectionDetailRow.querySelector(`input[name = ${section_text_input_name} ]`)
    let textToSaveToDb = currentSectionTextInput.value

    if (textToSaveToDb.trim().length == 0) return

    let data_to_post = {
        "text": textToSaveToDb
    }

    let data = await saveTextInDB(data_to_post);
    if (data && data["saved"]) {
        refreshTextResultDiv()
    }
    else {
        alert(`\nText already saved!`)
    }

}

// delete frequently used text from db
async function deleteFrequentlyUsedText(deleteTextTag) {
    let textId = deleteTextTag.getAttribute('data-text_id')
    let textLiId = deleteTextTag.getAttribute('data-text_li_id')

    if (confirm(`Are you sure you want to delete text?`) == true) {

        let data_to_post = {
            "text_id": textId
        }

        let data = await deleteFrequentlyUsedTextFromDB(data_to_post);

        if (data && data['deleted'] == true) {
            let liToDelete = textDisplayDiv.querySelector(` ul li#${textLiId}`)
            liToDelete.remove()
        }

    }
}

// delete saved text
async function deleteTextDb(deleteTextTag) {
    let textId = deleteTextTag.getAttribute('data-text_id')
    let textLiId = deleteTextTag.getAttribute('data-text_li_id')

    if (confirm(`Are you sure you want to delete text?`) == true) {
        let data_to_post = {
            "text_id": textId
        }

        let data = await deleteTextFromDB(data_to_post);

        if (data && data['deleted'] == true) {
            let liToDelete = textDisplayDiv.querySelector(` ul li#${textLiId}`)
            liToDelete.remove()
        }
    }
}



async function refreshTextResultDiv() {
    textULblock.innerHTML = '';
    frequentlyUsedTextUlBlock.innerHTML = ''
    textSearchInput.value = ''

    // Get texts by current user from db
    let data1 = await getTextsByCurrentUserFromDB();
    // fetch frequently used texts by current user from db
    let data2 = await getFrequentlyUsedTextsByCurrentUserFromDB();

    if (data1.length > 0) {
        textULblock.innerHTML = '<small class="bold">Saved texts</small>';
        data1.forEach(text => {

            let textLi = `<li class="mb-1" id="text_li_id_${text['text_id']}">
                        <span class="pr-1" onclick="addTextToQuoteDetail(this.id)" id="text_id_${text['text_id']}">${text['text']}</span> 
                        <small class="bold text-danger  p-1 rounded"  id="delete_text" data-text_li_id ="text_li_id_${text['text_id']}" data-text_id="${text['text_id']}" onclick="deleteTextDb(this)">Delete</small>
                    </li>`
            textULblock.insertAdjacentHTML('beforeend', textLi);
        })
    }

    if (data2.length > 0) {
        frequentlyUsedTextUlBlock.innerHTML = '<small class="bold">Frequently used texts</small>';
        data2.forEach(text => {
            let textLi = `<li class="mb-1" id="frequently_used_text_li_id_${text['id']}">
                            <span class="pr-1" onclick="addTextToQuoteDetail(this.id)" id="frequently_used_text_id_${text['id']}">${text['text']}</span> 
                            <small class="bold text-danger  p-1 rounded"  id="delete_text" data-text_li_id ="frequently_used_text_li_id_${text['id']}" data-text_id="${text['id']}" onclick="deleteFrequentlyUsedText(this)">Remove</small>
                        </li>`
            frequentlyUsedTextUlBlock.insertAdjacentHTML('beforeend', textLi);
        })
    }


}

// search texts using enter key
if (textSearchInput != null) {
    textSearchInput.onkeyup = (e) => getSearchedTextsFromDb();
}

async function getSearchedTextsFromDb() {
    let filter_str = textSearchInput.value

    // exit if the search_str is empty
    if (filter_str.trim().length == 0) {
        refreshTextResultDiv()
        return
    }
    else if (filter_str.includes('/') || filter_str.includes('\\')) {
        return
    }

    let data = await getFilteredTextsFromDB(filter_str);

    textULblock.innerHTML = '<small class="bold">Searched texts</small>';
    frequentlyUsedTextUlBlock.innerHTML = ''
    if (data.length > 0) {
        data.forEach(text => {
            let textLi = `<li class="mb-1" id="text_li_id_${text['text_id']}">
                                    <span class="pr-1" onclick="addTextToQuoteDetail(this.id)" id="text_id_${text['text_id']}">${text['text']}</span> 
                                    <small class="bold text-danger  p-1 rounded"  id="delete_text" data-text_li_id ="text_li_id_${text['text_id']}" data-text_id="${text['text_id']}" onclick="deleteTextDb(this)">Delete</small>
                                </li>`

            textULblock.insertAdjacentHTML('beforeend', textLi);
        })
    }
    else {
        let noDataDiv = `<div class="text-red">No texts found!</div>`
        textULblock.innerHTML = noDataDiv;
    }
}


function addTextToQuoteDetail(text_id) {
    // get the add detail input field of the last row of quote details and store in "lastSectionDetailRowInput"
    let sectionDetailRows = sectionDetailsDiv.getElementsByClassName('section_detail_row')
    let sectionDetailRowCount = sectionDetailRows.length
    let lastSectionDetailRow = sectionDetailRows[sectionDetailRowCount - 1]
    let lastSectionDetailRowIdNo = lastSectionDetailRow.id.split("_").pop()
    let lastSectionDetailTextInput = lastSectionDetailRow.querySelector(`input[name = section_text_row_${lastSectionDetailRowIdNo} ]`)

    // get text of the clicked li element
    let textToAddToQuote = textDisplayDiv.querySelector(` ul li span#${text_id}`).innerText

    // if the field is empty we will add text automatically
    if (lastSectionDetailTextInput.value == "") {
        lastSectionDetailTextInput.value = textToAddToQuote
    }
    else {
        addNewSectionDetailsRowAtEnd();
        // Because we added a new row we have to get the input field of the new row
        let sectionDetailRows = sectionDetailsDiv.getElementsByClassName('section_detail_row')
        let sectionDetailRowCount = sectionDetailRows.length
        let lastSectionDetailRow = sectionDetailRows[sectionDetailRowCount - 1]
        let lastSectionDetailRowIdNo = lastSectionDetailRow.getAttribute('id').split("_").pop()
        let lastSectionDetailTextInput = lastSectionDetailRow.querySelector(`input[name = section_text_row_${lastSectionDetailRowIdNo} ]`)

        // And update its value
        lastSectionDetailTextInput.value = textToAddToQuote
    }

    // we will add the selected text to frequently used table in the database. If it exists already, we will increase the count
    let data_to_post = {
        "text": textToAddToQuote
    }

    addTextToFrequentlyUsedTextInDB(data_to_post)
}

// END -ADD TEXT EVENT FUNCTIONS



//  ADD IMAGE EVENT FUNCTIONS

async function deleteImage(deleteBtn) {
    let imageDivId = deleteBtn.getAttribute('data-image_div_id')
    let imageId = deleteBtn.getAttribute('data-image_id')

    if (confirm(`Are you sure you want to delete the image?`) == true) {
        let data_to_post = {
            "image_id": imageId
        }

        let data = await deleteImageFromDB(data_to_post);

        if (data && data['deleted'] == true) {
            let imageDivToDelete = imageSearchResultDiv.querySelector('#' + imageDivId)
            imageDivToDelete.remove()
        }
        else {
            alert("Image not deleted! Try refreshing the page and delete again.")
        }
    }

}

function removeFromQuoteImageDiv(removeImageBtn) {
    let divIdData = removeImageBtn.getAttribute("data-div_id")
    let imageDivToDelete = quoteImageDiv.querySelector('#' + divIdData)

    imageDivToDelete.remove()
}


// add image to quote
async function addToQuoteImageDiv(image_info) {
    let imagePath = image_info.getAttribute('data-image_path');
    let imgFullName = imagePath.split('/').pop()
    let imageName = imgFullName.split('.')[0]

    let data = await getAllSectionImageSizesFromDB();
    if (data) {
        let sectionImageSizeInp = ''
        data.forEach(item => sectionImageSizeInp += `<option value="${item['section_image_size_id']}">${item['section_image_size_name']}</option>`)

        let quoteImage = `  <div class="m-1 mb-2 d-inline-block img-container" id="${imageName}">
                <img src="/static/${imagePath}" max-width="100%" height="120px" alt="${imageName}">
                <p class="img-container-text">${imageName}</p>
                <button type="button" class="img-container-btn-delete"  data-div_id ="${imageName}"   onclick="removeFromQuoteImageDiv(this)">x</button>
                <div id="section_image_size_div">
                    <select class="border border-0 bold bg-lightgray pl-1 pt-1 pb-1 pr-0">
                        ${sectionImageSizeInp}
                    </select>
                </div>
            </div>`


        // Add image to row image input if the row image input field is selected
        if (globalVar.activeSectionRowImageInpName != null) {
            let sectionRowImageInp = sectionDetailsDiv.querySelector(`input[name = ${globalVar.activeSectionRowImageInpName} ]`);

            console.log(globalVar.activeSectionRowImageInpName);

            sectionRowImageInp.value = imgFullName
            sectionRowImageInp.style.backgroundColor = 'white'
            globalVar.clickedAddRemoveRowImgBtn.innerHTML = "<small class='text-red'>-Image</small>"

            // set the global variable to null to allow adding only one image
            globalVar.activeSectionRowImageInpName = null
            globalVar.clickedAddRemoveRowImgBtn = null
        }
        // else insert the image at the bottom of the section
        else {

            quoteImageDiv.insertAdjacentHTML('beforeend', quoteImage);
        }
    }
    else {
        alert("Something went wrong!\nPlease refresh and try again!")
    }

}


// search images when enter key is pressed
if (page_path.includes('add_quote_details')) {
    imageSearchDiv.querySelector("#image_search_input").addEventListener("keyup", function (event) {
        // if (event.key == "Enter") {
        //     getSearchedImagesFromDb();
        // }
        getSearchedImagesFromDb();
    });
}

async function getSearchedImagesFromDb() {
    let tagNameRadioInps = imageTagNameDiv.querySelectorAll(`input[name = image_tag_name ]`)
    tagNameRadioInps[0].checked = true ? tagNameRadioInps.length > 0 : ''

    let ImageSearchInput = imageSearchDiv.querySelector("#image_search_input")
    let search_str = ImageSearchInput.value

    // exit if the search_str is empty
    if (search_str.trim().length == 0) {
        refreshImageResultDiv()
        return
    }
    else if (search_str.includes('/') || search_str.includes('\\')) {
        return
    }

    let data = await getFilteredImagesFromDB(search_str);
    // we will remove the content of the div "imageSearchResultDiv" before adding the new contents
    imageSearchResultDiv.innerHTML = '';
    if (data.length > 0) {

        data.forEach(image => {
            let imageDiv = `<div class="m-1 mb-2 d-inline-block img-container" id="image_div_id_${image['image_id']}">
                                <img src="/static/${image['image_path']}" class="equal-size-imgage" alt="${image['image_full_name']}">
                                <button type="button" class="   img-container-btn"  data-image_path ="${image['image_path']}"  onclick="addToQuoteImageDiv(this)">+</button>
                                <button type="button" class="img-container-btn-delete" data-image_div_id="image_div_id_${image['image_id']}" data-image_id="${image['image_id']}" onclick="deleteImage(this)">-</button>
                                <p class="img-container-text">${image['image_name_lower_no_ext']}</p>
                            </div>`

            imageSearchResultDiv.insertAdjacentHTML('beforeend', imageDiv);
        })
    }
    else {
        let noDataDiv = `<div class="text-red">No Images Found!</div>`
        imageSearchResultDiv.innerHTML = noDataDiv;
    }

}


// get filtered images by tag name
async function showImageByTagName(selectedRadioInp) {
    let ImageSearchInput = imageSearchDiv.querySelector("#image_search_input")
    ImageSearchInput.value = ''
    let selectedRadioInpId = selectedRadioInp.id.trim().toLowerCase()
    let imageTagId = selectedRadioInpId.split("_").pop()

    if (parseInt(imageTagId) == 0) {
        refreshImageResultDiv()
    }
    else {

        let data = await getFilteredImagesByTagFromDB(imageTagId);
        if (data) {
            // we will remove the content of the div "imageSearchResultDiv" before adding them again
            imageSearchResultDiv.innerHTML = '';
            data.forEach(image => {
                let imageDiv = `<div class="m-1 mb-2 d-inline-block img-container" id="image_div_id_${image['image_id']}">
                            <img src="/static/${image['image_path']}" class="equal-size-imgage" alt="${image['image_full_name']}">
                            <button type="button" class="   img-container-btn"  data-image_path ="${image['image_path']}"  onclick="addToQuoteImageDiv(this)">+</button>
                            <button type="button" class="img-container-btn-delete" data-image_div_id="image_div_id_${image['image_id']}" data-image_id="${image['image_id']}" onclick="deleteImage(this)">-</button>
                            <p class="img-container-text">${image['image_name_lower_no_ext']}</p>
                        </div>`

                imageSearchResultDiv.insertAdjacentHTML('beforeend', imageDiv);

            });
        }

    }

}


// refresh image result div
async function refreshImageResultDiv() {

    let tagNameRadioInps = imageTagNameDiv.querySelectorAll(`input[name = image_tag_name ]`)
    tagNameRadioInps[0].checked = true ? tagNameRadioInps.length > 0 : ''

    let ImageSearchInput = imageSearchDiv.querySelector("#image_search_input")
    ImageSearchInput.value = ''

    let data = await getAllImagesFromDB()

    if (data) {
        // we will remove the content of the div "imageSearchResultDiv" before adding them again
        imageSearchResultDiv.innerHTML = '';
        data.forEach(image => {
            let imageDiv = `<div class="m-1 mb-2 d-inline-block img-container" id="image_div_id_${image['image_id']}">
                                <img src="/static/${image['image_path']}" class="equal-size-imgage" alt="${image['image_full_name']}">
                                <button type="button" class="   img-container-btn"  data-image_path ="${image['image_path']}"  onclick="addToQuoteImageDiv(this)">+</button>
                                <button type="button" class="img-container-btn-delete" data-image_div_id="image_div_id_${image['image_id']}" data-image_id="${image['image_id']}" onclick="deleteImage(this)">-</button>
                                <p class="img-container-text">${image['image_name_lower_no_ext']}</p>
                            </div>`

            imageSearchResultDiv.insertAdjacentHTML('beforeend', imageDiv);

        })
    }
}

// save image to db and folder
async function saveImageInfoToDbAndFolder() {
    let imageTagName = imageTagNameInp.options[imageTagNameInp.selectedIndex].value.trim()
    let allowedImageTypes = ["image/jpg", "image/jpeg", "image/png", "image/webp", "image/svg+xml", "image/avif", "image/gif"];
    let uploadedFiles = imageFileInput.files;
    fileUploadMsgDiv.innerText = "";


    if (imageTagName.length == 0 || imageTagName.includes("--")) {
        alert("Select a tag name for the image!")
        imageTagNameInp.focus()
        return
    }

    if (uploadedFiles.length > 0) {
        let uploadedFile = uploadedFiles[0]
        let fileType = uploadedFile['type'].toLowerCase();

        if (allowedImageTypes.includes(fileType)) {

            let data = await saveImageInfoInDB(uploadedFile, imageTagName)

            if (data) {
                if (data["uploaded"]) {
                    fileUploadMsgDiv.innerText = "File Uploaded"
                    refreshImageResultDiv()
                }
                else {
                    fileUploadMsgDiv.innerText = "File not Uploaded.. Please rename the file and upload again."
                }
            }
            else {
                fileUploadMsgDiv.innerText = "File not Uploaded. Try again."
            }

            formImgUpload.reset()
        }
        else {
            formImgUpload.reset()
            fileUploadMsgDiv.innerText = "File not Uploaded.. You can upload .jpg, .jpeg and .png file types only.";
        }
    }
}

function showUploadImageDiv() {
    let ImageSearchInput = imageSearchDiv.querySelector("#image_search_input")
    ImageSearchInput.value = ''
    fileUploadMsgDiv.innerText = ""
    formImgUpload.reset()
    uploadImageDiv.classList.remove('hide')
    showUploadImageBtn.classList.add('hide')
    imageSearchDiv.classList.add('hide')
    imageSearchResultDiv.classList.add('hide')
    imageTagNameDiv.classList.add('hide')
}

function hideUploadImageDiv() {
    uploadImageDiv.classList.add('hide')
    showUploadImageBtn.classList.remove('hide')
    imageSearchDiv.classList.remove('hide')
    imageSearchResultDiv.classList.remove('hide')
    imageTagNameDiv.classList.remove('hide')
}


//  END -ADD IMAGE EVENT FUNCTIONS


// ADD EO TEXT FUNCTION
function showUploadEoExcelDiv() {
    // let ImageSearchInput = imageSearchDiv.querySelector("#image_search_input")
    // ImageSearchInput.value = ''
    // fileUploadMsgDiv.innerText = ""
    // formImgUpload.reset()
    eoExcelFileUploadMsgDiv.innerText = ''
    uploadEoExcelDiv.classList.remove('hide')
    showUploadEoExcelBtn.classList.add('hide')
    eoExcelTextSerachDiv.classList.add('hide')
    eoExcelTextResultDiv.classList.add('hide')
}

function hideUploadEoExcelDiv() {
    uploadEoExcelDiv.classList.add('hide')
    showUploadEoExcelBtn.classList.remove('hide')
    eoExcelTextSerachDiv.classList.remove('hide')
    eoExcelTextResultDiv.classList.remove('hide')
}

async function saveEoExcelFileToDb(saveBtn) {
    let user_id = saveBtn.getAttribute('data-user_id')
    let allowedExcelFileTypes = ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
    let uploadedFiles = eoExcelFileInput.files;
    eoExcelFileUploadMsgDiv.innerText = "";

    if (uploadedFiles.length > 0) {
        let uploadedFile = uploadedFiles[0]
        let fileType = uploadedFile['type'].toLowerCase();


        if (allowedExcelFileTypes.includes(fileType)) {
            let data = await saveEOexcelFileInDB(uploadedFile, user_id)
            if (data) {
                if (data["uploaded"] == true) {
                    eoExcelFileUploadMsgDiv.innerText = data['message']
                    refreshEoExcelTextResultDiv()
                }
                else {
                    eoExcelFileUploadMsgDiv.innerText = data['message']
                }
            }
            else {
                eoExcelFileUploadMsgDiv.innerText = "File not Uploaded. Try again."
            }

        }
        else {
            formEoExcelUpload.reset()
            eoExcelFileUploadMsgDiv.innerText = "The uploaded filetype is not supported. Make sure you upload only the excel files generated from Eze Order program.";

        }
    }
}


function addEoTextToQuoteDetail(eoTextId) {
    // get the add detail input field of the last row of quote details and store in "lastSectionDetailRowInput"
    let sectionDetailRows = sectionDetailsDiv.getElementsByClassName('section_detail_row')
    let sectionDetailRowCount = sectionDetailRows.length
    let lastSectionDetailRow = sectionDetailRows[sectionDetailRowCount - 1]
    let lastSectionDetailRowIdNo = lastSectionDetailRow.getAttribute('id').split("_").pop()
    let lastSectionDetailTextInput = lastSectionDetailRow.querySelector(`input[name = section_text_row_${lastSectionDetailRowIdNo} ]`)

    // get text of the clicked li element
    let textToAddToQuote = eoExcelTextResultDiv.querySelector(` ul li span#${eoTextId}`).innerText

    // if the add detial field is empty we will add text automatically
    if (lastSectionDetailTextInput.value == "") {
        lastSectionDetailTextInput.value = textToAddToQuote
    }
    else {
        addNewSectionDetailsRowAtEnd();
        // Because we added a new row we have to get the input field of the new row
        let sectionDetailRows = sectionDetailsDiv.getElementsByClassName('section_detail_row')
        let sectionDetailRowCount = sectionDetailRows.length
        let lastSectionDetailRow = sectionDetailRows[sectionDetailRowCount - 1]
        let lastSectionDetailRowIdNo = lastSectionDetailRow.getAttribute('id').split("_").pop()
        let lastSectionDetailTextInput = lastSectionDetailRow.querySelector(`input[name = section_text_row_${lastSectionDetailRowIdNo} ]`)

        // And update its value
        lastSectionDetailTextInput.value = textToAddToQuote
    }

    // we will add the selected text to frequently used table in the database. If it exists already, we will increase the count
    let data_to_post = {
        "text": textToAddToQuote
    }

    addTextToFrequentlyUsedTextInDB(data_to_post)
}

if (eoExcelTextSearchInput != null) {
    eoExcelTextSearchInput.onkeyup = (e) => getSearchedEoExcelTextFromDb();
}

async function getSearchedEoExcelTextFromDb() {
    let search_str = eoExcelTextSearchInput.value
    let user_id = eoExcelTextSearchInput.getAttribute('data-user_id')

    if (search_str.trim().length == 0) {
        refreshEoExcelTextResultDiv();
        return;
    }

    let data = await getFilteredEOexcelTextsFromDB(user_id, search_str)

    // we will remove the content  before adding the new contents
    eoExcelTextUlBlock.innerHTML = '';
    if (data.length > 0) {
        data.forEach(text => {
            let textLi = ` <li class="mb-1" id="eo_excel_text_li_id_${text['id']}">
                                 <span class="pr-1" onclick="addEoTextToQuoteDetail(this.id)" id="eo_text_id_${text['id']}">${text['text']}</span> 
                             </li>`
            eoExcelTextUlBlock.insertAdjacentHTML('beforeend', textLi);
        })
    }
    else {
        let noDataDiv = `<div class="text-red">No texts found!</div>`
        eoExcelTextUlBlock.innerHTML = noDataDiv;
    }
}


async function refreshEoExcelTextResultDiv() {
    let user_id = eoExcelTextSearchInput.getAttribute('data-user_id')
    eoExcelTextSearchInput.value = ''
    let data = await getEOexcelTextsByCurrentUserFromDB(user_id);
    if (data) {
        // we will remove the content  before adding the new contents
        eoExcelTextUlBlock.innerHTML = '';

        data.forEach(text => {
            // let textLi = `<li class="mb-1 " onclick="addEoTextToQuoteDetail(this.id)" id="eo_excel_text_li_${text['id']}">${text['text']}</li>`
            let textLi = ` <li class="mb-1" id="eo_excel_text_li_id_${text['id']}">
                                    <span class="pr-1" onclick="addEoTextToQuoteDetail(this.id)" id="eo_text_id_${text['id']}">${text['text']}</span> 
                                </li>`
            eoExcelTextUlBlock.insertAdjacentHTML('beforeend', textLi);
        })
    }
}





// Add empty template for adding new section details
function addEmptySectionDetailsRowTemplate() {
    let newSectionDetailRow = buildHTMLforNewSectionDetailRow(true);
    sectionDetailsDiv.innerHTML = newSectionDetailRow;
}

// insert new row at the end
function addNewSectionDetailsRowAtEnd() {
    let newSectionDetailRow = buildHTMLforNewSectionDetailRow();
    sectionDetailsDiv.insertAdjacentHTML('beforeend', newSectionDetailRow);
}

// insert new row below a row
function addNewSectionDetailsRowBelow(section_detail_row_id) {
    let currentSectionDetailRow = sectionDetailsDiv.querySelector("#" + section_detail_row_id)
    let newSectionDetailRow = buildHTMLforNewSectionDetailRow();
    currentSectionDetailRow.insertAdjacentHTML('afterend', newSectionDetailRow);
}

function buildHTMLforNewSectionDetailRow(isNewSection = false) {
    let new_row_no = 0;

    if (!isNewSection) {
        let sectionDetailRows = sectionDetailsDiv.getElementsByClassName('section_detail_row')
        let sectionDetailRowIDs = [];
        for (var row of sectionDetailRows) {
            let rowId = row.id.trim().split("_").pop()
            sectionDetailRowIDs.push(parseInt(rowId));
        }
        new_row_no = Math.max(...sectionDetailRowIDs) + 1; // genereate a new row id for new element we are about to add
    }

    return ` <div class="form-row section_detail_row mb-2" id="section_detail_row_${new_row_no}">
                <div class="col-md-1">
                    <input type="text" class="form-control form-control-sm" name="section_sub_heading_${new_row_no}" autocomplete="off">
                </div>

                <div class="col-md-1">
                    <input type="text" class="form-control form-control-sm" name="section_image_row_${new_row_no}" autocomplete="off" readonly tabindex="-1">
                </div>

                <div class="col-md-6">
                    <input type="text" class="form-control form-control-sm" name="section_text_row_${new_row_no}" autocomplete="off" >
                </div>

                <div class="col-md-1">
                    <input type="number" class="form-control form-control-sm" name="section_qty_row_${new_row_no}" autocomplete="off">
                </div>

                <div class="col-md-1">
                    <input type="number" class="form-control form-control-sm" name="section_unit_cost_row_${new_row_no}" autocomplete="off" > 
                </div>

                <div class=" col-md-2 bg-light d-flex justify-content-center px-0 ">
                    <button type="button" class="btn btn-sm btn-link px-1 " name="add_remove_row_image_btn_${new_row_no}" data-img_inp_name="section_image_row_${new_row_no}" onclick="addRemoveRowImage(this)" tabindex="-1"><small>+Image</small></button>
                    <button type="button" class="btn btn-sm btn-link px-1 " onclick="saveTextToDb('section_detail_row_${new_row_no}' , 'section_text_row_${new_row_no}')" tabindex="-1"><small>Save text</small></button>
                    <button type="button" class="btn btn-sm btn-link px-1 " onclick="addNewSectionDetailsRowBelow('section_detail_row_${new_row_no}')" tabindex="-1"><small>+Row</small></button>
                    <button type="button" class="btn btn-sm btn-link px-1  text-red" onclick="removeSectionDetailsRow('section_detail_row_${new_row_no}')" tabindex="-1"><small>-Row</small></button>
                </div>

            </div> ` ;
}



function removeSectionDetailsRow(section_detail_row_id) {
    let sectionDetailRowCount = sectionDetailsDiv.getElementsByClassName('section_detail_row').length;
    let currentRow = document.getElementById(section_detail_row_id)

    if (sectionDetailRowCount == 1) {
        alert("\nPlease add a new row before deleting the current row!");
        return;
    }

    // delete selected row if all of its inputs are empty, otherewise prompt user to delete or cancel. 
    let currentRowInps = currentRow.getElementsByTagName('input')
    let inpValues = ''
    for (let i = 0; i < currentRowInps.length; i++) {
        inpValues += currentRowInps[i].value.trim()
    }

    if (inpValues.length == 0) {
        currentRow.remove();
    }
    else {
        if (confirm("\nAre you sure you want to remove the row?") == true) {
            currentRow.remove();

        }
    }


}

// ADD QUOTE INFORMATION