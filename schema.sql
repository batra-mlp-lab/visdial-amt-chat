-- MySQL dump 10.13  Distrib 5.1.73, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: visual_dialog
-- ------------------------------------------------------
-- Server version	5.1.73

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `visual_dialog`
--

--  CREATE DATABASE /*!32312 IF NOT EXISTS*/ `visual_dialog` /*!40100 DEFAULT CHARACTER SET latin1 */;

--  USE `visual_dialog`;

--
-- Table structure for table `amthits`
--

DROP TABLE IF EXISTS `amthits`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `amthits` (
  `id` varchar(255) NOT NULL,
  `socketId` varchar(255) NOT NULL,
  `assignmentId` varchar(255) NOT NULL,
  `workerId` varchar(255) NOT NULL,
  `approve` varchar(255) NOT NULL,
  `hitId` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `isPaid` tinyint(1) NOT NULL,
  `bonus` int(11) NOT NULL,
  `hitIden` varchar(255) NOT NULL,
  `comment` varchar(255) NOT NULL,
  `image_id` varchar(255) NOT NULL,
  `caption_id` varchar(255) NOT NULL,
  `created_at` int(11) NOT NULL,
  `completed_at` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `image_id` (`image_id`),
  KEY `caption_id` (`caption_id`),
  KEY `hitId_index` (`hitId`),
  KEY `workerId_index` (`workerId`),
  KEY `socketId_index` (`socketId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `answer`
--

DROP TABLE IF EXISTS `answer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `answer` (
  `id` varchar(255) NOT NULL,
  `answer` varchar(255) NOT NULL,
  `question_id` varchar(255) NOT NULL,
  `image_id` varchar(255) NOT NULL,
  `annotationId_id` varchar(255) NOT NULL,
  `sequenceId` varchar(255) NOT NULL,
  `socketId` varchar(255) NOT NULL,
  `sourceId` varchar(255) NOT NULL,
  `destId` varchar(255) NOT NULL,
  `created_at` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `question_id` (`question_id`),
  KEY `image_id` (`image_id`),
  KEY `annotationId_id` (`annotationId_id`),
  KEY `socketId_index` (`socketId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `caption`
--

DROP TABLE IF EXISTS `caption`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `caption` (
  `captionId` varchar(255) NOT NULL,
  `caption` varchar(255) NOT NULL,
  `image_id` varchar(255) NOT NULL,
  PRIMARY KEY (`captionId`),
  KEY `image_id` (`image_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `feedback`
--

DROP TABLE IF EXISTS `feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `workerId` varchar(255) NOT NULL,
  `hitId` varchar(255) NOT NULL,
  `assignmentId` varchar(255) NOT NULL,
  `sequenceId` varchar(255) NOT NULL,
  `feedback` longtext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=98773 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `image`
--

DROP TABLE IF EXISTS `image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `image` (
  `imageId` varchar(255) NOT NULL,
  `imageName` varchar(255) NOT NULL,
  `imageType` varchar(255) NOT NULL,
  `imageSubType` varchar(255) NOT NULL,
  `numHitsFinished` varchar(255) NOT NULL,
  PRIMARY KEY (`imageId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `question`
--

DROP TABLE IF EXISTS `question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `question` (
  `id` varchar(255) NOT NULL,
  `question` varchar(255) NOT NULL,
  `image_id` varchar(255) NOT NULL,
  `annotationId_id` varchar(255) NOT NULL,
  `sequenceId` varchar(255) NOT NULL,
  `socketId` varchar(255) NOT NULL,
  `sourceId` varchar(255) NOT NULL,
  `destId` varchar(255) NOT NULL,
  `created_at` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `image_id` (`image_id`),
  KEY `annotationId_id` (`annotationId_id`),
  KEY `socketId_index` (`socketId`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-14  3:33:26
