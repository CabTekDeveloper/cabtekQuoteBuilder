// 
// 
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


