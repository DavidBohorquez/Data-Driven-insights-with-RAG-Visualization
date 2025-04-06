-- Create the authors table if it doesn't exist
CREATE TABLE IF NOT EXISTS authors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create the journals table if it doesn't exist
CREATE TABLE IF NOT EXISTS journals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);

-- Create the publications table if it doesn't exist
CREATE TABLE IF NOT EXISTS publications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    journal_id INTEGER NOT NULL,
    publication_date TEXT NOT NULL,
    FOREIGN KEY (journal_id) REFERENCES journals(id)
);

-- Create the junction table for authors and publications if it doesn't exist
CREATE TABLE IF NOT EXISTS publication_authors (
    publication_id INTEGER NOT NULL,
    author_id INTEGER NOT NULL,
    PRIMARY KEY (publication_id, author_id),
    FOREIGN KEY (publication_id) REFERENCES publications(id),
    FOREIGN KEY (author_id) REFERENCES authors(id)
);

-- Insert unique journals if they don't already exist
INSERT OR IGNORE INTO journals (name) VALUES
('JAAD International'),
('Automatica (2023) 111384'),
('BCB ’23: Proceedings of the 14th ACM International Conference on Bioinformatics, Computational Biology, and Health Informatics'),
('EHSF 2023, Florence'),
('Mathematics 2022, 10, 1410'),
('WiOpt 2019: 1-8'),
('J Optim Theory Appl'),
('In Biomedical and Other Applications of Soft Computing (pp. 155-163). Cham: Springer International Publishing'),
('International Mathematics Research Notices, 2020(23), 9228-9292'),
('Signal Processing, 188, 108185'),
('Communications in Mathematical Sciences, 19(7), 1761‑1798'),
('arXiv preprint arXiv:2106.13463'),
('Telemedicine and e-Health, 27(5), 495‑502'),
('Archives of Dermatological Research, 314(2), 183‑190'),
('Biology, 9(12), 477'),
('Journal of the American Academy of Dermatology, 84(5), 1269‑1277'),
('Revista de la Real Academia de Ciencias Exactas, Físicas y Naturales. Serie A. Matemáticas, 114(4), 186'),
('Dynamic Data Assimilation – Beating the Uncertainties'),
('ESAIM: Proceedings and Surveys, 67, 135-160'),
('hal-02379881, version 1 (25-11-2019)'),
('[Research Report] Rapport LAAS n° 19357, ISIC2019'),
('arXiv preprint arXiv:1910.02248'),
('IEEE Transactions on Signal Processing, 67(21), 5643-5658');

-- Insert unique authors if they don't already exist
INSERT OR IGNORE INTO authors (name) VALUES
('Hang Nguyen'), ('Léa Gazeau'), ('Jonathan Wolfe'), ('Hon Son Hoang'), ('Remy Baraille'),
('Olivier Talagrand'), ('Nga Nguyen'), ('Alessandra Cartocci'), ('Hoc Huynh'), ('Loan Tong'),
('Milad Mozafari'), ('Khoi Dang'), ('Zung Nguyen'), ('Le, P.B.'), ('Nguyen, Z.T'),
('Jeffrey Pawlick'), ('Thi Thu Hang Nguyen'), ('Edward Colbert'), ('Quanyan Zhu'), ('Truong, T. T.'),
('To, T. D.'), ('Nguyen, T. H.'), ('Nguyen, H. P.'), ('Helmy, M.'), ('Phuong, L. B.'),
('Nguyen, N. T.'), ('Nguyen, T. H. O.'), ('Soussen, C.'), ('Idier, J.'), ('Djermoune, E.'),
('Iglesias, S. F.'), ('Mirrahimi, S.'), ('Protin, F.'), ('Jules, M.'), ('Nguyen, D. T.'),
('Piffault, C.'), ('Rodríguez, W.'), ('Nguyen, T. Z.'), ('Tognetti, L.'), ('Balistreri, A.'),
('Cataldo, G.'), ('Cinotti, E.'), ('Moscarella, E.'), ('Farnetani, F.'), ('Lallas, A.'),
('Tiodorovic, D.'), ('Carrera, C.'), ('Longo, C.'), ('Puig, S.'), ('Perrot, J.'),
('Argenziano, G.'), ('Pellacani, G.'), ('Rubegni, P.'), ('Cevenini, G.'), ('Tat Dat, T.'),
('Frédéric, P.'), ('Duc Thang, N.'), ('Tien Zung, N.'), ('Marín, D.'), ('Mattei, J. F.'),
('Salem, É.'), ('Lebwohl, M.'), ('Kircik, L. H.'), ('Lacour, J.'), ('Liljedahl, M.'),
('Lynde, C.'), ('Mørch, M. H.'), ('Papp, K. A.'), ('Gold, L. S.'), ('Takhar, A.'),
('Thaçi, D.'), ('Warren, R. B.'), ('Wollenberg, A.'), ('Cano, F.'), ('Ravara-Vago, M.'),
('Hoang, H. S.'), ('Baraille, R.'), ('Calvez, V.'), ('Hivert, H.'), ('Méléard, S.'),
('Melnykova, A.'), ('Nordmann, S.'), ('Dinh Thi Lan'), ('Thi Thuy Nga Nguyen'), ('Hoang-Phuong Nguyen');

-- Insert publications if they don't already exist
INSERT OR IGNORE INTO publications (title, journal_id, publication_date) VALUES
('Using artificial intelligence to compute Severity of Alopecia Tool (SALT) scores', 1, 'April 2024'),
('State estimation in presence of uncertain model error statistics based on filter stability. Application to an adaptive filter', 2, '2023'),
('Automatically Measuring Dyspigmentation Severity of the Skin Using a Convolutional Neural Network', 3, 'September 2023'),
('AI-aided automatic severity scoring system for Hidradenitis Suppurativa', 4, '2023'),
('ROC Curves, Loss Functions, and Distorted Probabilities in Binary Classification', 5, '2022'),
('Optimal Timing in Dynamic and Robust Attacker Engagement During Advanced Persistent Threats', 6, '2019'),
('A Fast and Simple Modification of Newton’s Method Avoiding Saddle Points', 7, '2023'),
('Accuracy Measures and the Convexity of ROC Curves for Binary Classification Problems', 8, '2022'),
('Topological Voting Method for Image Segmentation', 9, '2022'),
('K-step analysis of orthogonal greedy algorithms for non-negative sparse representations', 10, '2021'),
('Selection and mutation in a shifting and fluctuating environment', 11, '2021'),
('Unified modelling of epidemics by coupled dynamics via Monte-Carlo Markov Chain algorithms', 12, '2021'),
('Comparative Use of Multiple Electronic Devices in the Teledermoscopic Diagnosis of Early Melanoma', 13, '2021'),
('Dermoscopy of early melanomas: variation according to the anatomic site', 14, '2021'),
('Epidemic dynamics via wavelet theory and machine learning with applications to Covid-19', 15, '2020'),
('Topological moduli space for germs of holomorphic foliations', 9, '2020'),
('Twice-weekly topical calcipotriene betamethasone dipropionate foam as proactive management of plaque psoriasis increases time in remission and is well tolerated over 52 weeks (PSO-LONG trial)', 16, '2020'),
('Invariant hypersurfaces and nodal components for codimension one singular foliations', 17, '2020'),
('Adaptive Filter as Efficient Tool for Data Assimilation under Uncertainties', 18, '2020'),
('Horizontal gene transfer: numerical comparison between stochastic and deterministic approaches', 19, '2020'),
('Dynamics of non cohomologically hyperbolic automorphisms of C 3', 20, '2019'),
('Ensembled Skin Cancer Classification', 21, '2019'),
('A new algorithm for graph center computation and graph partitioning according to the distance to the center', 22, '2019'),
('Non-negative orthogonal greedy algorithms', 23, '2019');

-- Link authors to publications via publication_authors if they don't already exist
INSERT OR IGNORE INTO publication_authors (publication_id, author_id) VALUES
(1, 1), (1, 2), (1, 3), -- Hang Nguyen, Léa Gazeau, Jonathan Wolfe
(2, 4), (2, 5), (2, 6), -- Hon Son Hoang, Remy Baraille, Olivier Talagrand
(3, 2), (3, 1), -- Léa Gazeau, Hang Nguyen
(4, 7), (4, 8), (4, 9), (4, 10), (4, 11), (4, 12), (4, 13), -- Nga Nguyen, Alessandra Cartocci, etc.
(5, 14), (5, 15), -- Le, P.B.; Nguyen, Z.T
(6, 16), (6, 17), (6, 18), (6, 19), -- Jeffrey Pawlick, Thi Thu Hang Nguyen, etc.
(7, 20), (7, 21), (7, 22), (7, 23), (7, 24), -- Truong, T. T., To, T. D., etc.
(8, 25), (8, 13), -- Phuong, L. B., Zung, N. T.
(9, 26), (9, 14), -- Nguyen, N. T., Le, P. B.
(10, 27), (10, 28), (10, 29), (10, 30), -- Nguyen, T. H. O., Soussen, C., etc.
(11, 31), (11, 32), -- Iglesias, S. F., Mirrahimi, S.
(12, 33), (12, 34), (12, 35), (12, 1), (12, 36), (12, 37), (12, 38), -- Protin, F., Jules, M., etc.
(13, 39), (13, 8), (13, 40), (13, 41), (13, 42), (13, 43), (13, 44), (13, 45), (13, 46), (13, 47), (13, 48), (13, 49), (13, 50), (13, 51), (13, 52), (13, 53), (13, 54), -- Tognetti, L., Cartocci, A., etc.
(14, 39), (14, 8), (14, 42), (14, 43), (14, 44), (14, 46), (14, 45), (14, 47), (14, 48), (14, 49), (14, 50), (14, 51), (14, 41), (14, 40), (14, 54), (14, 53), (14, 52), -- Tognetti, L., Cartocci, A., etc.
(15, 55), (15, 56), (15, 1), (15, 34), (15, 57), (15, 36), (15, 58), -- Tat Dat, T., Frédéric, P., etc.
(16, 59), (16, 60), (16, 61), -- Marín, D., Mattei, J. F., Salem, É.
(17, 62), (17, 63), (17, 64), (17, 65), (17, 66), (17, 67), (17, 68), (17, 49), (17, 69), (17, 70), (17, 71), (17, 72), (17, 73), -- Lebwohl, M., Kircik, L. H., etc.
(18, 74), (18, 60), (18, 75), -- Cano, F., Mattei, J. F., Ravara-Vago, M.
(19, 76), (19, 77), -- Hoang, H. S., Baraille, R.
(20, 78), (20, 31), (20, 79), (20, 80), (20, 81), (20, 82), -- Calvez, V., Iglesias, S. F., etc.
(21, 33), -- Protin, F.
(22, 55), (22, 83), (22, 17), (22, 84), (22, 85), -- Tat Dat Tô, Dinh Thi Lan, etc.
(23, 33), -- Protin, F.
(24, 22), (24, 29), (24, 28), (24, 30); -- Nguyen, T. T., Idier, J., etc.
