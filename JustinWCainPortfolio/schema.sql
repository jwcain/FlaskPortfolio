DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS recipe;
DROP TABLE IF EXISTS recipe_step;
DROP TABLE IF EXISTS recipe_ingredient;
DROP TABLE IF EXISTS project;
DROP TABLE IF EXISTS work_experience;
DROP TABLE IF EXISTS work_experience_point;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
);

CREATE TABLE recipe (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  info TEXT NOT NULL
);


CREATE TABLE recipe_step (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  step_id INTEGER NOT NULL,
  info TEXT NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES recipe (id)
);

CREATE TABLE recipe_ingredient (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  recipe_id INTEGER NOT NULL,
  step_id INTEGER NOT NULL,
  amount TEXT NOT NULL,
  ingredient_name TEXT NOT NULL,
  FOREIGN KEY (recipe_id) REFERENCES recipe (id),
  FOREIGN KEY (step_id) REFERENCES recipe_step (id)
);

CREATE TABLE project (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  shown BOOLEAN NOT NULL,
  programming_language TEXT NOT NULL,
  tools_used TEXT NOT NULL,
  title TEXT NOT NULL,
  info TEXT NOT NULL,
  link_github TEXT NOT NULL,
  link_live TEXT NOT NULL,
  last_updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE work_experience (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  shown BOOLEAN NOT NULL,
  title TEXT NOT NULL,
  one_liner TEXT NOT NULL,
  dates TEXT NOT NULL,
  work_location TEXT NOT NULL
);

CREATE TABLE work_experience_point (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  work_experience_id INTEGER NOT NULL,
  info TEXT NOT NULL,
  FOREIGN KEY (work_experience_id) REFERENCES work_experience (id)
);