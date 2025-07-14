

// JS : Edit CncConde Parameters Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editCnccodeImagesModal   = document.getElementById("edit_cnccode_images_modal");
let selectedCnccodeImagesDiv     = editCnccodeImagesModal.querySelector("#selected_items_div");
let notSelectedCnccodeImagesDiv  = editCnccodeImagesModal.querySelector("#not_selected_items_div");
let saveSelectedCnccodeImagesBtn = editCnccodeImagesModal.querySelector("#save_changes_btn");
let searchCnccodeImagesInput = editCnccodeImagesModal.querySelector("#search_items_input");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

async function closeEditCnccodeImagessModal(){
    if (saveSelectedCnccodeImagesBtn.classList.contains("hide") == false){
        if (confirm("You have made changes.\n\nHit 'OK' to save the changes.") == true){
            await saveSelectedCnccodeImages();
        }
    }
    closeModal(editCnccodeImagesModal.id)
}


function LoadEditCnccodeImages(){
    searchCnccodeImagesInput.value="";
    let currentCnccodeInfo = GlobalVariablesCP.SelectedCnccodeInfo;
    let selectedImages = []
    let notSelectedImages = []
    let AllImages = GlobalVariablesCP.AllImages ;
    hideElement(saveSelectedCnccodeImagesBtn)

    if (!isObjectEmpty(currentCnccodeInfo)) {
        let selectedCnccodeImages = currentCnccodeInfo['images']
        let selectedCnccodeNameTag = editCnccodeImagesModal.querySelector("#selected_cnccode_name");
        selectedCnccodeNameTag.innerText = currentCnccodeInfo['name'];

        openModal(editCnccodeImagesModal.id)
        
        AllImages.forEach(image => {
            let isSelected = selectedCnccodeImages.some(el =>  image['id'] == el['id']);
            (isSelected) ? selectedImages.push(image) : notSelectedImages.push(image)
        });
        updateSelectedImagesDiv(selectedImages);
        updateNotSelectedImagesDiv(notSelectedImages);
    
    }
    
}

function updateSelectedImagesDiv(parameters){
    let html = "";
    parameters.forEach(image => html += buildHtmlForCnccodeImage(image,true) );
    selectedCnccodeImagesDiv.innerHTML = html;
}

function updateNotSelectedImagesDiv(parameters){
    let html = "";
    parameters.forEach(image => html += buildHtmlForCnccodeImage(image,false) );
    notSelectedCnccodeImagesDiv.innerHTML = html;
}


function addImageToCnccode(clickedBtn){
    let clickedImageInfo = JSON.parse(clickedBtn.dataset.image_info);
    let selectedImages = getSelectedCnccodeImagesFromDiv();
    selectedImages.push(clickedImageInfo);
    let sortedArray = sortArrayObjects(selectedImages, "id");
    updateSelectedImagesDiv(sortedArray);
    unHideElement(saveSelectedCnccodeImagesBtn, false);
    // Remove the clicked part from the current list
    clickedBtn.parentNode.remove();
}


function removeImageFromCnccode(clickedBtn){
    let clickedImageInfo = JSON.parse(clickedBtn.dataset.image_info);
    let notSelectedImages = getNotSelectedCnccodeImagesFromDiv();
    notSelectedImages.push(clickedImageInfo);
    let sortedArray = sortArrayObjects(notSelectedImages, "id");
    updateNotSelectedImagesDiv(sortedArray);
    unHideElement(saveSelectedCnccodeImagesBtn);
    // Remove the clicked part from the current list
    clickedBtn.parentNode.remove();
}

function buildHtmlForCnccodeImage(image, isSelected=false){

    if (isSelected){
        return `<li class="hover-text-red cursor-pointer mt-1" data-image_info ='${JSON.stringify(image)}' >
                    <span data-image_info='${JSON.stringify(image)}' onclick="removeImageFromCnccode(this)" >${image['name']} </span>
                </li>` ;
    }
    else{
        return `<li class="hover-text-teal cursor-pointer mt-1 hover-text-bold" data-image_info='${JSON.stringify(image)}' >
                    <span  data-image_info='${JSON.stringify(image)}' onclick="addImageToCnccode(this)" >${image['name']} </span>
                </li>` ;
    }
}

function getSelectedCnccodeImagesFromDiv(){
    let items = [];
    let partsEl = [... selectedCnccodeImagesDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.image_info)) );
    return items;
}

function getNotSelectedCnccodeImagesFromDiv(){
    let items = [];
    let partsEl = [... notSelectedCnccodeImagesDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.image_info)) );
    return items;
}

async function saveSelectedCnccodeImages(){
    hideElement(saveSelectedCnccodeImagesBtn);
    let currentProductInfo  = GlobalVariablesCP.SelectedProductInfo;

    let currentCnccodeInfo = GlobalVariablesCP.SelectedCnccodeInfo
    let selectedImages = getSelectedCnccodeImagesFromDiv();

    let dataToSave = {
        "cnccode_id"    : currentCnccodeInfo['id'],
        "images"        : selectedImages 
    }

    var updated = await updateCnccodeImagesInDB(dataToSave)
    if(updated) {
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id'])
        updateCnccodeImagesDiv(selectedImages)
        GlobalVariablesCP.SelectedProductInfo   = updatedProductInfo
        GlobalVariablesCP.AllCncCodes           = await getAllCncCodesFromDB();
        GlobalVariablesCP.SelectedCnccodeInfo   = await getCnccodeInfoFromDB(currentCnccodeInfo['id'])  
    }
    else{
        alert("Failed to save!")
        unHideElement(saveSelectedCnccodeImagesBtn, false);
    }
}



if (searchCnccodeImagesInput != null){
    searchCnccodeImagesInput.onkeyup = (e) => {
        let searchString = searchCnccodeImagesInput.value.trim().toLowerCase();
        let filteredItems = fileterOutSelectedCnccodeImagesFromAllParts()
        if(!isEmpty(searchString)){
            filteredItems = filteredItems.filter(item => item.name.toLowerCase().startsWith(searchString));
        }
        updateNotSelectedImagesDiv(filteredItems);
    };
}

// This function will remove all the parts present in the selected div from AllParts array, and return the fileterd array of parts
function fileterOutSelectedCnccodeImagesFromAllParts(){
    let notSelectedItems =[];
    let AllImages = GlobalVariablesCP.AllImages ;
    let selectedImages = getSelectedCnccodeImagesFromDiv();

    AllImages.forEach(image => {
        let isSelected = selectedImages.some(selectedImage => image['id'] == selectedImage['id']);
        if(!isSelected) notSelectedItems.push(image)
    });

    return notSelectedItems;
}