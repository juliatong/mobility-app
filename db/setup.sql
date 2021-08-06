drop database IF EXISTS `mobility_data`;
create database `mobility_data`;

CREATE TABLE `mobility_data`.`regions` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `geo_type` ENUM ("country_region", "city", "sub_region", "county"),
  `name` VARCHAR(255) NULL,
  INDEX (`geo_type`),
  PRIMARY KEY (`id`));


CREATE TABLE `mobility_data`.`locations` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `region_id` BIGINT NOT NULL,
  `alternative_name` VARCHAR(255) NULL,
  `sub_region` VARCHAR(255) NULL,
  `country` VARCHAR(255) NULL,
  INDEX (`region_id`),
  PRIMARY KEY (`id`));


CREATE TABLE `mobility_data`.`direction_requests` (
  `id` BIGINT NOT NULL AUTO_INCREMENT,
  `location_id` BIGINT NOT NULL,
  `transportation_type` ENUM ("driving", "transit", "walking") NOT NULL,
  `request_date` DATE NOT NULL,
  `requests` DECIMAL(10,2) NOT NULL,
  INDEX (`location_id`),
  INDEX (`transportation_type`),
  PRIMARY KEY (`id`));

