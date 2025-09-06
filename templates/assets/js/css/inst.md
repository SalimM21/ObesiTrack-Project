<!-- 
1️⃣ Structure générale
On passe à un layout plus moderne avec header/nav, footer, et contenu central.
Header : logo ObesiTrack + navigation (Home, Prédiction, Historique, Admin si admin, Logout)
Footer : mentions légales + version de l’API
Main : container responsive pour les formulaires et tableaux
Utilisation de CSS Grid / Flexbox pour un design responsive.

2️⃣ Pages HTML principales
a) Page d’inscription / login (register.html / login.html)
Formulaire centré, input stylisés, bouton coloré
Messages d’erreur/succès animés
JS pour validation côté client

b) Page de prédiction (predict.html)
Formulaire clair pour soumettre les données
Affichage graphique des probabilités avec Chart.js
Feedback rapide et visuel

c) Page historique (history.html)
Tableau stylisé avec CSS Grid / Flexbox
Pagination ou scroll infini
Boutons pour voir détail ou revenir en arrière

d) Page admin (admin_users.html)
Tableau avec boutons stylisés pour Supprimer et Changer rôle
Feedback visuel sur succès/erreur des actions

3️⃣ Suggestions globales
Responsive : media queries pour mobile/tablette
UX améliorée : loader pour requêtes API
JS modulable : fichiers séparés pour chaque page (register.js, predict.js, history.js)
Couleurs cohérentes : vert pour succès, rouge pour erreurs, bleu pour info
utiliser Tailwind pour gagner du temps -->
