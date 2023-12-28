-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: oj
-- ------------------------------------------------------
-- Server version	8.0.34

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attempt`
--

DROP TABLE IF EXISTS `attempt`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attempt` (
  `problemid` int NOT NULL,
  `studentid` varchar(255) NOT NULL,
  `point` double DEFAULT '0' COMMENT 'the point student get in this problem\n',
  `content` text,
  PRIMARY KEY (`problemid`,`studentid`),
  KEY `fk_attempt_problem1_idx` (`problemid`),
  KEY `fk_attempt_user1_idx` (`studentid`),
  CONSTRAINT `fk_attempt_problem1` FOREIGN KEY (`problemid`) REFERENCES `problem` (`problemid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_attempt_user1` FOREIGN KEY (`studentid`) REFERENCES `user` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attempt`
--

LOCK TABLES `attempt` WRITE;
/*!40000 ALTER TABLE `attempt` DISABLE KEYS */;
INSERT INTO `attempt` VALUES (2,'123',0,'try to solve the problem');
/*!40000 ALTER TABLE `attempt` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `choice`
--

DROP TABLE IF EXISTS `choice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `choice` (
  `problemid` int NOT NULL,
  `choiceid` int NOT NULL AUTO_INCREMENT,
  `content` text,
  `label` varchar(45) DEFAULT NULL,
  `iscorrect` tinyint DEFAULT NULL COMMENT 'zero is false one is true',
  PRIMARY KEY (`choiceid`),
  KEY `fk_choices_problem1_idx` (`problemid`),
  CONSTRAINT `fk_choices_problem1` FOREIGN KEY (`problemid`) REFERENCES `problem` (`problemid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `choice`
--

LOCK TABLES `choice` WRITE;
/*!40000 ALTER TABLE `choice` DISABLE KEYS */;
INSERT INTO `choice` VALUES (2,1,'choice_1','A',1),(2,2,'choice_2','B',0),(3,3,'this is choice A','A',1),(3,4,'this is choice B','B',0);
/*!40000 ALTER TABLE `choice` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comment`
--

DROP TABLE IF EXISTS `comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comment` (
  `commentid` int NOT NULL AUTO_INCREMENT,
  `content` text,
  `createAt` datetime DEFAULT NULL,
  `solutionid` int NOT NULL,
  `contributorid` varchar(255) NOT NULL,
  PRIMARY KEY (`commentid`),
  KEY `fk_comment_solution1_idx` (`solutionid`),
  KEY `fk_comment_user1_idx` (`contributorid`),
  CONSTRAINT `fk_comment_solution1` FOREIGN KEY (`solutionid`) REFERENCES `solution` (`solutionid`),
  CONSTRAINT `fk_comment_user1` FOREIGN KEY (`contributorid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comment`
--

LOCK TABLES `comment` WRITE;
/*!40000 ALTER TABLE `comment` DISABLE KEYS */;
INSERT INTO `comment` VALUES (4,'excellent','2023-12-28 01:03:55',2,'1234'),(7,'123','2023-12-28 13:10:55',2,'123');
/*!40000 ALTER TABLE `comment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `course`
--

DROP TABLE IF EXISTS `course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `course` (
  `courseid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `info` varchar(255) DEFAULT NULL,
  `teacherid` varchar(255) NOT NULL,
  PRIMARY KEY (`courseid`),
  KEY `fk_course_user1_idx` (`teacherid`),
  CONSTRAINT `fk_course_user1` FOREIGN KEY (`teacherid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course`
--

LOCK TABLES `course` WRITE;
/*!40000 ALTER TABLE `course` DISABLE KEYS */;
INSERT INTO `course` VALUES (1,'course','string','1234'),(3,'new_course','string','1234');
/*!40000 ALTER TABLE `course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `homework`
--

DROP TABLE IF EXISTS `homework`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `homework` (
  `homeworkid` int NOT NULL AUTO_INCREMENT,
  `homeworkname` varchar(255) DEFAULT NULL,
  `duedate` datetime DEFAULT NULL,
  `courseid` int NOT NULL COMMENT 'the course homework belong to',
  PRIMARY KEY (`homeworkid`),
  KEY `fk_homework_course1_idx` (`courseid`),
  CONSTRAINT `fk_homework_course1` FOREIGN KEY (`courseid`) REFERENCES `course` (`courseid`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `homework`
--

LOCK TABLES `homework` WRITE;
/*!40000 ALTER TABLE `homework` DISABLE KEYS */;
INSERT INTO `homework` VALUES (1,'homework','2023-12-22 13:57:26',1);
/*!40000 ALTER TABLE `homework` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `problem`
--

DROP TABLE IF EXISTS `problem`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `problem` (
  `problemid` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `problemType` varchar(255) DEFAULT NULL COMMENT '题目类型',
  `content` text,
  `point` double DEFAULT NULL,
  `homeworkid` int NOT NULL COMMENT 'homework belong to',
  `difficult` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`problemid`),
  KEY `fk_problem_homework_idx` (`homeworkid`),
  CONSTRAINT `fk_problem_homework` FOREIGN KEY (`homeworkid`) REFERENCES `homework` (`homeworkid`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `problem`
--

LOCK TABLES `problem` WRITE;
/*!40000 ALTER TABLE `problem` DISABLE KEYS */;
INSERT INTO `problem` VALUES (2,'problem_name','blank','this is description of problem',10,1,'hard'),(3,'problem3','choice','string',0,1,'hard');
/*!40000 ALTER TABLE `problem` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `solution`
--

DROP TABLE IF EXISTS `solution`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `solution` (
  `solutionid` int NOT NULL AUTO_INCREMENT,
  `content` text COMMENT '答案内容',
  `problemid` int NOT NULL,
  `contributorid` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`solutionid`),
  KEY `fk_solution_problem1_idx` (`problemid`),
  KEY `fk_solution_user1_idx` (`contributorid`),
  CONSTRAINT `fk_solution_problem1` FOREIGN KEY (`problemid`) REFERENCES `problem` (`problemid`),
  CONSTRAINT `fk_solution_user1` FOREIGN KEY (`contributorid`) REFERENCES `user` (`userid`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `solution`
--

LOCK TABLES `solution` WRITE;
/*!40000 ALTER TABLE `solution` DISABLE KEYS */;
INSERT INTO `solution` VALUES (2,'content of solution',2,'1234','solution_name');
/*!40000 ALTER TABLE `solution` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `stu_course`
--

DROP TABLE IF EXISTS `stu_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `stu_course` (
  `courseid` int NOT NULL,
  `userid` varchar(255) NOT NULL,
  PRIMARY KEY (`courseid`,`userid`),
  KEY `fk_stu_course_user1_idx` (`userid`),
  KEY `fk_stu_course_course1_idx` (`courseid`),
  CONSTRAINT `fk_stu_course_course1` FOREIGN KEY (`courseid`) REFERENCES `course` (`courseid`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_stu_course_user1` FOREIGN KEY (`userid`) REFERENCES `user` (`userid`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `stu_course`
--

LOCK TABLES `stu_course` WRITE;
/*!40000 ALTER TABLE `stu_course` DISABLE KEYS */;
INSERT INTO `stu_course` VALUES (1,'123');
/*!40000 ALTER TABLE `stu_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `userid` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `role` int DEFAULT NULL,
  `major` varchar(255) DEFAULT NULL,
  `telephone` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`userid`),
  UNIQUE KEY `userid_UNIQUE` (`userid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('123','123@qq.com','student','$2b$12$XxOFcfyZbMlhgv0kmkef1OjlhC8CWhm/aAW0MBnkLzNQxXMeykjhK',0,'string','string'),('1234','1234@qq.com','teacher','$2b$12$LSEV/rZCRFu7efPy3c6/b.zpcYGbCpFKKEoIfdewvxznefVQ6cvKm',1,'string','string');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-28 23:43:25
