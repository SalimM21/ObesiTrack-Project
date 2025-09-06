const form = document.getElementById('login-form');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const data = Object.fromEntries(new FormData(form));
  const res = await fetch('/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const json = await res.json();
  if(json.access_token){
    localStorage.setItem('jwt', json.access_token);
    window.location.href = 'predict.html';
  } else {
    document.getElementById('message').textContent = json.detail || "Erreur de connexion";
  }
});
