import requests

# Test de connexion
r = requests.post('http://localhost:8001/auth/login', json={'email': 'test@example.com', 'password': 'test123'})
print('Login:', r.status_code, r.text)

if r.status_code == 200:
    token = r.json()['access_token']
    print('Token:', token[:50] + '...')
    
    # Test de prédiction
    headers = {'Authorization': f'Bearer {token}'}
    data = {
        'age': 25, 'gender': 'Male', 'height': 1.75, 'weight': 70,
        'family_history_with_overweight': 'no', 'favc': 'no', 'fcvc': 2.5,
        'ncp': 3, 'caec': 'sometimes', 'smoke': 'no', 'ch2o': 2.5,
        'scc': 'no', 'faf': 1.5, 'tue': 2.5, 'cal': 0, 'mtrans': 'Public_Transportation'
    }
    
    r2 = requests.post('http://localhost:8001/predictions/predict', json=data, headers=headers)
    print('Prediction:', r2.status_code, r2.text)
