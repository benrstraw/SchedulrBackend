-- MariaDB dump 10.17  Distrib 10.4.8-MariaDB, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: schedulr
-- ------------------------------------------------------
-- Server version	10.1.41-MariaDB-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `course_reqs`
--

DROP TABLE IF EXISTS `course_reqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `course_reqs` (
  `course_id` int(11) NOT NULL,
  `prereq_id` int(11) NOT NULL,
  `orgroup` smallint(6) DEFAULT NULL,
  PRIMARY KEY (`prereq_id`,`course_id`),
  KEY `class_deps_FK` (`course_id`),
  CONSTRAINT `class_deps_FK` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `class_deps_FK_1` FOREIGN KEY (`prereq_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `course_reqs`
--

LOCK TABLES `course_reqs` WRITE;
/*!40000 ALTER TABLE `course_reqs` DISABLE KEYS */;
INSERT INTO `course_reqs` VALUES (2,1,NULL),(64,2,NULL),(65,2,NULL),(29,10,NULL),(30,10,NULL),(38,10,NULL),(75,11,NULL),(76,11,NULL),(78,11,NULL),(81,11,NULL),(60,21,NULL),(59,23,NULL),(10,25,NULL),(18,27,NULL),(20,27,NULL),(25,27,NULL),(28,27,NULL),(39,27,NULL),(10,28,NULL),(20,28,NULL),(33,29,NULL),(31,30,NULL),(36,30,NULL),(37,30,NULL),(47,30,NULL),(57,30,NULL),(63,30,NULL),(74,30,NULL),(32,31,NULL),(44,31,NULL),(78,31,NULL),(45,32,NULL),(44,33,NULL),(47,33,NULL),(35,34,NULL),(51,36,NULL),(39,37,1),(42,37,1),(48,37,NULL),(61,37,1),(40,38,NULL),(40,39,NULL),(62,39,NULL),(43,40,NULL),(52,40,NULL),(63,40,NULL),(66,40,NULL),(68,40,NULL),(69,40,NULL),(70,40,NULL),(71,40,NULL),(72,40,NULL),(73,40,NULL),(39,41,1),(42,41,1),(53,41,NULL),(61,41,1),(74,41,NULL),(40,42,NULL),(45,44,NULL),(46,45,NULL),(54,46,NULL),(55,46,NULL),(48,47,NULL),(49,48,NULL),(50,48,1),(51,48,NULL),(54,49,NULL),(55,49,NULL),(50,53,1),(62,53,NULL),(56,55,NULL),(58,57,NULL),(66,62,NULL),(67,66,NULL),(66,70,NULL),(67,72,NULL),(77,76,NULL),(80,76,NULL),(82,76,NULL),(83,76,NULL),(79,78,NULL);
/*!40000 ALTER TABLE `course_reqs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `courses`
--

DROP TABLE IF EXISTS `courses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `courses` (
  `course_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `code` varchar(20) DEFAULT NULL,
  `hours` int(11) DEFAULT NULL,
  `catalog` varchar(10) DEFAULT NULL,
  `description` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`course_id`)
) ENGINE=InnoDB AUTO_INCREMENT=84 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `courses`
--

LOCK TABLES `courses` WRITE;
/*!40000 ALTER TABLE `courses` DISABLE KEYS */;
INSERT INTO `courses` VALUES (1,'Composition I','ENC 1101',3,'2018-19','Expository writing with emphasis on effective communication and critical thinking. Emphasizing the writing process writing topics are based on selected readings and on student experiences. The “NC” grading policy applies to this course'),(2,'Composition II','ENC 1102',3,'2018-19','Focus on extensive research in analytical and argumentative writing based on a variety of readings from the humanities. Emphasis on developing critical thinking and diversity of perspective. The “NC” grading policy applies to this course.'),(3,'Fundamentals of Oral Communication','SPC 1608',3,'2018-19','Communication theory and its application to preparing and delivering public speeches'),(4,'Fundamentals of Technical Presentations','SPC 1603C',3,'2018-19','Communication theory and its application to preparing and delivering technical information in public speaking situations'),(5,'Introduction to Communication','COM 1000',3,'2018-19','Survey course introducing students to theory, research, and practical principles associated with human communication in interpersonal, public, and professional contexts'),(6,'Encountering the Humanities','HUM 2020',3,'2018-19','Learn about people and history but in art'),(7,'Enjoyment of Music','MUL 2010',3,'2018-19','Designed to develop an understanding of musical principles'),(8,'Theatre Survey','THE 2000',3,'2018-19','Overview of the art and craft of the'),(9,'Introduction to Philosophy','PHI 2010',3,'2018-19','Inquiry into the'),(10,'Calculus with Analytic Geometry I','MAC 2311C',4,'2018-19','Derivatives!'),(11,'Statistical Methods I','STA 2023',3,'2018-19','Either fail or get 100, no inbetween option allowed'),(12,'General Anthropology','ANT 2000',3,'2018-19','An introductory survey'),(13,'General Psychology','PSY 2012',3,'2018-19','Diagnose yourself with a rare mental illness'),(14,'Introduction to Sociology','SYG 2000',3,'2018-19','Learn about people!'),(15,'U.S. History: 1877-Present','AMH 2020',3,'2018-19','Survey of U.S. history from 1877 to present'),(16,'Principles of Macroeconomics','ECO 2013',3,'2018-19','Supply and demand!'),(17,'American National Government','POS 2041',3,'2018-19','Learn about what a congress is'),(18,'Astronomy','AST 2002',3,'2018-19','Descriptive survey of solar system, galaxies and universe;'),(19,'Concepts of Physics','PHY 2020',3,'2018-19','Nothing'),(20,'College Physics I','PHY 2053C',4,'2018-19','Wrong move for physics'),(21,'Chemistry Fundamentals I','CHM 2045C',4,'2018-19','Atomic structure, periodicity, chemical'),(22,'Biological Principles','BSC 1005',3,'2018-19','A study of various biological'),(23,'Biology I','BSC 2010C',4,'2018-19','Cellular and chemical basis of life, genetics, and'),(24,'Introduction to Environmental Science','EVR 1001',3,'2018-19','If you want an easy science gen ed this will do and you can also find your fav animal'),(25,'Pre-Calculus Algebra','MAC 1140C',3,'2018-19','Who even knows.. Matrices?'),(26,'Intermediate Algebra','MAT 1033C',3,'2018-19','Nothing'),(27,'College Algebra','MAC 1105C',3,'2018-19','Find x and slopes and other things you can do in the calculator'),(28,'College Trigonometry','MAC 1114C',3,'2018-19','Triangles!'),(29,'General Physics Using Calculus I','PHY 2048C',3,'2018-19','Speeds and kinematics'),(30,'Calculus with Analytic Geometry II','MAC 2312',4,'2018-19','Integrals!'),(31,'Calculus with Analytic Geometry III','MAC 2313',4,'2018-19','3D derivatives!'),(32,'Ordinary Differential Equations I','MAP 2302',3,'2018-19','Break apart that Dy/Dx that they told you not to break apart'),(33,'General Physics Using Calculus II','PHY 2049C',4,'2018-19','Optics and magnets and fields ohmy'),(34,'Introduction to the Engineering Profession','EGS 1006C',1,'2018-19','Baby\'s first class. What is excel'),(35,'Engineering Concepts and Methods','EGN 1007C',1,'2018-19','Great Naval Race!'),(36,'Probability and Statistics for Engineers','STA 3032',3,'2018-19','Big boi stats only for big boi engineers'),(37,'Engineering Analysis and Computation','EGN 3211',3,'2018-19','Engineers version of intro to C'),(38,'Introduction to Discrete Structures','COT 3100C',3,'2018-19','CS weed out class- basic probability and stuff'),(39,'Computer Science I','COP 3502C',3,'2018-19','Data Structures '),(40,'Computer Science II','COP 3503C',3,'2018-19','Algorithms'),(41,'Introduction to Programming with C','COP 3223C',3,'2018-19','Programming in C including arrays, pointer manipulation'),(42,'Object Oriented Programming','COP 3330',3,'2018-19','Object oriented programming concepts (classes, objects,'),(43,'Processes for Object-Oriented Software Development','COP 4331C',3,'2018-19','Learn about Australian demo gods, the wonderful animated classic: Robots, and fishing'),(44,'Electrical Networks','EEL 3004C',3,'2018-19','How to analyze circuits'),(45,'Networks and Systems','EEL 3123C',3,'2018-19','How to analyze harder circuits'),(46,'Electronics I','EEE 3307C',4,'2018-19','All about Transistors'),(47,'Digital Systems','EEE 3342C',3,'2018-19','Boolean logics and gates and sums'),(48,'Computer Organization','EEL 3801C',4,'2018-19','Memory layout and caches'),(49,'Embedded Systems','EEL 4742C',3,'2018-19','Microcontrollers'),(50,'Computer Architecture','EEL 4768',3,'2018-19','CDA pt. 2'),(51,'Computer Communication Networks','EEL 4781',3,'2018-19','How do computers talk to each other'),(52,'Operating Systems','COP 4600',3,'2018-19','Garbage class- avoid'),(53,'Computer Logic and Organization','CDA 3103C',3,'2018-19','Logic design,'),(54,'Junior Design','EEL 3926L',1,'2018-19','Learn how to take Senior Design'),(55,'Senior Design I','EEL 4914',3,'2018-19','big boi project time'),(56,'Senior Design II','EEL 4915L',3,'2018-19','big boi project time pt 2'),(57,'Matrix and Linear Algebra','MAS 3105',4,'2018-19','Matrices!'),(58,'Linear Algebra','MAS 3106',4,'2018-19','Algebra in a line- theoretical matrix bullsh*t'),(59,'Biology II','BSC 2011C',4,'2018-19','Organismal anatomy and physiology as it relates to'),(60,'Chemistry Fundamentals II','CHM 2046',3,'2018-19','Intermolecular forces, solutions'),(61,'Security in Computing','CIS 3360',3,'2018-19','Security theory.'),(62,'Systems Software','COP 3402',3,'2018-19','Build a compiler'),(63,'Discrete Structures II','COT 4210',3,'2018-19','Big boi Discrete, not related to small boi discrete '),(64,'Writing for the Technical Professional','ENC 3241',3,'2018-19','Writing for businessmen and resumes'),(65,'Professional Writing','ENC 3250',3,'2018-19','Writing for businessmen and resume'),(66,'Senior Design I','COP 4934',3,'2018-19','Build a big boi project'),(67,'Senior Design II','COP 4935',3,'2018-19','Build a big boi project part 2'),(68,'CS Tech Elective 1','COP 5001',3,'2018-19','Take any one of the tech electives found on the CS major catalog or sent to your email every semester by Jenny'),(69,'CS Tech Elective 2','COP 5002',3,'2018-19','Take any one of the tech electives found on the CS major catalog or sent to your email every semester by Jenny'),(70,'CS Tech Elective 3','COP 5003',3,'2018-19','Take any one of the tech electives found on the CS major catalog or sent to your email every semester by Jenny'),(71,'CS Tech Elective 4','COP 5004',3,'2018-19','Take any one of the tech electives found on the CS major catalog or sent to your email every semester by Jenny'),(72,'CS Tech Elective 5','COP 5005',3,'2018-19','Take any one of the tech electives found on the CS major catalog or sent to your email every semester by Jenny'),(73,'CS Tech Elective 6','COP 5006',3,'2018-19','Take any one of the tech electives found on the CS major catalog or sent to your email every semester by Jenny'),(74,'Numerical Calculus','COT 4500',3,'2018-19','Program Calculus'),(75,'Computer Processing of Statistical Data','STA 4102',3,'2018-19','SAS R and Python'),(76,'Statistical Methods 2','STA 4163',3,'2018-19','Learn Stats Again!'),(77,'Statistical Methods 3','STA 4164',3,'2018-19','Learn Stats again pt. 2'),(78,'Statistical Theory 1','STA 4321',3,'2018-19','Distributions and probabilities'),(79,'Statistical Theory 2','STA 4322',3,'2018-19','Central Limit Theorem and even more distirbutions'),(80,'Biostatistical Methods','STA 4173',3,'2018-19','Learn stats again but with bio examples!'),(81,'Sample Survey Methods','STA 4222',3,'2018-19','Make sample sizes and learn how to sample people'),(82,'Categorical Data Analysis','STA 4504',3,'2018-19','Best class at UCF actually learn stats for the first time'),(83,'Applied Time Series','STA 4852',3,'2018-19','Scary class learn forecasting and predicting stuff with ARIMA');
/*!40000 ALTER TABLE `courses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prog_reqs`
--

DROP TABLE IF EXISTS `prog_reqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `prog_reqs` (
  `prog_id` int(11) NOT NULL,
  `rs_id` int(11) NOT NULL,
  PRIMARY KEY (`prog_id`,`rs_id`),
  KEY `prog_reqs_FK_1` (`rs_id`),
  CONSTRAINT `prog_reqs_FK` FOREIGN KEY (`prog_id`) REFERENCES `programs` (`prog_id`),
  CONSTRAINT `prog_reqs_FK_1` FOREIGN KEY (`rs_id`) REFERENCES `reqsets` (`rs_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prog_reqs`
--

LOCK TABLES `prog_reqs` WRITE;
/*!40000 ALTER TABLE `prog_reqs` DISABLE KEYS */;
INSERT INTO `prog_reqs` VALUES (1,1),(1,2),(1,3),(1,4),(1,5),(1,6),(1,7),(1,8),(1,9),(1,10),(2,11),(2,12),(3,13),(3,14),(3,15),(3,16),(3,17),(4,18);
/*!40000 ALTER TABLE `prog_reqs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `programs`
--

DROP TABLE IF EXISTS `programs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `programs` (
  `prog_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `catalog` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`prog_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `programs`
--

LOCK TABLES `programs` WRITE;
/*!40000 ALTER TABLE `programs` DISABLE KEYS */;
INSERT INTO `programs` VALUES (1,'General Education Program','2018-19'),(2,'Computer Engineering, Comprehensive Track (B.S.Cp.E.)','2018-19'),(3,'Computer Science (B.S.)','2018-19'),(4,'Statistics (B.S)','2018-19');
/*!40000 ALTER TABLE `programs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reqsets`
--

DROP TABLE IF EXISTS `reqsets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `reqsets` (
  `rs_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `catalog` varchar(10) DEFAULT NULL,
  `optionals` smallint(5) unsigned DEFAULT NULL,
  PRIMARY KEY (`rs_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reqsets`
--

LOCK TABLES `reqsets` WRITE;
/*!40000 ALTER TABLE `reqsets` DISABLE KEYS */;
INSERT INTO `reqsets` VALUES (1,'GEP - Communication - Areas 1 & 2','2018-19',NULL),(2,'GEP - Communication - Area 3','2018-19',3),(3,'GEP - Cultural & Historical - Area 1','2018-19',NULL),(4,'GEP - Cultural & Historical - Areas 2 & 3','2018-19',6),(5,'GEP - Mathematical - Area 1','2018-19',3),(6,'GEP - Mathematical - Area 2','2018-19',3),(7,'GEP - Social - Area 1','2018-19',3),(8,'GEP - Social - Area 2','2018-19',3),(9,'GEP - Science - Area 1','2018-19',3),(10,'GEP - Science - Area 2','2018-19',3),(11,'Engineering CPP','2018-19',NULL),(12,'Computer Engineering, Comprehensive Track - Core','2018-19',NULL),(13,'Computer Science - Core','2018-19',NULL),(14,'Computer Science - Science Basics','2018-19',6),(15,'Computer Science - Math Basics','2018-19',6),(16,'Computer Science - Writing Basics','2018-19',3),(17,'Computer Science - Tech Electives','2018-19',18),(18,'Statistics','2018-19',NULL);
/*!40000 ALTER TABLE `reqsets` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rs_reqs`
--

DROP TABLE IF EXISTS `rs_reqs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rs_reqs` (
  `rs_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  PRIMARY KEY (`rs_id`,`course_id`),
  KEY `requirements_FK_1` (`course_id`),
  CONSTRAINT `requirements_FK` FOREIGN KEY (`rs_id`) REFERENCES `reqsets` (`rs_id`),
  CONSTRAINT `requirements_FK_1` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rs_reqs`
--

LOCK TABLES `rs_reqs` WRITE;
/*!40000 ALTER TABLE `rs_reqs` DISABLE KEYS */;
INSERT INTO `rs_reqs` VALUES (1,1),(1,2),(2,3),(2,4),(2,5),(3,6),(4,7),(4,8),(4,9),(5,10),(5,27),(6,11),(6,38),(6,39),(7,12),(7,13),(7,14),(8,15),(8,16),(8,17),(9,21),(9,29),(10,23),(11,10),(11,21),(11,29),(11,30),(11,31),(11,32),(11,33),(11,34),(11,35),(11,36),(12,37),(12,38),(12,39),(12,40),(12,42),(12,43),(12,44),(12,45),(12,46),(12,47),(12,48),(12,49),(12,50),(12,51),(12,52),(12,54),(12,55),(12,56),(13,10),(13,11),(13,29),(13,30),(13,33),(13,38),(13,39),(13,40),(13,41),(13,42),(13,43),(13,53),(13,61),(13,62),(13,63),(13,66),(13,67),(14,21),(14,23),(14,59),(14,60),(15,31),(15,32),(15,57),(15,58),(16,64),(16,65),(17,68),(17,69),(17,70),(17,71),(17,72),(17,73),(18,10),(18,11),(18,29),(18,30),(18,31),(18,33),(18,38),(18,39),(18,41),(18,42),(18,57),(18,61),(18,74),(18,75),(18,76),(18,77),(18,78),(18,79),(18,80),(18,81),(18,82),(18,83);
/*!40000 ALTER TABLE `rs_reqs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_progs`
--

DROP TABLE IF EXISTS `user_progs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_progs` (
  `user_id` int(11) NOT NULL,
  `prog_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`,`prog_id`),
  KEY `user_progs_FK` (`prog_id`),
  CONSTRAINT `user_progs_FK` FOREIGN KEY (`prog_id`) REFERENCES `programs` (`prog_id`),
  CONSTRAINT `user_reqs_FK` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_progs`
--

LOCK TABLES `user_progs` WRITE;
/*!40000 ALTER TABLE `user_progs` DISABLE KEYS */;
INSERT INTO `user_progs` VALUES (1,1),(1,2),(2,1),(2,2),(3,1),(3,3),(4,1),(4,3),(5,1),(5,3),(6,1),(6,3),(6,4),(7,1),(7,3),(8,1),(8,3),(9,3),(12,1),(12,4),(13,1),(13,3),(15,1),(15,4),(16,1),(16,4),(17,1),(17,4),(18,1),(18,4);
/*!40000 ALTER TABLE `user_progs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_taken`
--

DROP TABLE IF EXISTS `user_taken`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_taken` (
  `user_id` int(11) NOT NULL,
  `course_id` int(11) NOT NULL,
  `semester` enum('SPRING','SUMMER','FALL') NOT NULL,
  `year` smallint(5) unsigned NOT NULL,
  `status` enum('COMPLETE','INPROGRESS','PLANNED') DEFAULT NULL,
  `grade` enum('A','A-','B+','B','B-','C+','C','C-','D+','D','D-','F') DEFAULT NULL,
  PRIMARY KEY (`user_id`,`course_id`,`semester`,`year`),
  KEY `user_taken_FK` (`course_id`),
  CONSTRAINT `user_taken_FK` FOREIGN KEY (`course_id`) REFERENCES `courses` (`course_id`),
  CONSTRAINT `user_taken_FK_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_taken`
--

LOCK TABLES `user_taken` WRITE;
/*!40000 ALTER TABLE `user_taken` DISABLE KEYS */;
INSERT INTO `user_taken` VALUES (1,1,'SPRING',2016,'COMPLETE','A'),(1,2,'FALL',2016,'COMPLETE','A'),(1,4,'SPRING',2017,'COMPLETE','A'),(1,6,'SPRING',2016,'COMPLETE','A'),(1,7,'SPRING',2017,'COMPLETE','A-'),(1,8,'SPRING',2016,'COMPLETE','A'),(1,10,'SUMMER',2017,'COMPLETE','B+'),(1,13,'FALL',2016,'COMPLETE','A'),(1,15,'SPRING',2016,'COMPLETE','A'),(1,21,'SPRING',2017,'COMPLETE','B+'),(1,22,'FALL',2017,'COMPLETE','C+'),(1,25,'SPRING',2017,'COMPLETE','C'),(1,27,'FALL',2016,'COMPLETE','A'),(1,28,'SPRING',2017,'COMPLETE','B'),(1,29,'FALL',2017,'COMPLETE','C+'),(1,30,'FALL',2017,'COMPLETE','C+'),(1,31,'SPRING',2018,'COMPLETE','B'),(1,32,'FALL',2018,'COMPLETE','C'),(1,33,'SPRING',2018,'COMPLETE','C'),(1,34,'FALL',2016,'COMPLETE','A'),(1,35,'SPRING',2017,'COMPLETE','A'),(1,36,'SPRING',2018,'COMPLETE','C'),(1,37,'SPRING',2018,'COMPLETE','A-'),(1,38,'FALL',2017,'COMPLETE','B'),(1,39,'FALL',2018,'COMPLETE','A'),(1,42,'FALL',2018,'COMPLETE','A'),(1,44,'FALL',2018,'COMPLETE','B'),(2,1,'SPRING',2016,'COMPLETE','A'),(2,2,'FALL',2016,'COMPLETE','A'),(2,4,'SPRING',2017,'COMPLETE','A'),(2,6,'SPRING',2016,'COMPLETE','A'),(2,8,'SPRING',2016,'COMPLETE','A'),(2,10,'SUMMER',2017,'COMPLETE','B+'),(2,13,'FALL',2016,'COMPLETE','A'),(2,15,'SPRING',2016,'COMPLETE','A'),(2,21,'SPRING',2017,'COMPLETE','B+'),(2,22,'FALL',2017,'COMPLETE','C+'),(2,25,'SPRING',2017,'COMPLETE','C'),(2,26,'SPRING',2019,'COMPLETE','B+'),(2,27,'FALL',2016,'COMPLETE','A'),(2,28,'SPRING',2017,'COMPLETE','B'),(2,29,'FALL',2017,'COMPLETE','C+'),(2,30,'FALL',2017,'COMPLETE','C+'),(2,31,'SPRING',2018,'COMPLETE','B'),(2,32,'FALL',2018,'COMPLETE','C'),(2,33,'SPRING',2018,'COMPLETE','C'),(2,34,'FALL',2016,'COMPLETE','A'),(2,35,'SPRING',2017,'COMPLETE','A'),(2,36,'SPRING',2018,'COMPLETE','C'),(2,37,'SPRING',2018,'COMPLETE','A-'),(2,38,'FALL',2017,'COMPLETE','B'),(2,39,'FALL',2018,'COMPLETE','A'),(2,40,'SPRING',2019,'COMPLETE','B+'),(2,41,'SPRING',2019,'COMPLETE','B+'),(2,42,'FALL',2018,'COMPLETE','A'),(2,44,'FALL',2018,'COMPLETE','B'),(2,53,'SPRING',2019,'COMPLETE','B+'),(3,4,'SPRING',2019,'COMPLETE','B+'),(4,1,'SPRING',2019,'COMPLETE','B+'),(4,3,'SPRING',2019,'COMPLETE','A'),(5,23,'SPRING',2019,'COMPLETE','B+'),(5,41,'SPRING',2019,'COMPLETE','B+'),(6,1,'SPRING',2019,'COMPLETE','B+'),(6,2,'SPRING',2019,'COMPLETE','B+'),(6,3,'SPRING',2019,'COMPLETE','B+'),(6,6,'SPRING',2019,'COMPLETE','B+'),(6,7,'SPRING',2019,'COMPLETE','B+'),(6,10,'SPRING',2019,'COMPLETE','B+'),(6,11,'SPRING',2019,'COMPLETE','B+'),(6,16,'SPRING',2019,'COMPLETE','B+'),(6,29,'SPRING',2019,'COMPLETE','B+'),(6,30,'SPRING',2019,'COMPLETE','B+'),(6,38,'SPRING',2019,'COMPLETE','B+'),(6,41,'SPRING',2019,'COMPLETE','B+'),(6,42,'SPRING',2019,'COMPLETE','B+'),(6,64,'SPRING',2019,'COMPLETE','B+'),(6,76,'SPRING',2019,'COMPLETE','B+'),(6,82,'SPRING',2019,'COMPLETE','B+'),(9,10,'SPRING',2019,'COMPLETE','B+'),(9,23,'SPRING',2019,'COMPLETE','B+'),(9,26,'SPRING',2019,'COMPLETE','B+'),(9,27,'SPRING',2019,'COMPLETE','B+'),(9,28,'SPRING',2019,'COMPLETE','B+'),(9,29,'SPRING',2019,'COMPLETE','B+'),(9,30,'SPRING',2019,'COMPLETE','B+'),(9,32,'SPRING',2019,'COMPLETE','B+'),(12,1,'SPRING',2019,'COMPLETE','B+'),(12,27,'SPRING',2019,'COMPLETE','B+'),(13,1,'SPRING',2019,'COMPLETE','B+'),(13,2,'SPRING',2019,'COMPLETE','B+'),(13,4,'SPRING',2019,'COMPLETE','B+'),(13,6,'SPRING',2019,'COMPLETE','B+'),(13,8,'SPRING',2019,'COMPLETE','B+'),(13,10,'SPRING',2019,'COMPLETE','B+'),(13,13,'SPRING',2019,'COMPLETE','B+'),(13,15,'SPRING',2019,'COMPLETE','B+'),(13,21,'SPRING',2019,'COMPLETE','B+'),(13,22,'SPRING',2019,'COMPLETE','B+'),(13,25,'SPRING',2019,'COMPLETE','B+'),(13,26,'SPRING',2019,'COMPLETE','B+'),(13,27,'SPRING',2019,'COMPLETE','B+'),(13,28,'SPRING',2019,'COMPLETE','B+'),(13,29,'SPRING',2019,'COMPLETE','B+'),(13,30,'SPRING',2019,'COMPLETE','B+'),(13,31,'SPRING',2019,'COMPLETE','B+'),(13,32,'SPRING',2019,'COMPLETE','B+'),(13,33,'SPRING',2019,'COMPLETE','B+'),(13,34,'SPRING',2019,'COMPLETE','B+'),(13,35,'SPRING',2019,'COMPLETE','B+'),(13,36,'SPRING',2019,'COMPLETE','B+'),(13,37,'SPRING',2019,'COMPLETE','B+'),(13,38,'SPRING',2019,'COMPLETE','B+'),(13,39,'SPRING',2019,'COMPLETE','B+'),(13,40,'SPRING',2019,'COMPLETE','B+'),(13,41,'SPRING',2019,'COMPLETE','B+'),(13,42,'SPRING',2019,'COMPLETE','B+'),(13,44,'SPRING',2019,'COMPLETE','B+'),(13,53,'SPRING',2019,'COMPLETE','B+'),(15,1,'SPRING',2019,'COMPLETE','B+'),(15,27,'SPRING',2019,'COMPLETE','B+'),(16,1,'SPRING',2019,'COMPLETE','B+'),(16,27,'SPRING',2019,'COMPLETE','B+'),(17,1,'SPRING',2019,'COMPLETE','B+'),(17,27,'SPRING',2019,'COMPLETE','B+'),(18,1,'SPRING',2019,'COMPLETE','B+'),(18,27,'SPRING',2019,'COMPLETE','B+');
/*!40000 ALTER TABLE `user_taken` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `password` char(128) DEFAULT NULL,
  `admin` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Ben Straw','benrstraw@gmail.com','$2b$12$OuR0YOKKsxXnuiEVImPi3.sS142pDm7ERpWMD/mrjw/kPYgnSaEDy',0),(2,'Test McTester','test@demo.org','$2b$12$a0XyohI8i6/ApFUdcTSUiek9FgaVpRkIduo08Z4D2L6gYefXlUsdy',0),(3,'Garrett Hollar','ghollar99@gmail.com','$2b$12$5v.feFknnQ12PKxX6WOE8eTqOs.Qdq/GnKvRWhmBHbvZ2xPH6RLM6',0),(4,'Test2 McTest','test2@demo.org','$2b$12$/fkP1K6Vp/J7UUpcJFqj5uqdsLz2ryN3pJ6gtEm4fO7ryy0G102EW',0),(5,'Joshua','josh@test.com','$2b$12$DvZa3j9/efMqSn2hhgRaU.jFSJPk11hpx6zTVJVTCTIsbL8OeVPa6',0),(6,'tara','tara@tara.com','$2b$12$q88fZMSqIagC0vb337ZvOOwvUHDAbVC6KpZ5VUD/.8z6AvRf/1Uc.',0),(7,'Garrett Hollar','hollargarrett@gmail.com','$2b$12$0kW9o8Xk5ihWmhP6Uo46J.DVrbJ1jACmtuoiEnSP3tBpexKQXQiVe',0),(8,'New McTest','new@demo.org','$2b$12$NZ/HidOAja3DDKoJg6a7xu.QlhNppnUg6KxQ5rBN7GwFz8SS2/dqa',0),(9,'Brian Smith','brian@brian.brian','$2b$12$PC1.Bf91vUKHMGgPboEeneWGSfj6.dCvTULeiM3kZDZy8/XfHHYdO',0),(10,'Test User','hollarg@gmail.com','$2b$12$bWbcKDC19dLTL7mjre7.o.UglAivB6i/190PA6OgNaCL7x.WSD3gC',0),(11,'Garrett','ghollar@gmail.com','$2b$12$JhUYWiCZR58K09WZJK4mK.yV7ZHnygfpIYji.PWzGmn94mD6ALJ.G',0),(12,'Test','testytest@test.test','$2b$12$oht/xSZE.uOlr4klddDg0e2EbMUdJMKpdTsQPZFaWdL96P6HjivKu',0),(13,'Official Test','testaccount@test.com','$2b$12$PsVqiWWtztYShNPM1/70KOOXJYM5F.nAnddGxyuQvc6VTYkHCWC0u',0),(14,'test','testytest@tesy.com','$2b$12$CeS6oARRUvjpDTuGFK47c./ilPNMYOstfDJJUGV9RMPFA6SXxLJ7O',0),(15,'test','test@test.or','$2b$12$eIc.JSFTe9iz6aRrkFmFReYQAYJRhPqu8bK3Bl7Z8HSUJ9PdQLA2W',0),(16,'Test','testytest@test.net','$2b$12$D2oUu8k.QVXNIj7MqYhCROZ7x.J7wovc72rococen6tdiCLY/Ch8m',0),(17,'tara','tara@te.com','$2b$12$OW6NkiITWGhumS2gC//nB.RyBpkml7leGyZv.p/NzxAxIESoVOj/C',0),(18,' new','new@new.com','$2b$12$xAgfiTMm6ERaSgrVLGKaSOxYP6xhERDuHXrKV23UjCuL1BW2zmTc6',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'schedulr'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-11 18:07:01
