

// JS : Display Image Modal

/* Variables ------------------------------------------------------------------------------------------------------------------------*/
let imageModal = document.getElementById("image_modal");
let imageNameTag = document.getElementById("image_name_tag");
let imageDiv = document.getElementById("image_div");

/* Functions ------------------------------------------------------------------------------------------------------------------------*/

function showImageModal(showModal, imageName="", imagePath="") {
    imageModal.style.display = showModal ? "block" : "none";

    let imageHtml = (showModal) ? `<img src="${imagePath}" alt="${imageName}" width="100%" height="auto" >` : ""
    imageNameTag.innerText = imageName;
    imageDiv.innerHTML= imageHtml ;
}

