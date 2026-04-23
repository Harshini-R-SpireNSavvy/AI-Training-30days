-- CLEAN UP
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS answers;
DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS employees;

-- EMPLOYEES
CREATE TABLE employees (
    emp_id INT PRIMARY KEY,
    name VARCHAR(50),
    department VARCHAR(50)
);

-- CATEGORIES
CREATE TABLE categories (
    category_id INT PRIMARY KEY,
    category_name VARCHAR(50)
);

-- QUESTIONS
CREATE TABLE questions (
    question_id INT PRIMARY KEY,
    question_text TEXT,
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- ANSWERS
CREATE TABLE answers (
    answer_id INT PRIMARY KEY,
    question_id INT,
    answer_text TEXT,
    FOREIGN KEY (question_id) REFERENCES questions(question_id)
);

-- RATINGS
CREATE TABLE ratings (
    rating_id INT PRIMARY KEY,
    emp_id INT,
    answer_id INT,
    rating INT,
    FOREIGN KEY (emp_id) REFERENCES employees(emp_id),
    FOREIGN KEY (answer_id) REFERENCES answers(answer_id)
);

-- EMPLOYEES
INSERT INTO employees VALUES
(1, 'Amit', 'HR'),
(2, 'Priya', 'Finance'),
(3, 'Rahul', 'IT'),
(4, 'Sneha', 'HR'),
(5, 'Kiran', 'IT');

-- CATEGORIES
INSERT INTO categories VALUES
(1, 'Leave'),
(2, 'Payroll'),
(3, 'Benefits'),
(4, 'Policy');

-- QUESTIONS
INSERT INTO questions VALUES
(1, 'How to apply leave?', 1),
(2, 'How is salary calculated?', 2),
(3, 'What are employee benefits?', 3),
(4, 'What is company policy?', 4),
(5, 'Leave balance check?', 1),
(6, 'Bonus eligibility?', 2),
(7, 'Health insurance details?', 3),
(8, 'Work from home policy?', 4);

-- ANSWERS
INSERT INTO answers VALUES
(1, 1, 'Apply via HR portal'),
(2, 2, 'Based on salary structure'),
(3, 3, 'Includes insurance and PF'),
(4, 4, 'Follow company handbook'),
(5, 5, 'Check in dashboard'),
(6, 6, 'Depends on performance'),
(7, 7, 'Covered under company plan'),
(8, 8, 'Allowed with approval');

-- RATINGS
INSERT INTO ratings VALUES
(1, 1, 1, 5),
(2, 2, 2, 4),
(3, 3, 3, 5),
(4, 4, 4, 3),
(5, 5, 1, 4);


SELECT c.category_name, COUNT(q.question_id) AS total_questions
FROM categories c
LEFT JOIN questions q ON c.category_id = q.category_id
GROUP BY c.category_name;


SELECT a.answer_text, AVG(r.rating) AS avg_rating
FROM answers a
JOIN ratings r ON a.answer_id = r.answer_id
GROUP BY a.answer_text
ORDER BY avg_rating DESC
LIMIT 3;


SELECT q.question_text
FROM questions q
LEFT JOIN answers a ON q.question_id = a.question_id
WHERE a.answer_id IS NULL;


SELECT c.category_name, AVG(r.rating) AS avg_rating
FROM categories c
JOIN questions q ON c.category_id = q.category_id
JOIN answers a ON q.question_id = a.question_id
JOIN ratings r ON a.answer_id = r.answer_id
GROUP BY c.category_name;


SELECT e.name, COUNT(r.rating_id) AS total_ratings
FROM employees e
JOIN ratings r ON e.emp_id = r.emp_id
GROUP BY e.name
HAVING COUNT(r.rating_id) > 3;