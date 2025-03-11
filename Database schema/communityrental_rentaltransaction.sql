-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: communityrental
-- ------------------------------------------------------
-- Server version	8.0.39

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `rentaltransaction`
--

DROP TABLE IF EXISTS `rentaltransaction`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rentaltransaction` (
  `transaction_ID` int NOT NULL AUTO_INCREMENT,
  `equip_ID` int DEFAULT NULL,
  `borrower_ID` int DEFAULT NULL,
  `lender_ID` int DEFAULT NULL,
  `start_date` date DEFAULT NULL,
  `end_date` date DEFAULT NULL,
  `status` enum('예약 중','대여 중','대여 가능') NOT NULL DEFAULT '대여 가능',
  `transaction_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `review_comment` text,
  `review_rating` float DEFAULT NULL,
  `equipment_quality_review` enum('최상','상','중상','중','중하','하') DEFAULT NULL,
  `equipment_comment` text,
  `lender_rating` int DEFAULT NULL,
  `lender_comment` text,
  `review_completed` tinyint(1) DEFAULT '0',
  `borrower_rating` int DEFAULT NULL,
  `borrower_comment` text,
  PRIMARY KEY (`transaction_ID`),
  KEY `equip_ID` (`equip_ID`),
  KEY `borrower_ID` (`borrower_ID`),
  KEY `lender_ID` (`lender_ID`),
  CONSTRAINT `rentaltransaction_ibfk_1` FOREIGN KEY (`equip_ID`) REFERENCES `equipment` (`equip_ID`),
  CONSTRAINT `rentaltransaction_ibfk_2` FOREIGN KEY (`borrower_ID`) REFERENCES `user` (`ID`),
  CONSTRAINT `rentaltransaction_ibfk_3` FOREIGN KEY (`lender_ID`) REFERENCES `user` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-08  3:22:21
