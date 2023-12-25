-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema OJ
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `OJ` ;

-- -----------------------------------------------------
-- Schema OJ
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `OJ` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `OJ` ;

-- -----------------------------------------------------
-- Table `OJ`.`user`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`user` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`user` (
  `userid` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NULL,
  `username` VARCHAR(255) NULL,
  `password` VARCHAR(255) NULL,
  `role` INT NULL,
  `major` VARCHAR(255) NULL,
  `telephone` VARCHAR(255) NULL,
  PRIMARY KEY (`userid`),
  UNIQUE INDEX `userid_UNIQUE` (`userid` ASC) VISIBLE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`course` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`course` (
  `courseid` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `info` VARCHAR(255) NULL,
  `teacherid` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`courseid`),
  INDEX `fk_course_user1_idx` (`teacherid` ASC) VISIBLE,
  CONSTRAINT `fk_course_user1`
    FOREIGN KEY (`teacherid`)
    REFERENCES `OJ`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`homework`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`homework` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`homework` (
  `homeworkid` INT NOT NULL AUTO_INCREMENT,
  `homeworkname` VARCHAR(255) NULL,
  `duedate` DATETIME NULL,
  `courseid` INT NOT NULL COMMENT 'the course homework belong to',
  PRIMARY KEY (`homeworkid`),
  INDEX `fk_homework_course1_idx` (`courseid` ASC) VISIBLE,
  CONSTRAINT `fk_homework_course1`
    FOREIGN KEY (`courseid`)
    REFERENCES `OJ`.`course` (`courseid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`problem`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`problem` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`problem` (
  `problemid` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `problemType` VARCHAR(255) NULL COMMENT '题目类型',
  `content` TEXT NULL,
  `point` DOUBLE NULL,
  `homeworkid` INT NOT NULL COMMENT 'homework belong to',
  `difficult` VARCHAR(255) NULL,
  PRIMARY KEY (`problemid`),
  INDEX `fk_problem_homework_idx` (`homeworkid` ASC) VISIBLE,
  CONSTRAINT `fk_problem_homework`
    FOREIGN KEY (`homeworkid`)
    REFERENCES `OJ`.`homework` (`homeworkid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`solution`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`solution` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`solution` (
  `solutionid` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NULL COMMENT '答案内容',
  `problemid` INT NOT NULL,
  `contributorid` VARCHAR(255) NOT NULL,
  `name` VARCHAR(255) NULL,
  PRIMARY KEY (`solutionid`),
  INDEX `fk_solution_problem1_idx` (`problemid` ASC) VISIBLE,
  INDEX `fk_solution_user1_idx` (`contributorid` ASC) VISIBLE,
  CONSTRAINT `fk_solution_problem1`
    FOREIGN KEY (`problemid`)
    REFERENCES `OJ`.`problem` (`problemid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_solution_user1`
    FOREIGN KEY (`contributorid`)
    REFERENCES `OJ`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`comment`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`comment` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`comment` (
  `commentid` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NULL,
  `createAt` DATETIME NULL,
  `solutionid` INT NOT NULL,
  `contributorid` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`commentid`),
  INDEX `fk_comment_solution1_idx` (`solutionid` ASC) VISIBLE,
  INDEX `fk_comment_user1_idx` (`contributorid` ASC) VISIBLE,
  CONSTRAINT `fk_comment_solution1`
    FOREIGN KEY (`solutionid`)
    REFERENCES `OJ`.`solution` (`solutionid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comment_user1`
    FOREIGN KEY (`contributorid`)
    REFERENCES `OJ`.`user` (`userid`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`stu_course`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`stu_course` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`stu_course` (
  `courseid` INT NOT NULL,
  `userid` VARCHAR(255) NOT NULL,
  INDEX `fk_stu_course_user1_idx` (`userid` ASC) VISIBLE,
  INDEX `fk_stu_course_course1_idx` (`courseid` ASC) VISIBLE,
  PRIMARY KEY (`courseid`, `userid`),
  CONSTRAINT `fk_stu_course_user1`
    FOREIGN KEY (`userid`)
    REFERENCES `OJ`.`user` (`userid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_stu_course_course1`
    FOREIGN KEY (`courseid`)
    REFERENCES `OJ`.`course` (`courseid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`attempt`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`attempt` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`attempt` (
  `problemid` INT NOT NULL,
  `studentid` VARCHAR(255) NOT NULL,
  `point` DOUBLE NULL DEFAULT 0 COMMENT 'the point student get in this problem\n',
  `content` TEXT NULL,
  INDEX `fk_attempt_problem1_idx` (`problemid` ASC) VISIBLE,
  INDEX `fk_attempt_user1_idx` (`studentid` ASC) VISIBLE,
  PRIMARY KEY (`problemid`, `studentid`),
  CONSTRAINT `fk_attempt_problem1`
    FOREIGN KEY (`problemid`)
    REFERENCES `OJ`.`problem` (`problemid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_attempt_user1`
    FOREIGN KEY (`studentid`)
    REFERENCES `OJ`.`user` (`userid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `OJ`.`choice`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `OJ`.`choice` ;

SHOW WARNINGS;
CREATE TABLE IF NOT EXISTS `OJ`.`choice` (
  `problemid` INT NOT NULL,
  `choiceid` INT NOT NULL AUTO_INCREMENT,
  `content` TEXT NULL,
  `label` VARCHAR(45) NULL,
  `iscorrect` TINYINT NULL COMMENT 'zero is false one is true',
  INDEX `fk_choices_problem1_idx` (`problemid` ASC) VISIBLE,
  PRIMARY KEY (`choiceid`),
  CONSTRAINT `fk_choices_problem1`
    FOREIGN KEY (`problemid`)
    REFERENCES `OJ`.`problem` (`problemid`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
