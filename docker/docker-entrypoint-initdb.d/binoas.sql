ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY 'jodal';
CREATE DATABASE IF NOT EXISTS `jodal`;

-- CREATE TABLE IF NOT EXISTS `jodal`.`user` (
--   `id` INT(11) NOT NULL PRIMARY KEY AUTO_INCREMENT,
--   `application` VARCHAR(255) NOT NULL,
--   `email` VARCHAR(255) NOT NULL,
--   unique index idx_application_email (application, email)
-- );
