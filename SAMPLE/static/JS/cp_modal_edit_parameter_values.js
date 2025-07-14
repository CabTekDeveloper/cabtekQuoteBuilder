

// JS : Edit CncConde Parameters Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let editParameterValuesModal = document.getElementById("edit_parameter_values_modal");
let defaultParameterValueInput = editParameterValuesModal.querySelector("#default_parameter_value_input");
let minParameterValueInput = editParameterValuesModal.querySelector("#min_parameter_value_input");
let maxParameterValueInput = editParameterValuesModal.querySelector("#max_parameter_value_input");
let saveParameterValuesBtn = editParameterValuesModal.querySelector("#save_changes_btn");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

function resetParameterValuesModal() {
    defaultParameterValueInput.value    = "";
    minParameterValueInput.value        = "";
    maxParameterValueInput.value        = "";
    hideElement(saveParameterValuesBtn)
}

function LoadEditParameterValues() {
    let currentParameterInfo = GlobalVariablesCP.SelectedParameterInfo;
    resetParameterValuesModal();

    if (!isEmpty(currentParameterInfo)) {
        openModal(editParameterValuesModal.id);
        let selectedParameterNameTag = editParameterValuesModal.querySelector("#selected_parameter_name");
        selectedParameterNameTag.innerText = currentParameterInfo['name'];
        if(!isEmpty(currentParameterInfo['default_value'])) defaultParameterValueInput.value = currentParameterInfo['default_value']
        if(!isEmpty(currentParameterInfo['min_value']))     minParameterValueInput.value = currentParameterInfo['min_value']
        if(!isEmpty(currentParameterInfo['max_value']))     maxParameterValueInput.value = currentParameterInfo['max_value']
    }
}

if (defaultParameterValueInput != null && minParameterValueInput != null && maxParameterValueInput != null) {
    defaultParameterValueInput.onchange = (e) => unHideElement(saveParameterValuesBtn);
    minParameterValueInput.onchange     = (e) => unHideElement(saveParameterValuesBtn);
    maxParameterValueInput.onchange     = (e) => unHideElement(saveParameterValuesBtn);
}


async function saveParameterValues(){
    hideElement(saveParameterValuesBtn) ;
    let currentProductInfo  = GlobalVariablesCP.SelectedProductInfo;
    let currentParameterInfo = GlobalVariablesCP.SelectedParameterInfo

    let defaultVal = isEmpty(defaultParameterValueInput.value) ? null : defaultParameterValueInput.value;
    let minVal = isEmpty(minParameterValueInput.value) ? null : minParameterValueInput.value ;
    let maxVal = isEmpty(maxParameterValueInput.value) ?  null : maxParameterValueInput.value ;

    let dataToSave = {
        "parameter_id"  : currentParameterInfo['id'],
        "default_value" : defaultVal ,
        "min_value"     : minVal ,
        "max_value"     : maxVal
    }

    var updated = await updateParameterValuesInDB(dataToSave)
    if(updated) {
        var updatedProductInfo = await getProductInfoFromDB(currentProductInfo['id']) ;
        updateParameterValues(defaultVal, minVal, maxVal) ;
        GlobalVariablesCP.SelectedProductInfo   = updatedProductInfo ;
        GlobalVariablesCP.AllParameters = await getAllParameterFromDB() ;
        GlobalVariablesCP.SelectedParameterInfo   = await getParameterInfoFromDB(currentParameterInfo['id'])  ;
    }
    else{
        alert("Failed to save!")
        unHideElement(saveSelectedParameterImagesBtn);
    }
}



// 