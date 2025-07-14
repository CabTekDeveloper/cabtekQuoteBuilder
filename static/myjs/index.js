// 
// 
let savedQuotesDiv = document.getElementById('saved_quote_div')
let savedTemplateDiv = document.getElementById('saved_template_div')

let savedQuoteTable = document.getElementById('saved_quote_table')
let savedTemplateTable = document.getElementById('saved_template_table')

// index buttons and display divs
let savedQuoteBtn = document.getElementById('saved_quote_btn')
let createQuoteBtn = document.getElementById('create_quote_btn')
let SavedTemplateBtn = document.getElementById('saved_template_btn')

let quoteStatusInp = document.getElementById('quote_status_inp')
let quoteStatusMsgDiv = document.getElementById('quote_status_msg_div')
let quoteAcceptedImgDiv = document.getElementById('quote_accepted_img_div')
let quoteRejectedImgDiv = document.getElementById("quote_rejected_img_div")

// UPDATE QUOTE STATUS
function update_quote_status(updateBtn) {
    hideElement(quoteAcceptedImgDiv);
    hideElement(quoteRejectedImgDiv);

    let quoteId = parseInt(updateBtn.getAttribute('data-quote_id'))
    let quoteStatus = quoteStatusInp.options[quoteStatusInp.selectedIndex].value

    let formData = new FormData()
    formData.append("quote_id", quoteId)
    formData.append("quote_status", quoteStatus)
    const url = `/update_quote_status/${quoteId}`
    const options = {
        method: "POST",
        body: formData
    }

    fetch(url, options)
        .then(res => {
            if (res.status == 200) {
                return res.json()
            }
            else {
                alert("The status was not update! Please log out and try again!")
                return
            }
        })
        .then(data => {
            if (data && data['updated'] == true) {
                quoteStatusMsgDiv.innerText = `Successfully updated!`
                setTimeout(() => { quoteStatusMsgDiv.innerText = '' }, 3000);   // remove the msg afer x seconds

                if (quoteStatus.toLowerCase() != "--none--") {
                    if (quoteStatus.toLowerCase() == "accepted") {
                        quoteAcceptedImgDiv.classList.remove('hide')
                        quoteRejectedImgDiv.classList.add('hide')
                    }
                    else {
                        quoteAcceptedImgDiv.classList.add('hide')
                        quoteRejectedImgDiv.classList.remove('hide')
                    }
                }
            }

        })

}



// TOGGLE COLOR OF ACTIVE AND INACTIVE BUTTONS, HIDE OR UNHIDE DISPLAY DIVS
function showSavedQuotesDiv() {
    addColorToActiveBtn(savedQuoteBtn)
    showActiveDisplayDiv(savedQuotesDiv)
}

function showSavedTemplateDiv() {
    addColorToActiveBtn(SavedTemplateBtn)
    showActiveDisplayDiv(savedTemplateDiv)
}

function addColorToActiveBtn(activeBtn) {
    let indexButtons = [savedQuoteBtn, createQuoteBtn, SavedTemplateBtn]
    indexButtons.forEach(el => {
        if (el == activeBtn) {
            el.classList.add('btn-dark')
        }
        else {
            el.classList.remove('btn-dark')
        }
    })

}

function showActiveDisplayDiv(activeDisplayDiv) {
    let indexDisplayDivs = [savedQuotesDiv, savedTemplateDiv]
    indexDisplayDivs.forEach(el => {
        if (el == activeDisplayDiv) {
            el.classList.remove('hide')
        }
        else {
            el.classList.add('hide')
        }
    })

}



// DELETE QUOTE FROM TABLE
async function deleteQuote(quoteDeleteBtn) {
    let quoteId = quoteDeleteBtn.getAttribute('data-quote_id')
    let quoteName = quoteDeleteBtn.getAttribute('data-quote_name')
    let isTemplate = quoteDeleteBtn.getAttribute('data-is_template').trim()

    if (confirm(`Are you sure you want to delete '${quoteName}'?`) == true) {
        toggleMessageModal("Deleting quote!", true);

        let data_to_post = { "quote_id": quoteId };
        let data = await deleteQuoteFromDB(data_to_post);
        
        if (data && data["deleted"]) {
            if (isTemplate == 'yes') {
                savedTemplateTable.querySelector("#quote_id_" + quoteId).remove()
            }
            else {
                savedQuoteTable.querySelector("#quote_id_" + quoteId).remove();
            }
        }
        else {
            alert("Quote not deleted!")
        }

        toggleMessageModal("",false)        ;
    }
}



// COPY AND ADD THE COPIED QUOTE IN THE TOP ROW OF THE TABLE
async function copyQuoteAndDetails(copyBtn) {
    let quoteId = copyBtn.getAttribute('data-quote_id')
    let quoteName = copyBtn.getAttribute('data-quote_name')

    if (confirm(`Are you sure you make a copy of "${quoteName}"?`) == true) {
        toggleMessageModal("Copying quote!", true);

        let data_to_post = { "quote_id": quoteId };
        let data = await copyQuoteAndDetailsInDB(data_to_post);

        if (data && data['data']) {
            let copied_quote_info = data['data']
            let diy_badge = copied_quote_info['company_id'] == 2 ? `<span class="badge badge-pill badge-danger ml-2 ">DIY</span>` : "";
            if (copied_quote_info['is_template'].toLowerCase().trim() == 'yes') {

                let newRow = `
                        <tr id ="quote_id_${copied_quote_info['quote_id']}" class="text-danger">  
                            <td>${copied_quote_info['quote_name']}${diy_badge}</td>
                            <td>${copied_quote_info['quoted_by']}</td>
                            <td>${copied_quote_info['date_quote_created']}</td>
                            <td ><a href="/add_quote_details/${copied_quote_info['quote_name']}" type="button" class="btn btn-sm btn-primary full-width p-0 m-0 "><small class=" pl-1 pr-1">Modify</small></a></td>
                            <td ><a href="/view_quote/${copied_quote_info['quote_name']}" type="button" class="btn btn-sm btn-info full-width p-0 m-0"><small class=" pl-1 pr-1">View</small></a></td>
                            <td ><a href="/edit_quote/${copied_quote_info['quote_id']}" type="button" class="btn btn-sm btn-success full-width p-0 m-0"><small class=" pl-1 pr-1">Edit</small></a></td>
                            <td ><button type="button" class="btn btn-sm btn-secondary full-width p-0 m-0 " data-quote_name ="${copied_quote_info['quote_name']}" data-quote_id ="${copied_quote_info['quote_id']}" onclick="copyQuoteAndDetails(this)"><small class=" pl-1 pr-1">Copy</small></button></td>
                            <td ><button  type="button" class="btn btn-sm btn-danger full-width p-0 m-0" data-quote_name ="${copied_quote_info['quote_name']}" data-quote_id="${copied_quote_info['quote_id']}" data-is_template="${copied_quote_info['is_template']}" onclick="deleteQuote(this)"><small class=" pl-1 pr-1">Delete</small></button></td>
                        </tr>`
                savedTemplateTable.getElementsByTagName('tBody')[0].insertAdjacentHTML("afterbegin", newRow)
            }
            else {
                let newRow = `
                        <tr id ="quote_id_${copied_quote_info['quote_id']}" class="text-danger">  
                            <td>${copied_quote_info['quote_name']}${diy_badge}</td>
                            <td>${copied_quote_info['quoted_by']}</td>
                            <td>${copied_quote_info['date_quote_created']}</td>
                            <td >  ${copied_quote_info['rev_date']}</td>
                            <td>${copied_quote_info['customer_name']}</td>
                            <td ><a href="/add_quote_details/${copied_quote_info['quote_name']}" type="button" class="btn btn-sm btn-primary full-width p-0 m-0 "><small class=" pl-1 pr-1">Modify</small></a></td>
                            <td ><a href="/view_quote/${copied_quote_info['quote_name']}" type="button" class="btn btn-sm btn-info full-width p-0 m-0"><small class=" pl-1 pr-1">View</small></a></td>
                            <td ><a href="/edit_quote/${copied_quote_info['quote_id']}" type="button" class="btn btn-sm btn-success full-width p-0 m-0"><small class=" pl-1 pr-1">Edit</small></a></td>
                            <td ><button type="button" class="btn btn-sm btn-secondary full-width p-0 m-0 " data-quote_name ="${copied_quote_info['quote_name']}" data-quote_id ="${copied_quote_info['quote_id']}" onclick="copyQuoteAndDetails(this)"><small class=" pl-1 pr-1">Copy</small></button></td>
                            <td ><button  type="button" class="btn btn-sm btn-danger full-width p-0 m-0" data-quote_name ="${copied_quote_info['quote_name']}" data-quote_id="${copied_quote_info['quote_id']}" data-is_template="${copied_quote_info['is_template']}" onclick="deleteQuote(this)"><small class=" pl-1 pr-1">Delete</small></button></td>
                            
                        </tr>`
                // <td><a href="/update_quote_status/${copied_quote_info['quote_id']}" type="button" class="btn btn-sm btn-warning full-width p-0 m-0"><small class=" pl-1 pr-1">Update status</small></a></td>
                savedQuoteTable.getElementsByTagName('tBody')[0].insertAdjacentHTML("afterbegin", newRow)
            }
        }
        else {
            alert("Quote not deleted!");

        }
        toggleMessageModal("", false);  //Close modal
    }
    else {
        return
    }
}
// END- COPY AND ADD THE COPIED QUOTE IN THE TOP ROW OF THE TABLE

