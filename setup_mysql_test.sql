-- prepares a MySQL server for the project test
CREATE DATABASE IF NOT EXISTS hbnb_test_db;
CREATE USER IF NOT EXISTS 'hbnb_test'@'localhost' IDENTIFIED BY 'hbnb_test_pwd';
GRANT ALL PRIVILEGES on hbnb_dev_db. * to 'hbnb_test_db'@'localhost';
GRANT SELECT ON performance_schema.* TO 'hbnb_test_db'@'localhost';
FLUSH PRIVILEGES;
