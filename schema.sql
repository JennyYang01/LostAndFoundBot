DROP TABLE IF EXISTS user;

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  age INTEGER,
  height INTEGER,
  weight INTEGER,
  if_found BIT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);