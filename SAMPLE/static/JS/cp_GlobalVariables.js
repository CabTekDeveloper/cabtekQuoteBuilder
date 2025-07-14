


let GlobalVariablesCP = {
    "Products"      : [],
    "AllParts"      : [],
    "AllCncCodes"   : [],
    "AllParameters" : [],
    "AllImages"     : [],
    "SelectedProductInfo"   : {},
    "SelectedPartInfo"      : {},
    "SelectedCnccodeInfo"   : {},
    "SelectedParameterInfo" : {}
};



/*------------ Initialize Variables -------------------------------------------------------*/

window.onload = async function () {
    if (window.location.href.match("/cp_home")) {

        GlobalVariablesCP.Products      = await getAllProductsFromDB();
        GlobalVariablesCP.AllParts      = await getAllPartNamesFromDB();
        GlobalVariablesCP.AllCncCodes   = await getAllCncCodesFromDB();
        GlobalVariablesCP.AllParameters = await getAllParameterFromDB();
        GlobalVariablesCP.AllImages     = await getAllImagesFromDB();
    
    }
};
