// 
// API CALLS
let OPTIONS_GET = {
    method: "GET"

}
let OPTIONS_POST_JSON_DATA = {
    method: "POST",
    headers: { 'Content-Type': 'application/json' },
    body: null
}

let OPTIONS_POST_FORM_DATA = {
    method: "POST",
    body: null
}

//POST FormData -----------------------------------------------------------------------------------------------------------//
async function saveImageInfoInDB(uploadedFile, imageTagName) {
    let data = {}
    const formData = new FormData()
    formData.append("uploadedFile", uploadedFile)
    formData.append('image_tag_name', imageTagName)
    const url = `/save_image_info_to_db`;
    OPTIONS_POST_FORM_DATA.body = formData;
    const res = await fetch(url, OPTIONS_POST_FORM_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}

async function saveEOexcelFileInDB(uploadedFile, user_id) {
    let data = {}
    const formData = new FormData()
    formData.append("uploadedFile", uploadedFile)
    formData.append("user_id", user_id)
    const url = `/save_eo_excel_file_text_to_db`;
    OPTIONS_POST_FORM_DATA.body = formData;
    const res = await fetch(url, OPTIONS_POST_FORM_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}

//POST JSON Data -----------------------------------------------------------------------------------------------------------//
async function saveNewSectionNameInDB(data_to_post) {
    let data = {}
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/save_new_section_name_to_db`;
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}

async function deleteSectionFromDB(data_to_post) {
    let data = {}
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/delete_selected_section_db`;
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}

async function saveSectionDetailsInDB(data_to_post) {
    let data = {}
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/save_quote_section_detials_db`;
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}

async function saveTextInDB(data_to_post) {
    let data = {}
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/save_texts_to_db`;
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}

async function deleteFrequentlyUsedTextFromDB(data_to_post) {
    let data = {}
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/delete_frequently_used_text_db`;
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}


function addTextToFrequentlyUsedTextInDB(data_to_post) {
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/add_text_to_frequently_used_table_db`;
    fetch(url, OPTIONS_POST_JSON_DATA);
}

async function deleteTextFromDB(data_to_post) {
    let data = {}
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/delete_text_by_text_id_db`;
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}


async function deleteImageFromDB(data_to_post) {
    let data = {}
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const url = `/delete_image_by_id_db`;
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json(); }
    return data;
}



async function deleteQuoteFromDB(data_to_post) {
    let data = {}
    const url = `/delete_quote`;
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json() };
    return data;
}

async function copyQuoteAndDetailsInDB(data_to_post) {
    let data = {}
    const url = `/copy_quote_and_details`;
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json() };
    return data;
}

async function reorderSectionNamesInDB(data_to_post) {
    let data = {}
    const url = `/reorder_section_names_db`;
    OPTIONS_POST_JSON_DATA.body = JSON.stringify(data_to_post)
    const res = await fetch(url, OPTIONS_POST_JSON_DATA);
    if (res.status == 200) { data = await res.json() };
    return data;
}


//GET -----------------------------------------------------------------------------------------------------------//

async function getQuoteDataFromDB(quote_name) {
    let data = {}
    const url = `/get_quote_data_db/${quote_name}`;
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json(); }
    return data
}


async function getTextsByCurrentUserFromDB() {
    let data = []
    const url = `/get_texts_by_user_id_db`;
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json(); }
    return data
}

async function getFrequentlyUsedTextsByCurrentUserFromDB() {
    let data = []
    const url = `/get_frequently_used_texts_by_user_id_db`;
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json(); }
    return data
}

async function getFilteredTextsFromDB(search_str) {
    let data = []
    const url = `/get_searched_texts_db/${search_str}`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json(); }
    return data
}

async function getFilteredEOexcelTextsFromDB(user_id, search_str) {
    let data = []
    const url = `/get_searched_eo_excel_texts_db/${user_id}/${search_str}`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json(); }
    return data
}

async function getEOexcelTextsByCurrentUserFromDB(user_id) {
    let data = []
    const url = `/get_all_eo_texts_of_current_user_db/${user_id}`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json(); }
    return data
}



async function getAllImagesFromDB() {
    let data = []
    const url = `/get_all_images_db`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json(); }
    return data
}


async function getAllSectionImageSizesFromDB() {
    let data = []
    const url = `/get_all_section_image_size_db`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json() };
    return data
}



async function getFilteredImagesFromDB(search_str) {
    let data = []
    const url = `/get_searched_images_db/${search_str}`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json() };
    return data
}

async function getFilteredImagesByTagFromDB(imageTagId) {
    let data = []
    const url = `/get_all_images_db/${imageTagId}`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json() };
    return data
}

async function GetAllSectionNamesFromDB() {
    let data = []
    const url = `/get_all_section_names_db`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json() };
    return data
}

async function GetQuotesByUserId(user_id) {
    let data = []
    const url = `/get_quotes_by_user_id_db/${user_id}`
    const res = await fetch(url, OPTIONS_GET);
    if (res.status == 200) { data = await res.json() };
    return data
}