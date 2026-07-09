//-------------------------------------------------------------------------------------------------------------------------------------------------------

let CLICKUP_CLIENTS_DATA_DB = null;

//-------------------------------------------------------------------------------------------------------------------------------------------------------

let createQuoteDiv = document.getElementById("create_quote_div")
let uploadFileMsg = document.getElementById('upload_msg')
let eoFileInput = document.getElementById('eo_file_input')

let createQuoteForm = document.getElementById("create_quote_form")
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
let customerPhoneInp = document.getElementById("customer_phone")

//------------------------------------------------------------------------------------------------------------------------------------------------------- 
// Wait for the browser to load the page completely
document.addEventListener('DOMContentLoaded', async function () {
    if (window.location.pathname.includes('create_quote')) {
        await setClickupClientsDB();
    }
});

async function setClickupClientsDB() {
    // Only fetch if it hasn't been loaded
    if (CLICKUP_CLIENTS_DATA_DB === null) {
        try {
            CLICKUP_CLIENTS_DATA_DB = await getClickupClientsDB();
        } catch (error) {
            console.error("Failed to load ClickUp Clients database:", error);
        }
    }
}



//-------------------------------------------------------------------------------------------------------------------------------------------------------

// Event listeners

if (isTradeYesTag !== null) {
    isTradeYesTag.addEventListener('change', updateCustomerCompanyOptions);
}
if (isTradeNoTag !== null) {
    isTradeNoTag.addEventListener('change', updateCustomerCompanyOptions);
}

//-------------------------------------------------------------------------------------------------------------------------------------------------------
// Update options tags of customer company tag
function updateCustomerCompanyOptions() {
    let optionHtml = "";
    const isTradeClient = isTradeYesTag.checked;
    customerCompanySelect.innerHTML = "";

    toggleFormFieldsByClientType(isTradeClient);

    if (isTradeClient) {
        optionHtml = `<option></option>`

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

        customerNameSelect.innerHTML = `<option></option>`;
        customerEmailInp.value = "";
        customerPhoneInp.value = "";

    } else {
        optionHtml = `<option value="Cash Sale" selected>Cash Sale</option>`;
        customerNameInp.value = ""
        customerEmailInp.value = ""
        customerPhoneInp.value = ""
    }

    customerCompanySelect.insertAdjacentHTML('beforeend', optionHtml);
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

//-----------------------------------------------------------------------------------------------------------------------------------------------------//
// Customer company on change

if (customerCompanySelect !== null) {
    customerCompanySelect.addEventListener("change", function () {
        let customerCompany = this.value.toLowerCase();
        let filteredClient = [];

        if (!customerCompany) {
            customerNameSelect.innerHTML = `<option></option>`;
            customerEmailInp.value = "";
            customerPhoneInp.value = "";
            return;
        }

        if (CLICKUP_CLIENTS_DATA_DB) {
            filteredClient = CLICKUP_CLIENTS_DATA_DB.filter(item => {
                // Escape the database company name so it matches the escaped dropdown value
                const escapedStr = escapeHtml(item['company']).toLowerCase();
                return escapedStr === customerCompany && item['name'].trim().length > 0;
            });
        }

        if (customerCompany.length > 0 && isEmpty(filteredClient)) {
            alert(`\n\Company name '${customerCompany}' is missing client's name!\n\nFix it in the Clickup App.`)
            return
        }

        populateCustomerNameTag(filteredClient);
    });
}
//-----------------------------------------------------------------------------------------------------------------------------------------------------//
function populateCustomerNameTag(filteredClient) {
    let optionHtml = "";

    // Reset options
    customerEmailInp.value = "";
    customerPhoneInp.value = "";

    // Build options
    filteredClient.forEach(item => {
        // Only build option if str is not empty
        let escapedStr = escapeHtml(item['name']);
        if (escapedStr && escapedStr.length > 0) {
            optionHtml += `<option value="${escapedStr}">${escapedStr}</option>`;
        }
    });

    if (filteredClient.length > 1) {
        optionHtml = `<option></option>` + optionHtml;
    }
    else {
        populateCustomerEmailTag(filteredClient)
        populateCustomerPhoneTag(filteredClient)
    }
    customerNameSelect.innerHTML = optionHtml;
}

//-----------------------------------------------------------------------------------------------------------------------------------------------------//
// Customer name on change
if (customerNameSelect !== null) {
    customerNameSelect.addEventListener("change", function () {
        let customerCompany = customerCompanySelect.value.toLowerCase();
        let customerName = this.value.toLowerCase();
        let filteredClient = [];

        // Clear the inputs if customer name is blank
        if (!customerName) {
            customerEmailInp.value = "";
            customerPhoneInp.value = "";
            return;
        }

        if (CLICKUP_CLIENTS_DATA_DB) {
            filteredClient = CLICKUP_CLIENTS_DATA_DB.filter(item => {
                const escapedCompany = escapeHtml(item['company']).toLowerCase();
                const escapedName = escapeHtml(item['name']).toLowerCase();
                return escapedCompany === customerCompany && escapedName === customerName;
            });
        }

        populateCustomerEmailTag(filteredClient);
        populateCustomerPhoneTag(filteredClient);
    });
}
//-----------------------------------------------------------------------------------------------------------------------------------------------------//
// Populate customer email
function populateCustomerEmailTag(filteredClient) {
    let val = ""
    if (!isEmpty(filteredClient)) {
        val = filteredClient[0]['email']
    }
    customerEmailInp.value = val
}

//-----------------------------------------------------------------------------------------------------------------------------------------------------//
// Populate customer phone no
function populateCustomerPhoneTag(filteredClient) {
    let val = ""
    if (!isEmpty(filteredClient)) {
        val = filteredClient[0]['phone']
    }
    customerPhoneInp.value = val
}



//-------------------------------------------------------------------------------------------------------------------------------------------------------//
// Create quote
async function creatQuote(event) {
    event.preventDefault();     //Stop form from refreshing

    let data = await getCreateQuoteFormData()

    if (!isEmpty(data)) {
        let response = await createNewQuote(data)

        if (response && response.success) {
            window.location.href = (`/add_quote_details/${data.quote_name}`)
        }
        else {
            alert("Failed to create quote!")
            window.location.reload();
        }
    }
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------//
// Get form data and validate
async function getCreateQuoteFormData() {
    let quoteNameInp = createQuoteForm.querySelector('[name="quote_name"]');

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
    if (!createQuoteForm.checkValidity()) {
        createQuoteForm.reportValidity();
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
        if (response && response.exists) {
            quoteNameInp.setCustomValidity(`The quote name '${quoteName}' exists already!`);
        }
    }

    // check custom error validation
    if (!createQuoteForm.checkValidity()) {
        createQuoteForm.reportValidity();
        return null;
    }

    // Get form data
    let formData = new FormData(createQuoteForm);
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
function uploadEoExcelFileToDb(event) {

    let user_id = event.getAttribute('data-user_id')
    let allowedExcelFileTypes = ["application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"];
    let uploadedFiles = eoFileInput.files;
    uploadFileMsg.innerText = "";
    quoteNameInp.value = ''

    if (uploadedFiles.length > 0) {
        let uploadedFile = uploadedFiles[0]
        let fileType = uploadedFile['type'].toLowerCase();

        if (allowedExcelFileTypes.includes(fileType)) {
            const formData = new FormData()
            formData.append("uploadedFile", uploadedFile)
            formData.append("user_id", user_id)

            const url = "/save_eo_excel_file_text_to_db"
            const options = {
                method: "POST",
                body: formData
            }


            // Post the image file to Flask App
            fetch(url, options).then(res => {
                if (res.status == 200) {
                    return res.json()
                }
                else {
                    uploadFileMsg.innerText = "File not Uploaded. Try again."
                }
            }).then(data => {
                if (data && data["file_uploaded"] == true) {
                    uploadFileMsg.innerText = "File uploaded!"

                    let fileName = uploadedFile['name'].split('.')[0]
                    quoteNameInp.value = fileName
                    // refreshImageResultDiv()
                }
                else {
                    uploadFileMsg.innerText = data['message']
                }
            })

        }
        else {

            uploadFileMsg.innerText = "The uploaded filetype is not supported. Make sure you upload only the excel files generated from Eze Order program.";

        }
    }

}

