-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema chamberlain
-- -----------------------------------------------------
-- 
-- 

-- -----------------------------------------------------
-- Schema chamberlain
--
-- 
-- 
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `chamberlain` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `chamberlain` ;

-- -----------------------------------------------------
-- Table `chamberlain`.`datasets`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`datasets` (
  `datasetId` VARCHAR(45) NOT NULL,
  `datasetschema` VARCHAR(1000) NULL,
  PRIMARY KEY (`datasetId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chamberlain`.`workflows`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`workflows` (
  `workflowId` VARCHAR(45) NOT NULL,
  `operationName` VARCHAR(45) NULL,
  PRIMARY KEY (`workflowId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chamberlain`.`cardinals`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`cardinals` (
  `cardinalId` VARCHAR(45) NOT NULL,
  `cardinalIp` VARCHAR(1000) NULL,
  PRIMARY KEY (`cardinalId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chamberlain`.`storageRelationships`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`storageRelationships` (
  `storageRelationshipId` VARCHAR(45) NOT NULL,
  `datasetId` VARCHAR(45) NULL,
  `cardinalId1` VARCHAR(45) NULL,
  `cardinalId2` VARCHAR(45) NULL,
  `cardinalId3` VARCHAR(45) NULL,
  PRIMARY KEY (`storageRelationshipId`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `chamberlain`.`workflowRelationships`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `chamberlain`.`workflowRelationships` (
  `workflowRelationshipId` VARCHAR(45) NOT NULL,
  `datasetId` VARCHAR(45) NULL,
  `workflowId` VARCHAR(45) NULL,
  PRIMARY KEY (`workflowRelationshipId`))
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
