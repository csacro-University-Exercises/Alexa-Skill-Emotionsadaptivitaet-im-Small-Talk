# Rechte für `Alexa`@`localhost`

GRANT SELECT, INSERT, UPDATE, DELETE ON *.* TO 'Alexa'@'localhost' IDENTIFIED BY PASSWORD 'axelA' WITH MAX_USER_CONNECTIONS 1;

GRANT SELECT, INSERT, UPDATE, DELETE ON `alexasmalltalkemotion`.* TO 'Alexa'@'localhost';