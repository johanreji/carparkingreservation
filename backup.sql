-- MySQL dump 10.13  Distrib 8.0.15, for Linux (x86_64)
--
-- Host: localhost    Database: bookmyslot
-- ------------------------------------------------------
-- Server version	8.0.15

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
 SET NAMES utf8mb4 ;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Customer`
--

DROP TABLE IF EXISTS `Customer`;
SET character_set_client = utf8mb4 ;
CREATE TABLE `Customer` (
  `CustomerID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(20) DEFAULT NULL,
  `MobileNumber` bigint(20) NOT NULL,
  `VehicleNumber` varchar(20) DEFAULT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `MobileNumber` (`MobileNumber`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Customer`
--

LOCK TABLES `Customer` WRITE;
/*!40000 ALTER TABLE `Customer` DISABLE KEYS */;
INSERT INTO `Customer` VALUES (25,'Abhijith',8547992701,'KL15D4565','abhijithka96@gmail.com','abhijith123@'),(27,'Kiran',45465464644,'KL56A5454','kiranjithka@gmail.com','1234');
/*!40000 ALTER TABLE `Customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PenaltyReservations`
--

DROP TABLE IF EXISTS `PenaltyReservations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `PenaltyReservations` (
  `ReservationID` bigint(20) NOT NULL,
  `SlotID` int(11) NOT NULL,
  `EndTime` timestamp NULL DEFAULT NULL,
  `LastSeenTime` timestamp NULL DEFAULT NULL,
  PRIMARY KEY (`ReservationID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 
/*!40101 SET character_set_client = @saved_cs_client */;
/*COLLATE=utf8mb4_0900_ai_ci */;

--
-- Dumping data for table `PenaltyReservations`
--

LOCK TABLES `PenaltyReservations` WRITE;
/*!40000 ALTER TABLE `PenaltyReservations` DISABLE KEYS */;
INSERT INTO `PenaltyReservations` VALUES (22,3,'2019-04-25 07:43:00','2019-04-26 04:55:00'),(28,2,'2019-04-26 04:11:00','2019-04-26 04:55:00'),(29,0,'2019-04-26 07:00:00','2019-04-26 13:00:00');
/*!40000 ALTER TABLE `PenaltyReservations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reservation`
--

DROP TABLE IF EXISTS `Reservation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Reservation` (
  `ReservationID` int(11) NOT NULL AUTO_INCREMENT,
  `CustomerID` int(11) DEFAULT NULL,
  `BookingTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ReservationStatus` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`ReservationID`),
  KEY `CustomerID` (`CustomerID`),
  CONSTRAINT `Reservation_ibfk_1` FOREIGN KEY (`CustomerID`) REFERENCES `Customer` (`CustomerID`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reservation`
--

LOCK TABLES `Reservation` WRITE;
/*!40000 ALTER TABLE `Reservation` DISABLE KEYS */;
INSERT INTO `Reservation` VALUES (20,25,'2019-04-24 15:54:57',1),(21,25,'2019-04-25 04:39:58',1),(22,25,'2019-04-25 04:44:38',1),(28,25,'2019-04-26 04:08:33',1),(29,25,'2019-04-26 06:18:43',1),(32,25,'2019-04-26 12:08:37',1),(33,27,'2019-04-28 02:25:34',1),(34,27,'2019-04-28 02:35:13',1),(35,25,'2019-04-28 03:06:14',1);
/*!40000 ALTER TABLE `Reservation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ReservedSlots`
--

DROP TABLE IF EXISTS `ReservedSlots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `ReservedSlots` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `ReservationID` int(11) DEFAULT NULL,
  `SlotID` int(11) DEFAULT NULL,
  `StartTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `EndTime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`),
  KEY `ReservationID` (`ReservationID`),
  KEY `SlotID` (`SlotID`),
  CONSTRAINT `ReservedSlots_ibfk_1` FOREIGN KEY (`ReservationID`) REFERENCES `Reservation` (`ReservationID`),
  CONSTRAINT `ReservedSlots_ibfk_2` FOREIGN KEY (`SlotID`) REFERENCES `Slots` (`SlotID`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ReservedSlots`
--

LOCK TABLES `ReservedSlots` WRITE;
/*!40000 ALTER TABLE `ReservedSlots` DISABLE KEYS */;
INSERT INTO `ReservedSlots` VALUES (14,20,1,'2019-04-24 15:55:00','2019-04-25 15:55:00'),(16,22,3,'2019-04-25 04:43:00','2019-04-25 07:43:00'),(22,28,2,'2019-04-26 04:08:00','2019-04-26 04:11:00'),(23,29,0,'2019-04-26 06:18:00','2019-04-26 07:00:00'),(26,32,2,'2019-04-26 12:08:00','2019-04-26 13:20:00'),(27,33,1,'2019-04-28 07:00:00','2019-04-29 18:00:00'),(28,34,3,'2019-04-27 18:30:00','2019-04-29 05:00:00'),(29,35,0,'2019-04-28 03:06:00','2019-04-29 03:06:00');
/*!40000 ALTER TABLE `ReservedSlots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Slots`
--

DROP TABLE IF EXISTS `Slots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `Slots` (
  `SlotID` int(11) NOT NULL,
  `occupied` tinyint(1) NOT NULL,
  `CNNTimestamp` timestamp NULL DEFAULT NULL,
  `CNNFlag` tinyint(1) DEFAULT NULL,
  `ReservationID` bigint(20) DEFAULT NULL,
  `EndTime` timestamp NULL DEFAULT NULL,
  `confidence` int(11) DEFAULT '0',
  PRIMARY KEY (`SlotID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Slots`
--

LOCK TABLES `Slots` WRITE;
/*!40000 ALTER TABLE `Slots` DISABLE KEYS */;
INSERT INTO `Slots` VALUES (0,1,'2019-04-26 06:06:55',0,29,'2019-04-26 07:00:00',9),(1,0,'2019-04-25 18:32:00',0,NULL,NULL,0),(2,1,'2019-04-26 05:12:59',0,32,'2019-04-26 13:20:00',10),(3,0,'2019-04-26 05:00:00',0,NULL,NULL,8);
/*!40000 ALTER TABLE `Slots` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`django`@`localhost`*/ /*!50003 TRIGGER `confinc` BEFORE UPDATE ON `Slots` FOR EACH ROW BEGIN
IF NEW.occupied = OLD.occupied THEN SET NEW.confidence = OLD.confidence + 1;
END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `UnauthorizedParkings`
--

DROP TABLE IF EXISTS `UnauthorizedParkings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `UnauthorizedParkings` (
  `SlotID` int(11) NOT NULL,
  `StartTime` timestamp NOT NULL,
  `LastSeenTime` timestamp NULL DEFAULT NULL,
  `status` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`StartTime`,`SlotID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `UnauthorizedParkings`
--

LOCK TABLES `UnauthorizedParkings` WRITE;
/*!40000 ALTER TABLE `UnauthorizedParkings` DISABLE KEYS */;
INSERT INTO `UnauthorizedParkings` VALUES (0,'2019-04-26 06:04:51','2019-04-26 06:05:00',0),(0,'2019-04-26 06:06:55','2019-04-26 06:20:00',0);
/*!40000 ALTER TABLE `UnauthorizedParkings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accountdetail`
--

DROP TABLE IF EXISTS `accountdetail`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `accountdetail` (
  `customerid` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`customerid`)
) ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accountdetail`
--

LOCK TABLES `accountdetail` WRITE;
/*!40000 ALTER TABLE `accountdetail` DISABLE KEYS */;
INSERT INTO `accountdetail` VALUES (1,'kumsdan@bjp.com','vannee'),(2,'kumsda]an@bjp.com','vaaannee'),(11,'asas','Asas'),(12,'asas','Asas'),(13,'asas','Asas'),(14,'asas','Asas'),(15,'try','try'),(16,'dssa','qwer'),(17,'dssd','qwer'),(18,'johan','johan123'),(19,'dskansl','an kas'),(20,'sand a','1234'),(21,'sand a','1234'),(22,'sand a','1234'),(23,'sand a','1234'),(24,'thambi','thambi'),(25,'sadsd','123'),(26,'aa','aa'),(27,'adarsh','adarsh');
/*!40000 ALTER TABLE `accountdetail` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser`
--

DROP TABLE IF EXISTS `accounts_customuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `accounts_customuser` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `vehicle_number` varchar(20) NOT NULL,
  `mobile_number` bigint(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `mobile_number` (`mobile_number`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser`
--

LOCK TABLES `accounts_customuser` WRITE;
/*!40000 ALTER TABLE `accounts_customuser` DISABLE KEYS */;
INSERT INTO `accounts_customuser` VALUES (1,'pbkdf2_sha256$150000$j1zWnI9nA3PD$CMq7IAWte+TMCEAJBA8VlfspzYWLRqhYMsu/gOr/5uM=',NULL,0,'kiranjithka','kiranjith','ka','kiranjithka@gmail.com',0,1,'2019-04-27 17:19:03.916767','KL12b5566',7907286676);
/*!40000 ALTER TABLE `accounts_customuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_groups`
--

DROP TABLE IF EXISTS `accounts_customuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `accounts_customuser_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_groups_customuser_id_group_id_c074bdcb_uniq` (`customuser_id`,`group_id`),
  KEY `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` (`group_id`),
  CONSTRAINT `accounts_customuser__customuser_id_bc55088e_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser_groups_group_id_86ba5f9e_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_groups`
--

LOCK TABLES `accounts_customuser_groups` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `accounts_customuser_user_permissions`
--

DROP TABLE IF EXISTS `accounts_customuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `accounts_customuser_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customuser_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `accounts_customuser_user_customuser_id_permission_9632a709_uniq` (`customuser_id`,`permission_id`),
  KEY `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` (`permission_id`),
  CONSTRAINT `accounts_customuser__customuser_id_0deaefae_fk_accounts_` FOREIGN KEY (`customuser_id`) REFERENCES `accounts_customuser` (`id`),
  CONSTRAINT `accounts_customuser__permission_id_aea3d0e5_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accounts_customuser_user_permissions`
--

LOCK TABLES `accounts_customuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `accounts_customuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can view permission',1,'view_permission'),(5,'Can add group',2,'add_group'),(6,'Can change group',2,'change_group'),(7,'Can delete group',2,'delete_group'),(8,'Can view group',2,'view_group'),(9,'Can add content type',3,'add_contenttype'),(10,'Can change content type',3,'change_contenttype'),(11,'Can delete content type',3,'delete_contenttype'),(12,'Can view content type',3,'view_contenttype'),(13,'Can add user',4,'add_customuser'),(14,'Can change user',4,'change_customuser'),(15,'Can delete user',4,'delete_customuser'),(16,'Can view user',4,'view_customuser'),(17,'Can add log entry',5,'add_logentry'),(18,'Can change log entry',5,'change_logentry'),(19,'Can delete log entry',5,'delete_logentry'),(20,'Can view log entry',5,'view_logentry'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add completed task',7,'add_completedtask'),(26,'Can change completed task',7,'change_completedtask'),(27,'Can delete completed task',7,'delete_completedtask'),(28,'Can view completed task',7,'view_completedtask'),(29,'Can add task',8,'add_task'),(30,'Can change task',8,'change_task'),(31,'Can delete task',8,'delete_task'),(32,'Can view task',8,'view_task');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `background_task`
--

DROP TABLE IF EXISTS `background_task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `background_task` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(190) NOT NULL,
  `task_params` longtext NOT NULL,
  `task_hash` varchar(40) NOT NULL,
  `verbose_name` varchar(255) DEFAULT NULL,
  `priority` int(11) NOT NULL,
  `run_at` datetime(6) NOT NULL,
  `repeat` bigint(20) NOT NULL,
  `repeat_until` datetime(6) DEFAULT NULL,
  `queue` varchar(190) DEFAULT NULL,
  `attempts` int(11) NOT NULL,
  `failed_at` datetime(6) DEFAULT NULL,
  `last_error` longtext NOT NULL,
  `locked_by` varchar(64) DEFAULT NULL,
  `locked_at` datetime(6) DEFAULT NULL,
  `creator_object_id` int(10) unsigned DEFAULT NULL,
  `creator_content_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `background_task_creator_content_type_61cc9af3_fk_django_co` (`creator_content_type_id`),
  KEY `background_task_task_name_4562d56a` (`task_name`),
  KEY `background_task_task_hash_d8f233bd` (`task_hash`),
  KEY `background_task_priority_88bdbce9` (`priority`),
  KEY `background_task_run_at_7baca3aa` (`run_at`),
  KEY `background_task_queue_1d5f3a40` (`queue`),
  KEY `background_task_attempts_a9ade23d` (`attempts`),
  KEY `background_task_failed_at_b81bba14` (`failed_at`),
  KEY `background_task_locked_by_db7779e3` (`locked_by`),
  KEY `background_task_locked_at_0fb0f225` (`locked_at`),
  CONSTRAINT `background_task_creator_content_type_61cc9af3_fk_django_co` FOREIGN KEY (`creator_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `background_task`
--

LOCK TABLES `background_task` WRITE;
/*!40000 ALTER TABLE `background_task` DISABLE KEYS */;
/*!40000 ALTER TABLE `background_task` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `background_task_completedtask`
--

DROP TABLE IF EXISTS `background_task_completedtask`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `background_task_completedtask` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `task_name` varchar(190) NOT NULL,
  `task_params` longtext NOT NULL,
  `task_hash` varchar(40) NOT NULL,
  `verbose_name` varchar(255) DEFAULT NULL,
  `priority` int(11) NOT NULL,
  `run_at` datetime(6) NOT NULL,
  `repeat` bigint(20) NOT NULL,
  `repeat_until` datetime(6) DEFAULT NULL,
  `queue` varchar(190) DEFAULT NULL,
  `attempts` int(11) NOT NULL,
  `failed_at` datetime(6) DEFAULT NULL,
  `last_error` longtext NOT NULL,
  `locked_by` varchar(64) DEFAULT NULL,
  `locked_at` datetime(6) DEFAULT NULL,
  `creator_object_id` int(10) unsigned DEFAULT NULL,
  `creator_content_type_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `background_task_comp_creator_content_type_21d6a741_fk_django_co` (`creator_content_type_id`),
  KEY `background_task_completedtask_task_name_388dabc2` (`task_name`),
  KEY `background_task_completedtask_task_hash_91187576` (`task_hash`),
  KEY `background_task_completedtask_priority_9080692e` (`priority`),
  KEY `background_task_completedtask_run_at_77c80f34` (`run_at`),
  KEY `background_task_completedtask_queue_61fb0415` (`queue`),
  KEY `background_task_completedtask_attempts_772a6783` (`attempts`),
  KEY `background_task_completedtask_failed_at_3de56618` (`failed_at`),
  KEY `background_task_completedtask_locked_by_edc8a213` (`locked_by`),
  KEY `background_task_completedtask_locked_at_29c62708` (`locked_at`),
  CONSTRAINT `background_task_comp_creator_content_type_21d6a741_fk_django_co` FOREIGN KEY (`creator_content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `background_task_completedtask`
--

LOCK TABLES `background_task_completedtask` WRITE;
/*!40000 ALTER TABLE `background_task_completedtask` DISABLE KEYS */;
/*!40000 ALTER TABLE `background_task_completedtask` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_accounts_customuser_id` FOREIGN KEY (`user_id`) REFERENCES `accounts_customuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (4,'accounts','customuser'),(5,'admin','logentry'),(2,'auth','group'),(1,'auth','permission'),(7,'background_task','completedtask'),(8,'background_task','task'),(3,'contenttypes','contenttype'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2019-04-27 17:12:13.886325'),(2,'contenttypes','0002_remove_content_type_name','2019-04-27 17:12:15.400960'),(3,'auth','0001_initial','2019-04-27 17:12:16.795077'),(4,'auth','0002_alter_permission_name_max_length','2019-04-27 17:12:21.878982'),(5,'auth','0003_alter_user_email_max_length','2019-04-27 17:12:21.992655'),(6,'auth','0004_alter_user_username_opts','2019-04-27 17:12:22.092940'),(7,'auth','0005_alter_user_last_login_null','2019-04-27 17:12:22.209086'),(8,'auth','0006_require_contenttypes_0002','2019-04-27 17:12:22.302506'),(9,'auth','0007_alter_validators_add_error_messages','2019-04-27 17:12:22.402868'),(10,'auth','0008_alter_user_username_max_length','2019-04-27 17:12:22.517359'),(11,'auth','0009_alter_user_last_name_max_length','2019-04-27 17:12:22.670608'),(12,'auth','0010_alter_group_name_max_length','2019-04-27 17:12:22.907503'),(13,'auth','0011_update_proxy_permissions','2019-04-27 17:12:23.028433'),(14,'accounts','0001_initial','2019-04-27 17:12:24.555690'),(15,'admin','0001_initial','2019-04-27 17:12:52.111457'),(16,'admin','0002_logentry_remove_auto_add','2019-04-27 17:12:54.561147'),(17,'admin','0003_logentry_add_action_flag_choices','2019-04-27 17:12:54.736781'),(18,'background_task','0001_initial','2019-04-27 17:12:55.792007'),(19,'background_task','0002_auto_20170927_1109','2019-04-27 17:13:12.876262'),(20,'sessions','0001_initial','2019-04-27 17:13:13.311834');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
 SET character_set_client = utf8mb4 ;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('1g0emswnuwooim7heyyypjyil85owb6b','MTAyZWFmNzA4MTg5YWYxZmJhOWM2YTA0ZDU0ZGEyYzVhZDdkYWM3MTp7ImxvZ2dlZGluIjowLCJuYW1lIjoidXNlciJ9','2019-05-11 17:13:29.831531'),('h89gz3grp3owsj2kiwmqu54d7l0oe2ys','MTAyZWFmNzA4MTg5YWYxZmJhOWM2YTA0ZDU0ZGEyYzVhZDdkYWM3MTp7ImxvZ2dlZGluIjowLCJuYW1lIjoidXNlciJ9','2019-05-12 02:45:48.017223'),('lhyi3weya2t9i9lfj0hncmuw3b72f17i','MTAyZWFmNzA4MTg5YWYxZmJhOWM2YTA0ZDU0ZGEyYzVhZDdkYWM3MTp7ImxvZ2dlZGluIjowLCJuYW1lIjoidXNlciJ9','2019-05-12 03:03:52.554940'),('w1i1l16szfpm5fhm6xie2ivkaiu5320z','M2FhNGQ4NTI4YjNlZGE1MjY0ZjU1MGEwYjNiMGZjNzZkNzhiMzc5MTp7ImxvZ2dlZGluIjoxLCJuYW1lIjoiQWJoaWppdGgiLCJjdXN0b21lcmlkIjoyNX0=','2019-05-12 03:05:25.005784');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-04-28 20:12:42
