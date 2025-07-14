

// JS : Upload Image Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let uploadImageModal = document.getElementById("upload_image_modal");
let imageUploadInput = uploadImageModal.querySelector("#image_upload_input")
let fileUploadMsgDiv = uploadImageModal.querySelector("#file_upload_msg_div")
let saveUploadedImageBtn = uploadImageModal.querySelector("#save_uploaded_image_btn")

// 

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

function resetUploadImageModal() {
    imageUploadInput.value = "";
    fileUploadMsgDiv.innerText = "";
    hideElement(saveUploadedImageBtn)
}

function LoadUploadImageModal() {
    openModal(uploadImageModal.id);
    resetUploadImageModal();
}

if (imageUploadInput != null) {
    // on change event
    imageUploadInput.onchange = (e) => {
        let uploadedFiles = imageUploadInput.files;
        let allowedImageTypes = ["image/jpg", "image/jpeg", "image/png"];
        if (uploadedFiles.length > 0) {
            let uploadedFile = uploadedFiles[0]
            let fileType = uploadedFile['type'].toLowerCase();

            if (allowedImageTypes.includes(fileType)) {
                unHideElement(saveUploadedImageBtn);
            }
            else {
                fileUploadMsgDiv.innerText = "Only .jpg, .jpeg and .png file types can be uploaded.";
            }
        }
        else {
            resetUploadImageModal()
        }
    };

    // on click event
    imageUploadInput.onclick = (e) => resetUploadImageModal();

}


async function saveUploadedImageInDB() {
    let uploadedFile = imageUploadInput.files[0];
    let responseData = await saveImageInDB(uploadedFile)
    
    if (responseData['saved']) {
        fileUploadMsgDiv.innerText = "File Uploaded"
        GlobalVariablesCP.AllImages     = await getAllImagesFromDB();
    }
    else {
        fileUploadMsgDiv.innerText = responseData['message']
    }
    hideElement(saveUploadedImageBtn)
}