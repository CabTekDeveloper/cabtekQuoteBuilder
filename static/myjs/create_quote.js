// 
// 
let createQuoteDiv = document.getElementById("create_quote_div")



let uploadFileMsg = document.getElementById('upload_msg')
let eoFileInput = document.getElementById('eo_file_input')
let quoteNameInp = document.getElementById('quote_name_inp')

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

// Get form data and validate
async function getCreateQuoteFormData() {
    let createQuoteForm = document.getElementById("create_quote_form")
    let quoteNameInp = createQuoteForm.querySelector('[name="quote_name"]');

    //check required validation field first
    quoteNameInp.setCustomValidity(""); // Clear previous custom validation message

    if (!createQuoteForm.checkValidity()) {
        createQuoteForm.reportValidity();
        return null;
    }

    //Custom validation : Quote name
    quoteNameInp.value = quoteNameInp.value.trim();
    const quoteName = quoteNameInp.value;

    if (quoteName.includes("/") || quoteName.includes("\\")) {
        quoteNameInp.setCustomValidity("Quote name cannot contain forward slashes (/) or backslashes (\\)")

    }
    else if (quoteName !== "") {
        // Check if the quote name exists already in the database
        let response = await checkQuoteNameExistsDB(quoteName)
        if (response && response.exists) {
            quoteNameInp.setCustomValidity(`The quote name '${quoteName}' exists already!`)
        }
    }

    //check custom error validation
    if (!createQuoteForm.checkValidity()) {
        createQuoteForm.reportValidity();
        return null;
    }

    //Get form data
    let formData = new FormData(createQuoteForm);
    let data = Object.fromEntries(formData.entries());

    // Trim whitespaces
    for (let key in data) data[key] = typeof data[key] === "string" ? data[key].trim() : data[key];

    // Convert number to correct format
    if (data.company_id) data.company_id = Number(data.company_id);

    //remove the field we don't require
    delete data.eo_file;

    return data;

}


// let new_quote_info = {
//     'quote_name': request.form['quote_name'].strip(),
//     'quoted_by': request.form['quoted_by'].strip().title(),
//     'date_quote_created': date_today,
//     'customer_name': request.form['customer_name'].strip(),
//     'customer_email': request.form['customer_email'].strip(),
//     'customer_phone_no': request.form['customer_phone_no'].strip(),
//     'delivery_info': request.form['delivery_info'].strip(),
//     'is_template': request.form['is_template'].strip(),
//     'company_id': int(request.form['company_id'])
// }