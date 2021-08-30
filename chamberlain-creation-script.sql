-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema chamberlain
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema chamberlain
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `chamberlain` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `chamberlain` ;

-- -----------------------------------------------------
-- Table `chamberlain`.`cardinals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`cardinals` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cardinalId` VARCHAR(45) NOT NULL,
  `cardinalIp` VARCHAR(1000) NULL DEFAULT NULL,
  `description` VARCHAR(1000) NULL DEFAULT NULL,
  `destination` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `chamberlain`.`datasets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`datasets` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `datasetId` VARCHAR(45) NULL DEFAULT NULL,
  `datasetSchema` VARCHAR(1000) NULL DEFAULT NULL,
  `backend` VARCHAR(1000) NULL DEFAULT NULL,
  `parameters` VARCHAR(1000) NULL DEFAULT NULL,
  `description` VARCHAR(1000) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 10
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `chamberlain`.`storageRelationships`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`storageRelationships` (
  `storageRelationshipId` INT NOT NULL AUTO_INCREMENT,
  `datasetId` VARCHAR(45) NULL DEFAULT NULL,
  `cardinals` VARCHAR(1000) NULL DEFAULT NULL,
  `description` VARCHAR(1000) NULL DEFAULT NULL,
  PRIMARY KEY (`storageRelationshipId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `chamberlain`.`workflowRelationships`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`workflowRelationships` (
  `workflowRelationshipId` INT NOT NULL AUTO_INCREMENT,
  `datasetId` VARCHAR(45) NULL DEFAULT NULL,
  `workflowId` VARCHAR(45) NULL DEFAULT NULL,
  `description` VARCHAR(1000) NULL DEFAULT NULL,
  PRIMARY KEY (`workflowRelationshipId`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


-- -----------------------------------------------------
-- Table `chamberlain`.`workflows`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`workflows` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `workflowId` VARCHAR(45) NULL DEFAULT NULL,
  `operationName` VARCHAR(45) NULL DEFAULT NULL,
  `datasetId` VARCHAR(45) NULL DEFAULT NULL,
  `sourceBucket` VARCHAR(1000) NULL DEFAULT NULL,
  `sourceKey` VARCHAR(1000) NULL DEFAULT NULL,
  `description` VARCHAR(1000) NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;

-- -----------------------------------------------------
-- Table `chamberlain`.`runningJobs`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`runningJobs` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `workflowName` VARCHAR(45) NULL DEFAULT NULL,
  `cardinals` VARCHAR(1000) NULL DEFAULT NULL,
  `datasetId` VARCHAR(45) NULL DEFAULT NULL,
  `operation` VARCHAR(45) NULL DEFAULT NULL,
  `cpuUsage` FLOAT(11) NULL DEFAULT NULL,
  `memoryUsage` FLOAT(11) NULL DEFAULT NULL,
  `runTime` FLOAT(11) NULL DEFAULT NULL,
  `submittedStats` INT NULL DEFAULT 0,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8
COLLATE = utf8_bin;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
