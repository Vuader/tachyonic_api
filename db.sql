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
-- Table structure for table `themes`
--

DROP TABLE IF EXISTS `theme`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `theme` (
  `id` varchar(36) NOT NULL,
  `tenant_id` varchar(36) DEFAULT NULL,
  `domain_id` varchar(36) NOT NULL,
  `domain` varchar(64) NOT NULL,
  `name` varchar(64) NOT NULL,
  `logo` longblob NULL,
  `logo_name` varchar(128) NOT NULL DEFAULT '',
  `logo_type` varchar(128) NOT NULL DEFAULT '',
  `logo_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `background` longblob NULL,
  `background_name` varchar(128) NOT NULL DEFAULT '',
  `background_type` varchar(128) NOT NULL DEFAULT '',
  `background_timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_name` (`domain`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `css`
--

DROP TABLE IF EXISTS `css`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `css` (
  `id` varchar(36) NOT NULL,
  `theme_id` varchar(36) NOT NULL,
  `element` varchar(64) NOT NULL,
  `property` varchar(64) NOT NULL,
  `value` varchar(64) NOT NULL,
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `item` (`theme_id`,`element`,`property`),
  CONSTRAINT `css_ibfk_1` FOREIGN KEY (`theme_id`) REFERENCES `theme` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `domain`
--

DROP TABLE IF EXISTS `domain`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `domain` (
  `id` varchar(36) NOT NULL,
  `name` varchar(64) NOT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  `extra` longtext,
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `domain_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `domain`
--

LOCK TABLES `domain` WRITE;
/*!40000 ALTER TABLE `domain` DISABLE KEYS */;
INSERT INTO `domain` VALUES ('3AF4FA64-9AFE-4481-8BB6-24F246599BF3','default',1,NULL,'2017-03-18 19:12:18');
/*!40000 ALTER TABLE `domain` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `role` (
  `id` varchar(36) NOT NULL,
  `name` varchar(64) NOT NULL,
  `description` varchar(128) DEFAULT NULL,
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  `root` enum('False','True') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `role` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES ('766E2877-0E06-440A-8E02-E09988FC21A7','Root',NULL,'2017-03-18 19:12:18','True');
INSERT INTO `role` VALUES ('8dd372aa-edc4-11e6-86e1-14109fe59f3f','Operations',NULL,'2017-03-18 19:12:18','False');
INSERT INTO `role` VALUES ('9cd65b14-edc4-11e6-86e1-14109fe59f3f','Administrator',NULL,'2017-03-18 19:12:18','False');
INSERT INTO `role` VALUES ('a525e582-edc4-11e6-86e1-14109fe59f3f','Account Manager',NULL,'2017-03-18 19:12:18','False');
INSERT INTO `role` VALUES ('b7706e6a-edc4-11e6-86e1-14109fe59f3f','Billing',NULL,'2017-03-18 19:12:18','False');
INSERT INTO `role` VALUES ('bced7216-edc4-11e6-86e1-14109fe59f3f','Customer',NULL,'2017-03-18 19:12:18','False');
INSERT INTO `role` VALUES ('F4FA990F-8D08-41C4-A927-4B08D86374A0','Support',NULL,'2017-03-18 19:12:18','False');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tenant`
--

DROP TABLE IF EXISTS `tenant`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tenant` (
  `id` varchar(36) NOT NULL,
  `tenant_id` varchar(36) DEFAULT NULL,
  `domain_id` varchar(36) NOT NULL,
  `external_id` varchar(36) DEFAULT NULL,
  `tenant_type` enum('individual','organization') NOT NULL DEFAULT 'individual',
  `name` varchar(100) NOT NULL,
  `title` varchar(10) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phone_mobile` varchar(25) DEFAULT NULL,
  `phone_office` varchar(25) DEFAULT NULL,
  `phone_home` varchar(25) DEFAULT NULL,
  `phone_fax` varchar(25) DEFAULT NULL,
  `idno` varchar(30) DEFAULT NULL,
  `reg` varchar(50) DEFAULT NULL,
  `taxno` varchar(50) DEFAULT NULL,
  `idtype` varchar(20) DEFAULT NULL,
  `employer` varchar(60) DEFAULT NULL,
  `designation` varchar(60) DEFAULT NULL,
  `bill_address` enum('Physical','Post') DEFAULT NULL,
  `address_line1` varchar(60) DEFAULT NULL,
  `address_line2` varchar(60) DEFAULT NULL,
  `address_line3` varchar(60) DEFAULT NULL,
  `address_city` varchar(60) DEFAULT NULL,
  `address_code` varchar(60) DEFAULT NULL,
  `address_state` varchar(60) DEFAULT NULL,
  `address_country` varchar(60) DEFAULT NULL,
  `post_line1` varchar(60) DEFAULT NULL,
  `post_line2` varchar(60) DEFAULT NULL,
  `post_line3` varchar(60) DEFAULT NULL,
  `post_city` varchar(60) DEFAULT NULL,
  `post_code` varchar(60) DEFAULT NULL,
  `post_state` varchar(60) DEFAULT NULL,
  `post_country` varchar(60) DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tenant_unique` (`domain_id`,`external_id`,`name`),
  KEY `tenant_id` (`tenant_id`),
  CONSTRAINT `tenant_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `tenant_ibfk_2` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `token`
--

DROP TABLE IF EXISTS `token`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `token` (
  `id` varchar(36) NOT NULL,
  `user_id` varchar(36) NOT NULL,
  `token` varchar(255) NOT NULL DEFAULT '',
  `token_expire` datetime DEFAULT NULL,
  `otp` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `token_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` varchar(36) NOT NULL,
  `domain_id` varchar(36) NOT NULL,
  `external_id` varchar(36) DEFAULT NULL,
  `tenant_id` varchar(36) DEFAULT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(100) NOT NULL,
  `title` varchar(10) DEFAULT NULL,
  `phone_mobile` varchar(25) DEFAULT NULL,
  `phone_office` varchar(25) DEFAULT NULL,
  `employer` varchar(60) DEFAULT NULL,
  `designation` varchar(60) DEFAULT NULL,
  `last_login` datetime DEFAULT NULL,
  `enabled` tinyint(1) DEFAULT '1',
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  UNIQUE KEY `email` (`email`),
  KEY `tenant_id` (`tenant_id`),
  KEY `domain_id` (`domain_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_ibfk_2` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('C0418B28-CCAE-459E-8882-568F433C46FB','3AF4FA64-9AFE-4481-8BB6-24F246599BF3',NULL,NULL,'root','$2b$15$Ij1uoXuF3ZAuxpg6WNZ5RuPPqcKMA80Vs7ELjzF0m/WcxQNrl4ezq','root@example.com','Root',NULL,NULL,NULL,NULL,NULL,'2017-03-25 18:26:30',1,'2017-03-18 19:12:18');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_role`
--

DROP TABLE IF EXISTS `user_role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_role` (
  `id` varchar(36) NOT NULL,
  `role_id` varchar(36) NOT NULL,
  `domain_id` varchar(36) NOT NULL,
  `tenant_id` varchar(36) DEFAULT NULL,
  `user_id` varchar(36) DEFAULT NULL,
  `creation_time` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_role_tenant` (`role_id`,`domain_id`,`user_id`,`tenant_id`),
  KEY `domain_id` (`domain_id`),
  KEY `tenant_id` (`tenant_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `user_role_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_role_ibfk_2` FOREIGN KEY (`domain_id`) REFERENCES `domain` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_role_ibfk_3` FOREIGN KEY (`tenant_id`) REFERENCES `tenant` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_role_ibfk_4` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_role`
--

LOCK TABLES `user_role` WRITE;
/*!40000 ALTER TABLE `user_role` DISABLE KEYS */;
INSERT INTO `user_role` VALUES ('5E72FF71-B34E-42CC-964F-1338E9417438','766E2877-0E06-440A-8E02-E09988FC21A7','3AF4FA64-9AFE-4481-8BB6-24F246599BF3',NULL,'C0418B28-CCAE-459E-8882-568F433C46FB','2017-03-18 19:12:18');
/*!40000 ALTER TABLE `user_role` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
