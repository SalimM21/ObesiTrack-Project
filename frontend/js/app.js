// === URL de l'API FastAPI ===
const API_URL = "http://localhost:8000";

// === Sauvegarder et récupérer le JWT ===
function saveToken(token) {
    localStorage.setItem("jwt", token);
}

function getToken() {
    return localStorage.getItem("jwt");
}

function clearToken() {
    localStorage.removeItem("jwt");
}

// === Requête générique avec ou sans JWT ===
async function apiRequest(endpoint, method = "GET", data = null, auth = false) {
    const headers = { "Content-Type": "application/json" };
    if (auth) {
        const token = getToken();
        if (token) {
            headers["Authorization"] = `Bearer ${token}`;
        }
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        method,
        headers,
        body: data ? JSON.stringify(data) : null
    });

    if (!response.ok) {
        throw new Error(`Erreur ${response.status}: ${await response.text()}`);
    }

    return response.json();
}

// === INSCRIPTION ===
async function registerUser(username, password) {
    try {
        const result = await apiRequest("/auth/register", "POST", { username, password });
        alert("Inscription réussie Vous pouvez maintenant vous connecter.");
        return result;
    } catch (err) {
        alert("Erreur d'inscription : " + err.message);
    }
}

// === CONNEXION ===
async function loginUser(username, password) {
    try {
        const result = await apiRequest("/auth/login", "POST", { username, password });
        saveToken(result.access_token);
        alert("Connexion réussie 🎉");
        window.location.href = "dashboard.html"; // redirection après connexion
    } catch (err) {
        alert("Erreur de connexion : " + err.message);
    }
}

// === DÉCONNEXION ===
function logoutUser() {
    clearToken();
    alert("Déconnecté ✅");
    window.location.href = "index.html";
}

// === ENVOYER DES DONNÉES POUR PREDICTION ===
async function sendPrediction(data) {
    try {
        const result = await apiRequest("/predictions", "POST", data, true);
        console.log("Résultat prédiction :", result);
        alert(`Prédiction : ${result.prediction} (probabilité : ${result.probability}%)`);
        return result;
    } catch (err) {
        alert("Erreur lors de la prédiction : " + err.message);
    }
}

// === CONSULTER L'HISTORIQUE DES PREDICTIONS ===
async function getHistory() {
    try {
        const result = await apiRequest("/predictions/history", "GET", null, true);
        console.log("Historique :", result);
        return result;
    } catch (err) {
        alert("Erreur lors du chargement de l'historique : " + err.message);
    }
}

// === GESTION ADMIN : LISTE DES UTILISATEURS ===
async function getUsers() {
    try {
        const result = await apiRequest("/users", "GET", null, true);
        console.log("Utilisateurs :", result);
        return result;
    } catch (err) {
        alert("Erreur lors du chargement des utilisateurs : " + err.message);
    }
}


// -----------------------------
// Pagination
// -----------------------------
let currentPage = 1;
const rowsPerPage = 5;

// Charger les utilisateurs
async function fetchUsers(dateFilter = null) {
    let url = `${API_URL}/users?page=${currentPage}&limit=${rowsPerPage}`;
    if (dateFilter) url += `&date=${dateFilter}`;

    const res = await fetch(url, { headers: getAuthHeaders() });
    if (!res.ok) return alert("Erreur lors de la récupération des utilisateurs !");
    const data = await res.json();

    populateTable(data.users);
    document.getElementById('page-info').innerText = `Page ${currentPage} / ${data.total_pages}`;
}

// Remplir le tableau
function populateTable(users) {
    const tbody = document.querySelector('#users-table tbody');
    tbody.innerHTML = '';
    users.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${user.id}</td>
            <td>${user.name}</td>
            <td>${user.email}</td>
            <td>${user.role}</td>
            <td>${user.created_at}</td>
            <td>
                <button class="btn-action btn-edit" onclick="toggleRole(${user.id}, '${user.role}')">Changer rôle</button>
                <button class="btn-action btn-delete" onclick="deleteUser(${user.id})">Supprimer</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

// -----------------------------
// Changer rôle utilisateur
// -----------------------------
async function toggleRole(userId, currentRole) {
    if (!confirm("Confirmer le changement de rôle?")) return;
    const newRole = currentRole === "admin" ? "user" : "admin";

    const res = await fetch(`${API_URL}/users/${userId}/role`, {
        method: "PATCH",
        headers: getAuthHeaders(),
        body: JSON.stringify({ role: newRole })
    });
    if (!res.ok) return alert("Erreur lors du changement de rôle !");
    fetchUsers(document.getElementById('filter-date').value);
}

// -----------------------------
// Supprimer utilisateur
// -----------------------------
async function deleteUser(userId) {
    if (!confirm("Confirmer la suppression de cet utilisateur?")) return;

    const res = await fetch(`${API_URL}/users/${userId}`, {
        method: "DELETE",
        headers: getAuthHeaders()
    });
    if (!res.ok) return alert("Erreur lors de la suppression !");
    fetchUsers(document.getElementById('filter-date').value);
}

// -----------------------------
// Filtre par date
// -----------------------------
document.getElementById('filter-date').addEventListener('change', (e) => {
    currentPage = 1;
    fetchUsers(e.target.value);
});

// -----------------------------
// Pagination boutons
// -----------------------------
document.getElementById('prev-page').addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        fetchUsers(document.getElementById('filter-date').value);
    }
});
document.getElementById('next-page').addEventListener('click', () => {
    currentPage++;
    fetchUsers(document.getElementById('filter-date').value);
});

// -----------------------------
// Graphique probabilités
// -----------------------------
const ctx = document.getElementById('predictionChart').getContext('2d');
const predictionChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: ['Obèse', 'Non Obèse'],
        datasets: [{
            label: 'Probabilités',
            data: [0.7, 0.3], // à remplacer par l'API
            backgroundColor: ['#f87171','#4ade80']
        }]
    },
    options: {
        responsive: true,
        plugins: { legend: { display: false } }
    }
});

// -----------------------------
// Logout
// -----------------------------
function logout() {
    localStorage.removeItem('token');
    return true;
}

// -----------------------------
// Initialisation
// -----------------------------
window.addEventListener('DOMContentLoaded', () => {
    if (!token) {
        alert("Veuillez vous connecter !");
        window.location.href = "/login";
    }
    fetchUsers();
});

