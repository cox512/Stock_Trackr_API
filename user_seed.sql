DROP TABLE user IF EXISTS;
CREATE TABLE IF NOT EXISTS user;
INSERT INTO user (fname, lname, username, password, created_at) VALUES('Johnny', 'Jim', 'jimmyboy', 'password', date('now'));