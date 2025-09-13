// === URL de l'API FastAPI ===
const API_URL = "http://localhost:8001";

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
        if (!token) {
            throw new Error("Token d'authentification manquant. Veuillez vous connecter.");
        }
        headers["Authorization"] = `Bearer ${token}`;
    }

    console.log(`🌐 Requête ${method} vers ${API_URL}${endpoint}`);
    if (auth) {
        console.log(`🔑 Token utilisé: ${getToken()?.substring(0, 20)}...`);
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        method,
        headers,
        body: data ? JSON.stringify(data) : null
    });

    console.log(`📊 Réponse: ${response.status} ${response.statusText}`);

    if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Erreur API: ${response.status} - ${errorText}`);
        
        if (response.status === 401) {
            // Token expiré ou invalide
            clearToken();
            throw new Error("Session expirée. Veuillez vous reconnecter.");
        }
        
        throw new Error(`Erreur ${response.status}: ${errorText}`);
    }

    return response.json();
}

// === INSCRIPTION ===
async function registerUser(email, password, fullName) {
    try {
        const result = await apiRequest("/auth/signup", "POST", { 
            email, 
            password, 
            full_name: fullName 
        });
        alert("Inscription réussie ! Vous pouvez maintenant vous connecter.");
        return result;
    } catch (err) {
        alert("Erreur d'inscription : " + err.message);
    }
}

// === CONNEXION ===
async function loginUser(email, password) {
    try {
        console.log("🔐 Tentative de connexion pour:", email);
        const result = await apiRequest("/auth/login", "POST", { 
            email, 
            password 
        });
        
        console.log("✅ Connexion réussie, token reçu:", result.access_token?.substring(0, 20) + "...");
        saveToken(result.access_token);
        
        // Vérifier que le token est bien sauvegardé
        const savedToken = getToken();
        if (savedToken) {
            console.log("💾 Token sauvegardé avec succès");
            alert("Connexion réussie 🎉");
            window.location.href = "dashboard.html";
        } else {
            throw new Error("Erreur lors de la sauvegarde du token");
        }
    } catch (err) {
        console.error("❌ Erreur de connexion:", err);
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
        const result = await apiRequest("/predictions/predict", "POST", data, true);
        console.log("Résultat prédiction :", result);
        return result;
    } catch (err) {
        alert("Erreur lors de la prédiction : " + err.message);
        throw err;
    }
}

// === CONSULTER L'HISTORIQUE DES PREDICTIONS ===
async function getHistory() {
    try {
        const result = await apiRequest("/predictions/me", "GET", null, true);
        console.log("Historique :", result);
        return result;
    } catch (err) {
        alert("Erreur lors du chargement de l'historique : " + err.message);
        return [];
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

