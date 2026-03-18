// Wangchuk
// 18-03-2026

let socket = io();

// Listen for the 'update_client_list' event from the server
socket.on('update_client_list', (clients) => {
    let countsDiv = document.getElementById('count');
    let clientListDiv = document.getElementById('client_list_div');
    if (clientListDiv !== null && countsDiv !== null) {
        clientListDiv.innerHTML = '';
        countsDiv.textContent = Object.keys(clients).length;

        for (const [key, value] of Object.entries(clients)) {
            let clientInfoHTML = `<div class="col-sm-2  text-right">SID :</div>
                                <div class="col-sm-10  px-0">${key}</div>`

            for (const [itemkey, itemValue] of Object.entries(value)) {
                clientInfoHTML += `<div class="col-sm-2  text-right">${itemkey} :</div>
                                <div class="col-sm-10  px-0">${itemValue}</div>`
            }

            var mainHTML = `<div class="row py-2 bg-secondary text-light mb-1">
                            ${clientInfoHTML}
                      </div>`

            clientListDiv.insertAdjacentHTML('beforeend', mainHTML);
        }

        if (countsDiv !== null && clients !== null) {
            
        }
    }
}
);

