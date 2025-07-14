

deleteDiv = document.getElementById('deleteDiv')
yesNoDiv = document.getElementById('yesNoDiv')
btnDelete = document.getElementById('btnDelete')
updateDiv = document.getElementById('updateDiv')
btnNo = document.getElementById('btnNo')

if (btnDelete != null) {
    btnDelete.onclick = function (e) {
        updateDiv.classList.add('hide')
        deleteDiv.classList.add('hide')
        yesNoDiv.classList.remove('hide')
        window.scrollTo({ left: 0, top: document.body.scrollHeight, behavior: "smooth" });
    }
}

if (btnNo != null) {
    btnNo.onclick = function (e) {

        updateDiv.classList.remove('hide')
        deleteDiv.classList.remove('hide')
        yesNoDiv.classList.add('hide')
    }
}

// hide/show upload file div
addImageDiv = document.getElementById('addImageDiv');
addVideoDiv = document.getElementById('addVideoDiv');
fileAddedDiv = document.getElementById('fileAddedDiv');

function showAddImageDiv() {
    addImageDiv.classList.remove('hide');
    addVideoDiv.classList.add('hide');
    fileAddedDiv.innerHTML = "";
    errorMsgDiv.innerHTML = "";
}

function showAddVideoDiv() {
    addImageDiv.classList.add('hide');
    addVideoDiv.classList.remove('hide');
    fileAddedDiv.innerHTML = "";
}

function hideUploadDiv() {
    addImageDiv.classList.add('hide');
    addVideoDiv.classList.add('hide');

}