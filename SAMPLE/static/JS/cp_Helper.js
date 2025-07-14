
/*---------------------------------- This file will contain helper functions -------------------------------------------------------*/

function filterProductsByProductTypeId(products, productTypeId) {
    return products.filter((prod) => prod['product_type_id'] == productTypeId);
}


function isObjectEmpty(obj) {
    return (typeof obj == "object") && Object.keys(obj).length < 1
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = "none";
}


function openModal(modalId) {
    document.getElementById(modalId).style.display = "block";
}


function sortArrayObjects(arrayObj, key, numericKeyVal = true, asc = true) {
    // Push items from orignal arry into a local and work on it. 
    // Doing this will stop modifying the original array.
    try {
        let sorted_arrayObj = [].concat(arrayObj)

        if (asc) {
            if (numericKeyVal) {
                sorted_arrayObj = sorted_arrayObj.sort((a, b) => a[key] - b[key])
            }
        }

        return sorted_arrayObj;
    }
    catch (err) {
        return [];
    }

}



function hideElement(element) {
    if (!element.classList.contains("hide")) element.classList.add("hide") 
}


function unHideElement(element) {
    if (element.classList.contains("hide"))  element.classList.remove("hide");
}



function isEmpty(value) {
    return (
      value === null ||         // Checks for null
      value === undefined ||    // Checks for undefined
      value === '' ||           // Checks for empty string
      (typeof value === 'object' && Object.keys(value).length === 0)    // Checks for empty object
    );
}
