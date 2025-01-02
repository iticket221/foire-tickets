let tickets = [];

// Charger les tickets depuis l'API
async function loadTickets() {
    const response = await fetch('/api/tickets');
    tickets = await response.json();
    displayTickets();
}

// Afficher les tickets disponibles
function displayTickets() {
    const ticketsList = document.getElementById('tickets-list');
    ticketsList.innerHTML = tickets.map(ticket => `
        <div class="col-md-12 mb-3">
            <div class="ticket-card">
                <h3>${ticket.type}</h3>
                <p class="price">${ticket.price.toFixed(0)} F CFA</p>
                <button onclick="vendreTicket()" class="btn btn-success btn-lg w-100">Vendre</button>
            </div>
        </div>
    `).join('');
}

// Vendre un ticket
async function vendreTicket() {
    try {
        const response = await fetch('/api/purchase', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({})
        });

        if (!response.ok) {
            throw new Error('Erreur lors de la vente du ticket');
        }

        const result = await response.json();
        if (result.success) {
            document.getElementById('achat-section').style.display = 'none';
            document.getElementById('recu-section').style.display = 'block';
            
            // Mettre à jour les informations du ticket
            document.querySelector('.ticket-number').textContent = `N° ${result.tickets[0].id}`;
            document.getElementById('ticket-type').textContent = tickets[0].type;
            document.getElementById('ticket-price').textContent = tickets[0].price;
            document.getElementById('ticket-date').textContent = new Date().toLocaleString('fr-FR');
            
            // Lancer l'impression automatiquement
            setTimeout(() => {
                window.print();
            }, 500);
        } else {
            alert(result.message || 'Erreur lors de la vente du ticket');
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la vente du ticket');
    }
}

function retourAchat() {
    document.getElementById('achat-section').style.display = 'block';
    document.getElementById('recu-section').style.display = 'none';
    loadTickets(); // Recharger les tickets disponibles
}

// Initialisation
document.addEventListener('DOMContentLoaded', () => {
    loadTickets();
});
