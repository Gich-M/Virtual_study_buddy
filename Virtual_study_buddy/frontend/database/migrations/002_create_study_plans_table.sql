CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    otp_secret TEXT,
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES user (email) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS study_plan (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tags TEXT,
    attachments TEXT,
    comments TEXT,
    priority INTEGER NOT NULL DEFAULT 1,
    progress INTEGER NOT NULL DEFAULT 0,
    due_date TIMESTAMP,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS study_material (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    link TEXT NOT NULL,
    tags TEXT,
    attachments TEXT,
    comments TEXT,
    priority INTEGER NOT NULL DEFAULT 1,
    progress INTEGER NOT NULL DEFAULT 0,
    due_date TIMESTAMP,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS study_session (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    tags TEXT,
    attachments TEXT,
    comments TEXT,
    priority INTEGER NOT NULL DEFAULT 1,
    progress INTEGER NOT NULL DEFAULT 0,
    due_date TIMESTAMP,
    owner_id INTEGER NOT NULL,
    study_plan_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user (id) ON DELETE CASCADE,
    FOREIGN KEY (study_plan_id) REFERENCES study_plan (id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reminder (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    reminder_time TIMESTAMP NOT NULL,
    tags TEXT,
    attachments TEXT,
    comments TEXT,
    priority INTEGER NOT NULL DEFAULT 1,
    progress INTEGER NOT NULL DEFAULT 0,
    due_date TIMESTAMP,
    owner_id INTEGER NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES user (id) ON DELETE CASCADE
);