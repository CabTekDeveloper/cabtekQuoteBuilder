// Updated  : 21-09-2023
// By       : Wangchuk

let quoteDateTable = document.getElementById('quote_date_table')
// let pageTitle = document.querySelector('title')
let divsToHide = document.getElementsByClassName('hide_in_printing_div')
let divForPrinting = document.getElementById('div_for_printing')
let joinerySupplyTypeHeader = document.getElementById('joinery_supply_type_header')
// let joinerySupplyTypeSelectTag = document.getElementById('joinery_supply_type')

// Update joinery supply type header
function updateJoinerySupplyType(joinerySupplyTypeSelectTag) {
    let quoteId = joinerySupplyTypeSelectTag.getAttribute('data-quote_id')
    let joinerySupplyType = joinerySupplyTypeSelectTag.value

    if (joinerySupplyType == null || joinerySupplyType.trim().length == 0) {
        return
    }
    
    const formData = new FormData();
    formData.append("quote_id", quoteId)
    formData.append("joinery_supply_type", joinerySupplyType)
    const url = "/update_joinery_supply_type_db"
    const options = {
        method: "POST",
        body: formData
    }

    fetch(url, options)
        .then(res => res.json())
        .then(data => {
            if (data && data['updated'] == true) {
                joinerySupplyTypeHeader.innerText = joinerySupplyType
                joinerySupplyTypeHeader.classList.add('text-danger')
                
                setTimeout(() => {
                    joinerySupplyTypeHeader.classList.remove('text-danger')
                }, 500);
            }
        })

}

// Add new rev data to quote
function addRevDate(btn) {
    let quoteId = btn.getAttribute('data-quote_id')

    if (confirm(`Are you sure you add a new rev date?`) == true) {
        const formData = new FormData();
        formData.append("quote_id", quoteId)
        const url = "/add_new_rev_date_db"
        const options = {
            method: "POST",
            body: formData
        }

        fetch(url, options)
            .then(res => res.json())
            .then(data => {
                if (data) {
                    let quoteName = data['quote_name']
                    let revisionDates = data['revision_dates'].trim().split('|')

                    let revCount = revisionDates.length
                    let newRevDate = revisionDates.pop()

                    let tBody = quoteDateTable.getElementsByTagName('tBody')[0]
                    let newRow = `<tr>
                                    <td class="font-weight-normal ">Rev ${revCount} </td>
                                    <td class="font-weight-normal p-0 m-0 pr-1 align-text-top ">: </td>
                                    <td class="font-weight-normal text-left"> ${newRevDate}</td>
                                </tr>`

                    // insert new rev date 
                    tBody.insertAdjacentHTML("beforeend", newRow)

                    // update page title of view_quote.html
                    let newPageTitle = `${quoteName}_rev_${revCount}`
                    document.title = newPageTitle
                }

            })
    }

}

// Format table so that it takes full width of viewport when printing

function printQuote() {
    window.print()
}

window.onbeforeprint = function () {
    for (let i = 0; i < divsToHide.length; i++) {
        divsToHide[i].classList.add('hide')
    }
    divForPrinting.classList.add('col-md-12')
}

window.onafterprint = function () {
    for (let i = 0; i < divsToHide.length; i++) {
        divsToHide[i].classList.remove('hide')
    }
    divForPrinting.classList.remove('col-md-12')
}
// end

function addBorderBottom(tableRow) {
    tableRow.classList.toggle('border-bottom-3')
}

function addBlankData(tableRow) {
    let emptyRow = `<h6 onclick="removeBlankData(this)">&nbsp;<small class=" font-italic btn-link text-danger disable-in-printing">- blank space<small></small></h6>`
    tableRow.insertAdjacentHTML('afterend', emptyRow)
}

function removeBlankData(tableRow) {
    tableRow.remove()
}