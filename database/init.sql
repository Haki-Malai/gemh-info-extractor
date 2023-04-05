CREATE DATABASE IF NOT EXISTS `prod_database`;
CREATE DATABASE IF NOT EXISTS `dev_database`;
CREATE DATABASE IF NOT EXISTS `test_database`;

CREATE USER IF NOT EXISTS 'prod_username'@'%' IDENTIFIED BY 'prod_password';
GRANT ALL PRIVILEGES ON `prod_database`.* TO 'prod_username'@'%';

CREATE USER IF NOT EXISTS 'dev_username'@'%' IDENTIFIED BY 'dev_password';
GRANT ALL PRIVILEGES ON `dev_database`.* TO 'dev_username'@'%';

CREATE USER IF NOT EXISTS 'test_username'@'%' IDENTIFIED BY 'test_password';
GRANT ALL PRIVILEGES ON `test_database`.* TO 'test_username'@'%';
