CREATE TABLE IF NOT EXISTS person (
    person_id SERIAL PRIMARY KEY,
    person_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    pass VARCHAR(100) NOT NULL,
    person_type VARCHAR(20) NOT NULL,
    is_verified BOOLEAN NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS quiz (
    quiz_id SERIAL PRIMARY KEY,
    quiz_name VARCHAR(100) NOT NULL,
    teacher_id INTEGER REFERENCES person(person_id),
    category VARCHAR(50),
    difficulty_level VARCHAR(20),
    question_type VARCHAR(20),
    questions JSONB
);

CREATE TABLE IF NOT EXISTS score (
    score_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES person(person_id),
    quiz_id INTEGER REFERENCES quiz(quiz_id),
    score INTEGER
);

CREATE TABLE IF NOT EXISTS solved_quiz (
    solved_quiz_id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES person(person_id),
    quiz_id INTEGER REFERENCES quiz(quiz_id),
    token VARCHAR(100) UNIQUE,
    student_answers JSONB,
    score INTEGER,
    submission_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS shared_results (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quiz(quiz_id),
    sender_id INTEGER REFERENCES person(person_id),
    receiver_id INTEGER REFERENCES person(person_id),
    token VARCHAR(100) UNIQUE NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiration_date INTERVAL,
    status VARCHAR(20) DEFAULT 'active'
);

CREATE TABLE IF NOT EXISTS shared_results (
    shared_result_id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quiz(quiz_id),
    sender_id INTEGER REFERENCES person(person_id),
    receiver_id INTEGER REFERENCES person(person_id),
    token VARCHAR(100),
    expiration_date TIMESTAMP WITHOUT TIME ZONE,
    status VARCHAR(20),
    score INTEGER
);

