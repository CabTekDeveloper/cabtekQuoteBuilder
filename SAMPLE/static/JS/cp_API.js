/*---------------------------------- This file will contain functions used for getting and positing data to Database.------------------------------------------------*/

// Get: all Products from DB
async function getAllProductsFromDB() {
    let data = []
    let url = "/get_all_products_db"
    let options = { method: "GET" }
    const res = await fetch(url, options)

    if (res.status == 200) {
        data = await res.json();
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }

    return data
}

// Get: all Part Names from DB
async function getAllPartNamesFromDB() {
    let data = []
    let url = "/get_all_part_names_db"
    let options = { method: "GET" }
    const res = await fetch(url, options)

    if (res.status == 200) {
        data = await res.json();
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }

    return data
}

// Get: all Part Names from DB
async function getAllCncCodesFromDB() {
    let data = []
    let url = "/get_all_cnccodes_db"
    let options = { method: "GET" }
    const res = await fetch(url, options)

    if (res.status == 200) {
        data = await res.json();
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }

    return data
}

async function getAllParameterFromDB() {
    let url = "/get_all_parameters_db"
    let options = { method: "GET" }
    const res = await fetch(url, options)

    if (res.status == 200) {
        data = await res.json();
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }

    return data
}

// Get: Images Info from DB
async function getAllImagesFromDB() {
    let url = "/get_all_images_db"
    let options = { method: "GET" }
    const res = await fetch(url, options)

    if (res.status == 200) {
        data = await res.json();
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }

    return data
}


// Get: Product Info from DB
async function getProductInfoFromDB(productId) {
    let data = {}
    if (!isEmpty(productId)) {
        let url = `/get_product_info_db/${productId}`
        let options = { method: "GET" }
        const res = await fetch(url, options);
        if (res.status == 200) {
            data = await res.json();
        }
        else {
            alert(`Http request error code ${res.status}: ${res.statusText}`)
        }
    }
    return data
}

// Get: CncCode from DB
async function getCnccodeInfoFromDB(cnccodeId) {
    let data = {}
    let url = `/get_cnccode_info_db/${cnccodeId}`
    let options = { method: "GET" }
    const res = await fetch(url, options);

    if (res.status == 200) {
        data = await res.json();
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }

    return data
}

// Get: Parameter Info from DB
async function getParameterInfoFromDB(parameterId) {
    let data = {}
    let url = `/get_parameter_info_db/${parameterId}`
    let options = { method: "GET" }
    const res = await fetch(url, options);

    if (res.status == 200) {
        data = await res.json();
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }

    return data
}


// POST

// Post: Update Product Parts in DB
async function updateProductPartsInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_product_parts_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}

async function updatePartCnccodesInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_part_cnccodes_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}

async function updateCnccodeParametersInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_cnccode_parameters_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}

async function updateCnccodeDescriptionInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_cnccode_description_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}

async function updateCnccodeImagesInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_cnccode_images_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}


async function updateParameterDescriptionInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_parameter_description_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}

async function updateParameterImagesInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_parameter_images_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}


async function updateParameterValuesInDB(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/update_parameter_values_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}



async function saveImageInDB(data_to_post) {
    let response = { "saved": false, "message": "File not uploaded!" }

    const formData = new FormData()
    formData.append("data", data_to_post)

    const url = `/save_image_db`;
    let options = {
        method: "POST",
        body: formData
    }

    const res = await fetch(url, options);

    if (res.status == 200) {
        const data = await res.json();
        response.saved = data['saved'];
        response.message = data['message'];
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
    }



    return response;


}







async function insertNewPartInDb(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/insert_new_part_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}

async function insertNewCnccodeInDb(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/insert_new_cnccode_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}

async function insertNewParameterInDb(data_to_post) {
    let options = {
        method: "POST",
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data_to_post)
    }
    const url = `/insert_new_parameter_db`;
    const res = await fetch(url, options);

    if (res.status == 200) {
        return true;
    }
    else {
        alert(`Http request error code ${res.status}: ${res.statusText}`)
        return false;
    }

}