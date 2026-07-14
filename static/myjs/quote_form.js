//-------------------------------------------------------------------------------------------------------------------------------------------------------

// windows variable set in quote_form.html
let CLICKUP_CLIENTS_DATA_DB = window.all_clients || [];
let QUOTE_INFO = window.quote_info || null;
let IS_EDIT = QUOTE_INFO !== null; // Dynamically sets your edit state flag
//-------------------------------------------------------------------------------------------------------------------------------------------------------

let createQuoteDiv = document.getElementById("create_quote_div")
let uploadFileMsg = document.getElementById('upload_msg')
let eoFileInput = document.getElementById('eo_file_input')

let quoteForm = document.getElementById("quote_form")
let quoteNameInp = document.getElementById('quote_name_inp')
let isTradeYesTag = document.getElementById("is_trade_client_yes")
let isTradeNoTag = document.getElementById("is_trade_client_no")
let customerCompanySelect = document.getElementById('customer_company');

// Customer name 
let customerNameInp = document.getElementById("customer_name_inp")
let customerNameSelect = document.getElementById("customer_name_select")

// Customer email
let customerEmailInp = document.getElementById("customer_email")

// Customer phone no 
let customerPhoneInp = document.getElementById("customer_phone_no")

let formSubmitBtn = document.getElementById("form_submit_btn")

// Delivery type
let deliveryTypeSelect = document.getElementById("delivery_type");

// Delivery info/address
let deliveryInfoInp = document.getElementById("delivery_info")


//-------------------------------------------------------------------------------------------------------------------------------------------------------
// Populate quote info when in edit mode
if (IS_EDIT) {
    initEditMode();
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------

function initEditMode() {
    // Auto populate quote info if valid info exists: is_trade_client
    if (!QUOTE_INFO || isEmpty(QUOTE_INFO.is_trade_client)) {
        return;
    }

    // Determine is_trade_client
    const isTradeClient = QUOTE_INFO.is_trade_client.toLowerCase() === "yes";
    isTradeYesTag.checked = isTradeClient;
    isTradeNoTag.checked = !isTradeClient;

    // Build the initial customer info fields
    handleClientTypeChange();

    // Populate cutomer info fields
    if (isTradeClient) {
        // Populate client company
        const targetCompany = escapeHtml(QUOTE_INFO.customer_company);
        customerCompanySelect.value = targetCompany;

        // Filter and build option for client name
        populateCustomerNameTag(targetCompany);

        // Select client name from client name options
        const targetName = escapeHtml(QUOTE_INFO.customer_name);
        customerNameSelect.value = targetName;

        // Populate client details:Emial and phone
        populateCustomerDetails(targetCompany, targetName);

    } else {
        if (QUOTE_INFO.customer_name) customerNameInp.value = QUOTE_INFO.customer_name;
        if (QUOTE_INFO.customer_email) customerEmailInp.value = QUOTE_INFO.customer_email;
        if (QUOTE_INFO.customer_phone_no) customerPhoneInp.value = QUOTE_INFO.customer_phone_no;
    }
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
function toggleFormFieldsByClientType(isTradeClient) {
    const hideClass = "hide";

    // Toggle visibility classes based on isTradeClient
    customerNameSelect.classList.toggle(hideClass, !isTradeClient);
    customerNameInp.classList.toggle(hideClass, isTradeClient);

    //Disable the hidden element so FormData ignores it
    customerNameSelect.disabled = !isTradeClient;
    customerNameInp.disabled = isTradeClient;

    // Toggle required attributes
    customerNameSelect.required = isTradeClient;
    customerNameInp.required = !isTradeClient;

    // Toggle readonly
    customerEmailInp.readOnly = isTradeClient;
    customerPhoneInp.readOnly = isTradeClient;
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
// Client type change Event listeners
[isTradeYesTag, isTradeNoTag].forEach(tag => {
    tag.addEventListener('change', handleClientTypeChange);
});
//-------------------------------------------------------------------------------------------------------------------------------------------------------

function handleClientTypeChange() {
    const isTradeClient = isTradeYesTag.checked;
    toggleFormFieldsByClientType(isTradeClient);
    populateCompanyDropdown(isTradeClient);
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
function populateCompanyDropdown(isTradeClient) {
    let optionHtml = "";
    customerCompanySelect.innerHTML = "";

    if (isTradeClient) {
        optionHtml = `<option></option>`;

        if (CLICKUP_CLIENTS_DATA_DB) {
            // Use a Set to keep track of unique company names
            const seenCompanies = new Set();

            CLICKUP_CLIENTS_DATA_DB.forEach(item => {
                let escapedCompany = escapeHtml(item['company']);
                // Only add if it's a valid string AND we haven't seen it yet
                if (escapedCompany && escapedCompany.trim().length > 0 && !seenCompanies.has(escapedCompany)) {
                    seenCompanies.add(escapedCompany);
                    optionHtml += `<option value="${escapedCompany}">${escapedCompany}</option>`;
                }
            });
        }

        // Reset trade-specific dependent elements
        customerNameSelect.innerHTML = `<option></option>`;
        customerEmailInp.value = "";
        customerPhoneInp.value = "";

    } else {
        // Fallback option setup for Cash Sales
        optionHtml = `<option value="Cash Sale" selected>Cash Sale</option>`;

        // Reset plain text input elements
        customerNameInp.value = "";
        customerEmailInp.value = "";
        customerPhoneInp.value = "";
    }

    customerCompanySelect.insertAdjacentHTML('beforeend', optionHtml);
}


//-----------------------------------------------------------------------------------------------------------------------------------------------------//
// Customer company on change
customerCompanySelect.addEventListener("change", function () {
    populateCustomerNameTag(this.value);
});

//-----------------------------------------------------------------------------------------------------------------------------------------------------//
//-----------------------------------------------------------------------------------------------------------------------------------------------------//
function populateCustomerNameTag(companyName) {
    let optionHtml = "";

    // Reset dependent text inputs immediately
    customerEmailInp.value = "";
    customerPhoneInp.value = "";

    // Clear dropdown and exit early if the company selection is blank
    if (!companyName) {
        customerNameSelect.innerHTML = `<option></option>`;
        return;
    }

    // Filter clients
    let filteredClient = [];
    if (CLICKUP_CLIENTS_DATA_DB) {
        let searchCompanyLower = companyName.toLowerCase();
        filteredClient = CLICKUP_CLIENTS_DATA_DB.filter(item => {
            const dbEscapedCompany = escapeHtml(item['company']).toLowerCase();
            return dbEscapedCompany === searchCompanyLower && item['name'].trim().length > 0;
        });
    }

    // Handle empty client
    if (isEmpty(filteredClient)) {
        customerNameSelect.innerHTML = `<option></option>`;
        alert(`\nCompany name '${companyName}' is missing client's name!\n\nFix it in the Clickup App.`);
        return;
    }

    // Build option tags
    filteredClient.forEach(item => {
        let escapedStr = escapeHtml(item['name']);
        if (escapedStr && escapedStr.length > 0) {
            optionHtml += `<option value="${escapedStr}">${escapedStr}</option>`;
        }
    });

    if (filteredClient.length > 1) {
        optionHtml = `<option></option>` + optionHtml;
    } else {
        // Automatically populate email and phone if there's exactly one client matching this company
        const singleClientName = escapeHtml(filteredClient[0]['name']);
        populateCustomerDetails(companyName, singleClientName);
    }

    customerNameSelect.innerHTML = optionHtml;
}

//-----------------------------------------------------------------------------------------------------------------------------------------------------//
// Customer name on change
customerNameSelect.addEventListener("change", function () {
    populateCustomerDetails(customerCompanySelect.value, this.value);
});

//-----------------------------------------------------------------------------------------------------------------------------------------------------//
// Populate customer email and phone no
function populateCustomerDetails(companyName, customerName) {
    // 1. Clear out fields and exit early if either search query string is missing
    if (!companyName || !customerName) {
        customerEmailInp.value = "";
        customerPhoneInp.value = "";
        return;
    }

    let filteredClient = [];
    if (CLICKUP_CLIENTS_DATA_DB) {
        const targetCompanyLower = companyName.toLowerCase();
        const targetNameLower = customerName.toLowerCase();

        filteredClient = CLICKUP_CLIENTS_DATA_DB.filter(item => {
            const dbEscapedCompany = escapeHtml(item['company']).toLowerCase();
            const dbEscapedName = escapeHtml(item['name']).toLowerCase();
            return dbEscapedCompany === targetCompanyLower && dbEscapedName === targetNameLower;
        });
    }

    // 2. Extracted safe assignment values
    let emailVal = "";
    let phoneVal = "";

    if (!isEmpty(filteredClient)) {
        emailVal = filteredClient[0]['email'] || "";
        phoneVal = filteredClient[0]['phone'] || "";
    }

    // 3. Assign to DOM elements
    customerEmailInp.value = emailVal;
    customerPhoneInp.value = phoneVal;
}
// if (customerNameSelect !== null) {
//     customerNameSelect.addEventListener("change", function () {
//         let customerCompany = customerCompanySelect.value.toLowerCase();
//         let customerName = this.value.toLowerCase();
//         let filteredClient = [];

//         // Clear the inputs if customer name is blank
//         if (!customerName) {
//             customerEmailInp.value = "";
//             customerPhoneInp.value = "";
//             return;
//         }

//         if (CLICKUP_CLIENTS_DATA_DB) {
//             filteredClient = CLICKUP_CLIENTS_DATA_DB.filter(item => {
//                 const escapedCompany = escapeHtml(item['company']).toLowerCase();
//                 const escapedName = escapeHtml(item['name']).toLowerCase();
//                 return escapedCompany === customerCompany && escapedName === customerName;
//             });
//         }

//         populateCustomerEmailTag(filteredClient);
//         populateCustomerPhoneTag(filteredClient);
//     });
// }
// //-----------------------------------------------------------------------------------------------------------------------------------------------------//
// // Populate customer email
// function populateCustomerEmailTag(filteredClient) {
//     let val = ""
//     if (!isEmpty(filteredClient)) {
//         val = filteredClient[0]['email']
//     }
//     customerEmailInp.value = val
// }

// //-----------------------------------------------------------------------------------------------------------------------------------------------------//
// // Populate customer phone no
// function populateCustomerPhoneTag(filteredClient) {
//     let val = ""
//     if (!isEmpty(filteredClient)) {
//         val = filteredClient[0]['phone']
//     }
//     customerPhoneInp.value = val
// }



//-------------------------------------------------------------------------------------------------------------------------------------------------------//
// Create quote
// 
formSubmitBtn.addEventListener("click", onFormSubmit)

async function onFormSubmit(event) {
    event.preventDefault(); // Stop form from refreshing

    let data = await getquoteFormData();

    // Check if data is valid and not empty (assuming getquoteFormData returns null on validation failure)
    if (data && !isEmpty(data)) {

        if (IS_EDIT) {
            data.quote_id = QUOTE_INFO.quote_id
        }

        let response = await (IS_EDIT ? saveEditedQuote(data) : createNewQuote(data));

        if (response && response.success) {
            if (IS_EDIT) {
                // Safely route back using the template type flag
                window.location.href = `/index/${QUOTE_INFO?.is_template || 'no'}`;
            } else {
                window.location.href = `/add_quote_details/${encodeURIComponent(data.quote_name)}`;
            }
        }
        else {
            // Extract a specific error message from the backend if it exists, fallback to a default
            let errorMsg = response?.message || "Failed to save quote!";
            alert(`Error: ${errorMsg}\n\nPlease check your connection and try again.`);
        }
    }
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------//
// Get form data and validate
async function getquoteFormData() {
    // check required validation field first. Clear previous message
    quoteNameInp.setCustomValidity("");

    // Since the validation will not work on readonly html tags, we will alert user Fix the value in the ClickUp app
    if (isTradeYesTag.checked && quoteNameInp.value && customerNameSelect.value) {
        if (customerEmailInp.value === "" && customerPhoneInp.value === "") {
            alert("\nThis client is missing Email and Phone no.\n\nFix them in the ClickUp app!");
            return null;
        } else if (customerEmailInp.value === "") {
            alert("\nThis client is missing Email.\n\nFix it in the ClickUp app!");
            return null;
        } else if (customerPhoneInp.value === "") {
            alert("\nThis client is missing Phone no.\n\nFix it in the ClickUp app!");
            return null;
        }
    }

    // Validation for required Values
    if (!quoteForm.checkValidity()) {
        quoteForm.reportValidity();
        return null;
    }

    // Custom validation : Quote name
    quoteNameInp.value = quoteNameInp.value.trim();
    const quoteName = quoteNameInp.value;

    if (quoteName.includes("/") || quoteName.includes("\\")) {
        quoteNameInp.setCustomValidity("Quote name cannot contain forward slashes (/) or backslashes (\\)");
    }
    else if (quoteName !== "") {
        // Check if the quote name exists already in the database
        let response = await checkQuoteNameExistsDB(quoteName);
        let quoteNameExists = response?.exists ?? false;

        // Determine if the enterned quote name matches the original name
        let isOrignalName = IS_EDIT ? quoteName.toLowerCase() === QUOTE_INFO.quote_name.toLowerCase() : false;

        // Set error, if the name is a duplicate and not the orginal name
        if (quoteNameExists && !isOrignalName) {
            quoteNameInp.setCustomValidity(`The quote name '${quoteName}' exists already!`);
        }
    }

    // check custom error validation
    if (!quoteForm.checkValidity()) {
        quoteForm.reportValidity();
        return null;
    }

    // Get form data
    let formData = new FormData(quoteForm);
    let data = Object.fromEntries(formData.entries());

    // Trim whitespaces
    for (let key in data) data[key] = typeof data[key] === "string" ? data[key].trim() : data[key];

    // Convert number to correct format
    if (data.company_id) data.company_id = Number(data.company_id);

    // remove the field we don't require
    delete data.eo_file;

    return data;
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
// Delivery type on change

deliveryTypeSelect.addEventListener("change", (event)=>{
    toggleDeliveryInfoInp(event.target.value)
})

//-------------------------------------------------------------------------------------------------------------------------------------------------------
function toggleDeliveryInfoInp(delivery_type) {
    let pickupDeliveryInfo = "7:30am - 3:00pm Mon to Fri"
    let isPickUp = delivery_type && delivery_type.toLowerCase().includes("pick up");
    deliveryInfoInp.value = isPickUp ? pickupDeliveryInfo : "";
    deliveryInfoInp.readOnly = isPickUp
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
// function uploadEoExcelFileToDb(event) {

//     let user_id = event.getAttribute('data-user_id')
//     let allowedExcelFileTypes = ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
//     let uploadedFiles = eoFileInput.files;
//     uploadFileMsg.innerText = "";
//     quoteNameInp.value = ''

//     if (uploadedFiles.length > 0) {
//         let uploadedFile = uploadedFiles[0]
//         let fileType = uploadedFile['type'].toLowerCase();

//         if (allowedExcelFileTypes.includes(fileType)) {
//             const formData = new FormData()
//             formData.append("uploadedFile", uploadedFile)
//             formData.append("user_id", user_id)

//             const url = "/save_eo_excel_file_text_to_db"
//             const options = {
//                 method: "POST",
//                 body: formData
//             }


//             // Post the image file to Flask App
//             fetch(url, options).then(res => {
//                 if (res.status == 200) {
//                     return res.json()
//                 }
//                 else {
//                     uploadFileMsg.innerText = "File not Uploaded. Try again."
//                 }
//             }).then(data => {
//                 if (data && data["file_uploaded"] == true) {
//                     uploadFileMsg.innerText = "File uploaded!"

//                     let fileName = uploadedFile['name'].split('.')[0]
//                     quoteNameInp.value = fileName
//                     // refreshImageResultDiv()
//                 }
//                 else {
//                     uploadFileMsg.innerText = data['message']
//                 }
//             })

//         }
//         else {

//             uploadFileMsg.innerText = "The uploaded filetype is not supported. Make sure you upload only the excel files generated from Eze Order program.";

//         }
//     }

// }

