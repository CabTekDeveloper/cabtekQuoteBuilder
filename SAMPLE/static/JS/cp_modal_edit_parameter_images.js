

// JS : Edit CncConde Parameters Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editParameterImagesModal   = document.getElementById("edit_parameter_images_modal");
let selectedParameterImagesDiv     = editParameterImagesModal.querySelector("#selected_items_div");
let notSelectedParameterImagesDiv  = editParameterImagesModal.querySelector("#not_selected_items_div");
let saveSelectedParameterImagesBtn = editParameterImagesModal.querySelector("#save_changes_btn");
let searchParameterImagesInput = editParameterImagesModal.querySelector("#search_items_input");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

async function closeEditParameterImagesModal(){
    if (saveSelectedParameterImagesBtn.classList.contains("hide") == false){
        if (confirm("You have made changes.\n\nHit 'OK' to save the changes.") == true){
            await saveSelectedParameterImages();
        }
    }
    closeModal(editParameterImagesModal.id)
}


function LoadEditParameterImages(){
    searchParameterImagesInput.value="";
    let currentParameterInfo = GlobalVariablesCP.SelectedParameterInfo;
    let selectedImages = []
    let notSelectedImages = []
    let AllImages = GlobalVariablesCP.AllImages ;
    hideElement(saveSelectedParameterImagesBtn)

    if (!isObjectEmpty(currentParameterInfo)) {
        let selectedParameterImages = currentParameterInfo['images']
        let selectedParameterNameTag = editParameterImagesModal.querySelector("#selected_parameter_name");
        selectedParameterNameTag.innerText = currentParameterInfo['name'];

        openModal(editParameterImagesModal.id)
        
        AllImages.forEach(image => {
            let isSelected = selectedParameterImages.some(el =>  image['id'] == el['id']);
            (isSelected) ? selectedImages.push(image) : notSelectedImages.push(image)
        });
        updateSelectedParameterImagesDiv(selectedImages);
        updateNotSelectedParameterImagesDiv(notSelectedImages);
    
    }
    
}

function updateSelectedParameterImagesDiv(parameters){
    let html = "";
    parameters.forEach(image => html += buildHtmlForParameterImage(image,true) );
    selectedParameterImagesDiv.innerHTML = html;
}

function updateNotSelectedParameterImagesDiv(parameters){
    let html = "";
    parameters.forEach(image => html += buildHtmlForParameterImage(image,false) );
    notSelectedParameterImagesDiv.innerHTML = html;
}


function addImageToParameter(clickedBtn){
    let clickedImageInfo = JSON.parse(clickedBtn.dataset.image_info);
    let selectedImages = getSelectedParameterImagesFromDiv();
    selectedImages.push(clickedImageInfo);
    let sortedArray = sortArrayObjects(selectedImages, "id");
    updateSelectedParameterImagesDiv(sortedArray);
    unHideElement(saveSelectedParameterImagesBtn);
    // Remove the clicked part from the current list
    clickedBtn.parentNode.remove();
}

function removeImageFromParameter(clickedBtn){
    let clickedImageInfo = JSON.parse(clickedBtn.dataset.image_info);
    let notSelectedImages = getNotSelectedParameterImagesFromDiv();
    notSelectedImages.push(clickedImageInfo);
    let sortedArray = sortArrayObjects(notSelectedImages, "id");
    updateNotSelectedParameterImagesDiv(sortedArray);
    unHideElement(saveSelectedParameterImagesBtn);
    // Remove the clicked part from the current list
    clickedBtn.parentNode.remove();
}

function buildHtmlForParameterImage(image, isSelected=false){
    if (isSelected){
        return `<li class="hover-text-red cursor-pointer mt-1" data-image_info ='${JSON.stringify(image)}' >
                    <span data-image_info='${JSON.stringify(image)}' onclick="removeImageFromParameter(this)" >${image['name']} </span>
                </li>` ;
    }
    else{
        return `<li class="hover-text-teal cursor-pointer mt-1 hover-text-bold" data-image_info='${JSON.stringify(image)}' >
                    <span data-image_info='${JSON.stringify(image)}' onclick="addImageToParameter(this)" >${image['name']} </span>
                </li>` ;
    }
}


function getSelectedParameterImagesFromDiv(){
    let items = [];
    let partsEl = [... selectedParameterImagesDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.image_info)) );
    return items;
}

function getNotSelectedParameterImagesFromDiv(){
    let items = [];
    let partsEl = [... notSelectedParameterImagesDiv.childNodes]
    partsEl.forEach(el => items.push(JSON.parse(el.dataset.image_info)) );
    return items;
}

async function saveSelectedParameterImages(){
    hideElement(saveSelectedParameterImagesBtn);
    let currentProductInfo  = GlobalVariablesCP.SelectedProductInfo;

    let currentParameterInfo = GlobalVariablesCP.SelectedParameterInfo
    let selectedImages = getSelectedParameterImagesFromDiv();

    let dataToSave = {
        "parameter_id"    : currentParameterInfo['id'],
        "images"        : selectedImages 
    }

    var updated = await updateParameterImagesInDB(dataToSave)
    if(updated) {
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id'])
        updateParameterImages(selectedImages)
        GlobalVariablesCP.SelectedProductInfo   = updatedProductInfo
        GlobalVariablesCP.AllParameters = await getAllParameterFromDB();
        GlobalVariablesCP.SelectedParameterInfo   = await getParameterInfoFromDB(currentParameterInfo['id'])  
    }
    else{
        alert("Failed to save!")
        unHideElement(saveSelectedParameterImagesBtn);
    }
}



if (searchParameterImagesInput != null){
    searchParameterImagesInput.onkeyup = (e) => {
        let searchString = searchParameterImagesInput.value.trim().toLowerCase();
        let filteredItems = fileterOutSelectedParameterImagesFromAllParts()
        if(!isEmpty(searchString)){
            filteredItems = filteredItems.filter(item => item.name.toLowerCase().startsWith(searchString));
        }
        updateNotSelectedParameterImagesDiv(filteredItems);
    };
}

// This function will remove all the parts present in the selected div from AllParts array, and return the fileterd array of parts
function fileterOutSelectedParameterImagesFromAllParts(){
    let notSelectedItems =[];
    let AllImages = GlobalVariablesCP.AllImages ;
    let selectedImages = getSelectedParameterImagesFromDiv();

    AllImages.forEach(image => {
        let isSelected = selectedImages.some(selectedImage => image['id'] == selectedImage['id']);
        if(!isSelected) notSelectedItems.push(image)
    });

    return notSelectedItems;
}