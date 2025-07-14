
/*------------ Variables -------------------------------------------------------*/

let productTypeOptions = document.getElementById('product_type_options');
let productOptions = document.getElementById('product_options');
let productPartsDiv = document.getElementById('product_parts_div')
let partDetailsDiv = document.getElementById('part_details_div')
let btnLoadEditProductPartsModal = document.getElementById("btn_load_edit_product_parts_modal");

let cnccodeDetailsDiv = document.getElementById("cnccode_details_div")
let cnccodeNameTag = document.getElementById("cnccode_name")
let cnccodeDescriptionTextArea = document.getElementById("cnccode_description")
let cnccodeParametersDiv = document.getElementById("cnccode_parameters")
let cnccodeImagesDiv = document.getElementById("cnccode_images")

let parameterDetailsDiv = document.getElementById("parameter_details_div")
let parameterNameTag = document.getElementById("parameter_name")
let parameterDescriptionTextArea = document.getElementById("parameter_description")

let parameterValuesDiv = document.getElementById("parameter_values")
let parameterImagesDiv = document.getElementById("parameter_images")



/*------------ Events -------------------------------------------------------*/

async function productTypeOnChange() {
    let selectedProductTypeId = productTypeOptions.options[productTypeOptions.selectedIndex].value;
    let products = (GlobalVariablesCP.Products.length > 0) ? GlobalVariablesCP.Products : await getAllProductsFromDB();
    let filteredProducts = filterProductsByProductTypeId(products, selectedProductTypeId);
    populateProducts(filteredProducts);
}

async function productOnChange() {
    let selectedProductId = productOptions.options[productOptions.selectedIndex].value;

    let productInfo = await getProductInfoFromDB(selectedProductId)
    GlobalVariablesCP.SelectedProductInfo = productInfo;
    populateProductParts(productInfo)
}

async function cnccodeOnClick(cnccodeTag) {
    let cnccodeId = cnccodeTag.id;
    let cnccodeInfo = await getCnccodeInfoFromDB(cnccodeId);
    GlobalVariablesCP.SelectedCnccodeInfo = cnccodeInfo
    populateCncCodeDetails(cnccodeInfo);
}

async function parameterOnClick(paramaterTag) {
    let parameterId = paramaterTag.id;
    let parameterInfo = await getParameterInfoFromDB(parameterId);
    GlobalVariablesCP.SelectedParameterInfo = parameterInfo
    populateParameterDetails(parameterInfo);
}

function imageOnClick(imageTag) {
    let imageName = imageTag.innerText;
    let imagePath = imageTag.dataset.image_path;
    showImageModal(true, imageName, imagePath);
}

/*------------ Functions -------------------------------------------------------*/

function hideCPhomeDivs(hideCnccodeDetailsDiv, hideParameterDetailsDiv) {
    (hideCnccodeDetailsDiv) ? cnccodeDetailsDiv.classList.add("hide") : cnccodeDetailsDiv.classList.remove("hide");
    (hideParameterDetailsDiv) ? parameterDetailsDiv.classList.add("hide") : parameterDetailsDiv.classList.remove("hide");
}


function populateProducts(filteredProducts) {
    GlobalVariablesCP.SelectedProductInfo = {}; //Reset selected product info because there will not be any product seleted at this point.
    partDetailsDiv.innerHTML = ""; // Clear the partDetailsDiv
    hideElement(btnLoadEditProductPartsModal); //Hide the edit prodcut parts btn
    hideCPhomeDivs(true, true)

    let options = "<option> </option>"
    filteredProducts.forEach(product => options += `<option value="${product['id']}"> ${product['name']}</option>`);
    productOptions.innerHTML = options;
}


function populateProductParts(productInfo = {}) {
    hideElement(btnLoadEditProductPartsModal); //Hide the edit prodcut parts btn
    partDetailsDiv.innerHTML = "";
    hideCPhomeDivs(true, true);
    if (!isEmpty(productInfo)) {
        unHideElement(btnLoadEditProductPartsModal); //Unhide the edit prodcut parts btn if the selected product has parts.
        let parts = productInfo['parts']
        if (parts.length > 0) {
            parts.forEach(part => {
                let partCncocdes = "";
                let cnccodes = part['cnccodes']

                if (cnccodes.length > 0) {
                    cnccodes.forEach(cnccode => partCncocdes += `<li> <span class="hover-text-bold " id="${cnccode['id']}" onclick="cnccodeOnClick(this)">${cnccode['name']}</span> </li>`);
                }

                let partDetails = ` <div class="row border-bottom py-2 hover-bg-lightgray">
                                    <div class="col-sm-7"> 
                                        <span class="text-dark bold mr-2">${part['name']}</span>
                                        <span class="text-primary d-inline-block cursor-pointer hover-underline hide small" data-part_info='${JSON.stringify(part)}' onclick="LoadEditPartCncCodes(this)" >Edit cncode list</span>
                                    </div>
                                    <div class="col-sm-5  ">
                                         ${partCncocdes} 
                                    </div>
                                </div> `

                partDetailsDiv.insertAdjacentHTML('beforeend', partDetails);

            });
        }
        else {
            partDetailsDiv.innerHTML = `<span class="text-danger font-italic" id="" > </span>`;
        }
    }
}





// Populate CncCode Details Div
function populateCncCodeDetails(cnccodeInfo) {
    // Clear previous data
    cnccodeNameTag.innerText = "";
    cnccodeDescriptionTextArea.innerText = "";
    cnccodeParametersDiv.innerHTML = "";
    cnccodeImagesDiv.innerHTML = "";

    if (!isEmpty(cnccodeInfo)) {
        hideCPhomeDivs(false, true);
        // Update cnccode name 
        cnccodeNameTag.innerText = cnccodeInfo['name']
        // Update description 
        updateCnccodeDescriptionDiv(cnccodeInfo['description']);
        // Update parameter tags
        updateCnccodeParametersDiv(cnccodeInfo['parameters']);
        // Update image tags
        updateCnccodeImagesDiv(cnccodeInfo['images'])

    }
}

function updateCnccodeDescriptionDiv(description) {
    cnccodeDescriptionTextArea.innerHTML = description
}

function updateCnccodeParametersDiv(parameters) {
    hideCPhomeDivs(false,true);
    cnccodeParametersDiv.innerHTML = "";
    if (parameters.length > 0) {
        parameters.forEach(item => {
            let htmlElement = `<span class="bg-dark rounded p-1 px-3 d-inline-block m-1  text-light hover-bg-lightgray hover-text-black cursor-pointer" id="${item['id']}" onclick="parameterOnClick(this)"> ${item['name']} </span>`;
            cnccodeParametersDiv.insertAdjacentHTML('beforeend', htmlElement);
        });
    }
    else {
        // cnccodeParametersDiv.innerHTML = `<span class="text-danger font-italic">No parameters added!</span>`
        cnccodeParametersDiv.innerHTML = `<span class="text-danger font-italic"> </span>`
    }
}

function updateCnccodeImagesDiv(images) {
    cnccodeImagesDiv.innerHTML = "";
    if (images.length > 0) {
        images.forEach(item => {
            let htmlElement = `<span class="bg-light text-dark hover-bg-lightgray rounded p-1 px-3 d-inline-block m-1 cursor-pointer " data-image_path="${item['image_path']}" id="${item['id']}" onclick="imageOnClick(this)"> ${item['name']} </span>`;
            cnccodeImagesDiv.insertAdjacentHTML('beforeend', htmlElement);
        });
    }
    else {
        cnccodeImagesDiv.innerHTML = `<span class="text-danger font-italic"> </span>`
    }

}

// Populate Parameter Details Div
function populateParameterDetails(parameterInfo) {
    // Clear previous data
    parameterNameTag.innerText = "";
    parameterDescriptionTextArea.innerText = "";
    parameterImagesDiv.innerHTML = "";

    if (!isObjectEmpty(parameterInfo)) {
        hideCPhomeDivs(false, false);
        // Update parameter name 
        parameterNameTag.innerText = parameterInfo['name'];
        // Update descriptions
        updateParameterDescriptionDiv(parameterInfo['description'])
        // Update parameter values
        updateParameterValues(parameterInfo['default_value'], parameterInfo['min_value'], parameterInfo['max_value'])
        // Update image tags
        updateParameterImages(parameterInfo['images']);
    }
}

function updateParameterDescriptionDiv(description) {
    parameterDescriptionTextArea.innerHTML = description;
}

function updateParameterValues(defaultVal, minVal, maxVal) {
    parameterValuesDiv.innerHTML = "";
    let valueHtml = "";
    valueHtml += `<span class=" mr-4" >Default value: ${(defaultVal ?? "-")} </span>`;
    valueHtml += `<span class=" mr-4" >Min value: ${(minVal ?? "-")} </span>`;
    valueHtml += `<span class=" mr-4">Max value: ${(maxVal ?? "-")} </span>`;
    parameterValuesDiv.innerHTML = valueHtml;
}

function updateParameterImages(images) {
    parameterImagesDiv.innerHTML = "";
    if (images.length > 0) {
        images.forEach(item => {
            let htmlElement = `<span class="bg-light text-dark hover-bg-lightgray rounded p-1 px-3 d-inline-block m-1 cursor-pointer" data-image_path="${item['image_path']}" id="${item['id']}" onclick="imageOnClick(this)"> ${item['name']} </span>`;
            parameterImagesDiv.insertAdjacentHTML('beforeend', htmlElement);
        });
    }
    else {
        parameterImagesDiv.innerHTML = `<span class="text-danger font-italic"> </span>`
    }
}