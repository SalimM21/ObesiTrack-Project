-- 🔹 20 utilisateurs
INSERT INTO users (full_name, email, hashed_password, role) VALUES
('Alice Dupont', 'alice1@example.com', 'hashed_password123', 'user'),
('Jean Martin', 'jean2@example.com', 'hashed_password123', 'user'),
('Sarah Bernard', 'sarah3@example.com', 'hashed_password123', 'user'),
('David Laurent', 'david4@example.com', 'hashed_password123', 'user'),
('Emma Richard', 'emma5@example.com', 'hashed_password123', 'user'),
('Lucas Petit', 'lucas6@example.com', 'hashed_password123', 'user'),
('Marie Fabre', 'marie7@example.com', 'hashed_password123', 'user'),
('Hugo Leroy', 'hugo8@example.com', 'hashed_password123', 'user'),
('Chloé Moreau', 'chloe9@example.com', 'hashed_password123', 'user'),
('Antoine Garcia', 'antoine10@example.com', 'hashed_password123', 'user'),
('Julie Thomas', 'julie11@example.com', 'hashed_password123', 'user'),
('Louis Renaud', 'louis12@example.com', 'hashed_password123', 'user'),
('Manon Leclerc', 'manon13@example.com', 'hashed_password123', 'user'),
('Paul Robert', 'paul14@example.com', 'hashed_password123', 'user'),
('Laura Fontaine', 'laura15@example.com', 'hashed_password123', 'user'),
('Maxime Olivier', 'maxime16@example.com', 'hashed_password123', 'user'),
('Camille Chevalier', 'camille17@example.com', 'hashed_password123', 'user'),
('Thomas Lemoine', 'thomas18@example.com', 'hashed_password123', 'user'),
('Élise Blanc', 'elise19@example.com', 'hashed_password123', 'user'),
('Nicolas Dupuis', 'nicolas20@example.com', 'hashed_password123', 'user');

-- 🔹 10 administrateurs
INSERT INTO users (full_name, email, hashed_password, role) VALUES
('Admin One', 'admin1@example.com', 'hashed_admin123', 'admin'),
('Admin Two', 'admin2@example.com', 'hashed_admin123', 'admin'),
('Admin Three', 'admin3@example.com', 'hashed_admin123', 'admin'),
('Admin Four', 'admin4@example.com', 'hashed_admin123', 'admin'),
('Admin Five', 'admin5@example.com', 'hashed_admin123', 'admin'),
('Admin Six', 'admin6@example.com', 'hashed_admin123', 'admin'),
('Admin Seven', 'admin7@example.com', 'hashed_admin123', 'admin'),
('Admin Eight', 'admin8@example.com', 'hashed_admin123', 'admin'),
('Admin Nine', 'admin9@example.com', 'hashed_admin123', 'admin'),
('Admin Ten', 'admin10@example.com', 'hashed_admin123', 'admin');

-- 🔹 30 prédictions (ici associées arbitrairement aux user_id entre 1 et 30)
INSERT INTO predictions (user_id, payload, result, probability) VALUES
(1, '{"age": 25, "gender": "Male", "height": 1.80, "weight": 75}', 'Normal', 0.85),
(2, '{"age": 30, "gender": "Female", "height": 1.65, "weight": 82}', 'Overweight', 0.91),
(3, '{"age": 45, "gender": "Male", "height": 1.70, "weight": 95}', 'Obese', 0.88),
(4, '{"age": 19, "gender": "Female", "height": 1.60, "weight": 50}', 'Normal', 0.93),
(5, '{"age": 55, "gender": "Male", "height": 1.75, "weight": 110}', 'Obese', 0.97),
(6, '{"age": 28, "gender": "Female", "height": 1.68, "weight": 72}', 'Overweight', 0.80),
(7, '{"age": 40, "gender": "Male", "height": 1.82, "weight": 77}', 'Normal', 0.87),
(8, '{"age": 22, "gender": "Female", "height": 1.55, "weight": 65}', 'Overweight', 0.82),
(9, '{"age": 33, "gender": "Male", "height": 1.78, "weight": 99}', 'Obese', 0.95),
(10, '{"age": 27, "gender": "Female", "height": 1.70, "weight": 60}', 'Normal', 0.90),
-- (👉 ajoute les 20 autres prédictions de la même manière)
(30, '{"age": 42, "gender": "Male", "height": 1.85, "weight": 120}', 'Obese', 0.92);
