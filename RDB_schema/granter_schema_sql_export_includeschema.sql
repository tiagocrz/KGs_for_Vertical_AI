CREATE DATABASE  IF NOT EXISTS `granter` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `granter`;
-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: localhost    Database: granter
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=209 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=95 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=370 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_activity`
--

DROP TABLE IF EXISTS `granter_activity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_activity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(100) NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `description` longtext,
  `application_id` bigint DEFAULT NULL,
  `company_id` bigint NOT NULL,
  `file_id` bigint DEFAULT NULL,
  `profile_id` bigint NOT NULL,
  `created_by_expert` tinyint(1) NOT NULL,
  `activity_date` datetime(6) DEFAULT NULL,
  `data` longtext,
  `data_id` varchar(100) DEFAULT NULL,
  `opportunity_id` bigint DEFAULT NULL,
  `data_type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_activity_application_id_4284cf67_fk_granter_a` (`application_id`),
  KEY `granter_activity_company_id_b2808af0_fk_granter_company_id` (`company_id`),
  KEY `granter_activity_file_id_6f2e8b31_fk_granter_companyfile_id` (`file_id`),
  KEY `granter_activity_profile_id_6f7995a1_fk_granter_profile_id` (`profile_id`),
  KEY `granter_activity_opportunity_id_8907ad01_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_activity_application_id_4284cf67_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_activity_company_id_b2808af0_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_activity_file_id_6f2e8b31_fk_granter_companyfile_id` FOREIGN KEY (`file_id`) REFERENCES `granter_companyfile` (`id`),
  CONSTRAINT `granter_activity_opportunity_id_8907ad01_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`),
  CONSTRAINT `granter_activity_profile_id_6f7995a1_fk_granter_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_application`
--

DROP TABLE IF EXISTS `granter_application`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_application` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `state` varchar(30) NOT NULL,
  `codename` varchar(60) NOT NULL,
  `title` varchar(150) NOT NULL,
  `other_data` json DEFAULT NULL,
  `company_id` bigint DEFAULT NULL,
  `opportunity_id` bigint DEFAULT NULL,
  `profile_creator_id` bigint DEFAULT NULL,
  `pricing_option` varchar(30) DEFAULT NULL,
  `ai_review_state` varchar(30) DEFAULT NULL,
  `consortium_id` bigint DEFAULT NULL,
  `sale_confirmed` tinyint(1) NOT NULL,
  `approved_grant_amount` varchar(100) DEFAULT NULL,
  `success_fee` varchar(50) DEFAULT NULL,
  `success_payment_amount` varchar(100) DEFAULT NULL,
  `upfront_payment_amount` varchar(100) DEFAULT NULL,
  `initial_summary` longtext,
  `writer_mode` varchar(30) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `consortium_id` (`consortium_id`),
  KEY `granter_application_company_id_847c5b4f_fk_granter_company_id` (`company_id`),
  KEY `granter_application_opportunity_id_6a6373f2_fk_granter_o` (`opportunity_id`),
  KEY `granter_application_profile_creator_id_4a94343d_fk_granter_p` (`profile_creator_id`),
  CONSTRAINT `granter_application_company_id_847c5b4f_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_application_consortium_id_ff9bdeba_fk_granter_c` FOREIGN KEY (`consortium_id`) REFERENCES `granter_consortium` (`id`),
  CONSTRAINT `granter_application_opportunity_id_6a6373f2_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`),
  CONSTRAINT `granter_application_profile_creator_id_4a94343d_fk_granter_p` FOREIGN KEY (`profile_creator_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_application_shared_profile`
--

DROP TABLE IF EXISTS `granter_application_shared_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_application_shared_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `application_id` bigint NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_application_shar_application_id_profile_i_09183e05_uniq` (`application_id`,`profile_id`),
  KEY `granter_application__profile_id_6b9e7234_fk_granter_p` (`profile_id`),
  CONSTRAINT `granter_application__application_id_7a8979d8_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_application__profile_id_6b9e7234_fk_granter_p` FOREIGN KEY (`profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_applicationfile`
--

DROP TABLE IF EXISTS `granter_applicationfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_applicationfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(1500) NOT NULL,
  `uploaded_file` varchar(1500) NOT NULL,
  `vector_indexed` tinyint(1) NOT NULL,
  `type` varchar(30) NOT NULL,
  `application_id` bigint NOT NULL,
  `document_type_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_applicationf_application_id_1aa2b0d5_fk_granter_a` (`application_id`),
  KEY `granter_applicationf_document_type_id_83886dda_fk_granter_d` (`document_type_id`),
  CONSTRAINT `granter_applicationf_application_id_1aa2b0d5_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_applicationf_document_type_id_83886dda_fk_granter_d` FOREIGN KEY (`document_type_id`) REFERENCES `granter_doctype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_applicationinput`
--

DROP TABLE IF EXISTS `granter_applicationinput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_applicationinput` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `codename` varchar(60) DEFAULT NULL,
  `value` longtext NOT NULL,
  `summarized_value` longtext,
  `application_id` bigint NOT NULL,
  `company_id` bigint NOT NULL,
  `question_id` bigint DEFAULT NULL,
  `updated_profile_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_applicationi_application_id_9db944b0_fk_granter_a` (`application_id`),
  KEY `granter_applicationi_company_id_e5313da0_fk_granter_c` (`company_id`),
  KEY `granter_applicationi_question_id_81754ecf_fk_granter_q` (`question_id`),
  KEY `granter_applicationi_updated_profile_id_f1afc62e_fk_granter_p` (`updated_profile_id`),
  CONSTRAINT `granter_applicationi_application_id_9db944b0_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_applicationi_company_id_e5313da0_fk_granter_c` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_applicationi_question_id_81754ecf_fk_granter_q` FOREIGN KEY (`question_id`) REFERENCES `granter_question` (`id`),
  CONSTRAINT `granter_applicationi_updated_profile_id_f1afc62e_fk_granter_p` FOREIGN KEY (`updated_profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_applicationoutput`
--

DROP TABLE IF EXISTS `granter_applicationoutput`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_applicationoutput` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `codename` varchar(250) NOT NULL,
  `prompt` longtext,
  `generated_value` longtext,
  `curated_value` longtext,
  `application_id` bigint NOT NULL,
  `company_id` bigint DEFAULT NULL,
  `updated_profile_id` bigint DEFAULT NULL,
  `multiple_context` varchar(250) DEFAULT NULL,
  `order` int unsigned DEFAULT NULL,
  `not_html` tinyint(1) NOT NULL,
  `parent` varchar(50) NOT NULL,
  `summary` longtext,
  PRIMARY KEY (`id`),
  KEY `granter_applicationo_application_id_85b62c1c_fk_granter_a` (`application_id`),
  KEY `granter_applicationo_updated_profile_id_b617dbd9_fk_granter_p` (`updated_profile_id`),
  KEY `granter_applicationo_company_id_716230cd_fk_granter_c` (`company_id`),
  CONSTRAINT `granter_applicationo_application_id_85b62c1c_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_applicationo_company_id_716230cd_fk_granter_c` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_applicationo_updated_profile_id_b617dbd9_fk_granter_p` FOREIGN KEY (`updated_profile_id`) REFERENCES `granter_profile` (`id`),
  CONSTRAINT `granter_applicationoutput_chk_1` CHECK ((`order` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=220 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_chatconversation`
--

DROP TABLE IF EXISTS `granter_chatconversation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_chatconversation` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `thread_id` varchar(25) NOT NULL,
  `messages` json NOT NULL,
  `title` varchar(100) DEFAULT NULL,
  `sentiment` varchar(50) DEFAULT NULL,
  `confidence_score` double DEFAULT NULL,
  `company_id` bigint NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `thread_id` (`thread_id`),
  KEY `granter_chatconversa_company_id_413ff85c_fk_granter_c` (`company_id`),
  KEY `granter_chatconversa_profile_id_e15a37b9_fk_granter_p` (`profile_id`),
  CONSTRAINT `granter_chatconversa_company_id_413ff85c_fk_granter_c` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_chatconversa_profile_id_e15a37b9_fk_granter_p` FOREIGN KEY (`profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_comment`
--

DROP TABLE IF EXISTS `granter_comment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_comment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `position_id` varchar(100) NOT NULL,
  `content` longtext NOT NULL,
  `is_resolved` tinyint(1) NOT NULL,
  `application_id` bigint NOT NULL,
  `profile_id` bigint NOT NULL,
  `reply_to_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_comment_application_id_4bbeff17_fk_granter_a` (`application_id`),
  KEY `granter_comment_profile_id_df770973_fk_granter_profile_id` (`profile_id`),
  KEY `granter_comment_reply_to_id_be95aa55_fk_granter_comment_id` (`reply_to_id`),
  CONSTRAINT `granter_comment_application_id_4bbeff17_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_comment_profile_id_df770973_fk_granter_profile_id` FOREIGN KEY (`profile_id`) REFERENCES `granter_profile` (`id`),
  CONSTRAINT `granter_comment_reply_to_id_be95aa55_fk_granter_comment_id` FOREIGN KEY (`reply_to_id`) REFERENCES `granter_comment` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_company`
--

DROP TABLE IF EXISTS `granter_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_company` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(100) NOT NULL,
  `legal_name` varchar(100) NOT NULL,
  `address` varchar(200) NOT NULL,
  `post_code` varchar(100) NOT NULL,
  `city` varchar(100) NOT NULL,
  `country` varchar(30) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `legal_form` varchar(100) DEFAULT NULL,
  `activity_date` date DEFAULT NULL,
  `company_id` varchar(50) NOT NULL,
  `tax_id` varchar(50) NOT NULL,
  `social_security_id` varchar(50) NOT NULL,
  `is_sme` tinyint(1) NOT NULL,
  `employees_n` int unsigned DEFAULT NULL,
  `annual_revenue` decimal(14,2) DEFAULT NULL,
  `description` longtext NOT NULL,
  `cover_image` varchar(100) NOT NULL,
  `website_data` longtext,
  `owner_id` bigint DEFAULT NULL,
  `stripe_customer_id` varchar(200) DEFAULT NULL,
  `digital_component` longtext,
  `future_goals_infrastructure` longtext,
  `future_goals_internationalization` longtext,
  `future_goals_machinery_and_equipments` longtext,
  `future_goals_marketing` longtext,
  `future_goals_rd` longtext,
  `green_component` longtext,
  `team_description` longtext,
  `future_goals_hr` longtext,
  `onboarding_state` varchar(100) DEFAULT NULL,
  `matches_generating` tinyint(1) NOT NULL,
  `userless` tinyint(1) NOT NULL,
  `cae` json DEFAULT NULL,
  `whitelabel_id` bigint DEFAULT NULL,
  `related_operations` longtext,
  `shareholders` longtext,
  `other_data` json DEFAULT NULL,
  `source` varchar(200) NOT NULL,
  `subscription_id` bigint DEFAULT NULL,
  `extra_information` longtext,
  `matching_order` json NOT NULL DEFAULT (_utf8mb3'{"closing_soon": 1, "co_financing_percentage": 2, "grant_amount": 3, "application_difficulty": 4}'),
  `agent_language` varchar(10) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_company_owner_id_a5db6676_fk_granter_profile_id` (`owner_id`),
  KEY `granter_company_whitelabel_id_8f5b3ccd_fk_granter_whitelabel_id` (`whitelabel_id`),
  KEY `granter_company_subscription_id_bdda824d_fk_granter_s` (`subscription_id`),
  CONSTRAINT `granter_company_owner_id_a5db6676_fk_granter_profile_id` FOREIGN KEY (`owner_id`) REFERENCES `granter_profile` (`id`),
  CONSTRAINT `granter_company_subscription_id_bdda824d_fk_granter_s` FOREIGN KEY (`subscription_id`) REFERENCES `granter_subscription` (`id`),
  CONSTRAINT `granter_company_whitelabel_id_8f5b3ccd_fk_granter_whitelabel_id` FOREIGN KEY (`whitelabel_id`) REFERENCES `granter_whitelabel` (`id`),
  CONSTRAINT `granter_company_chk_1` CHECK ((`employees_n` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_company_profiles`
--

DROP TABLE IF EXISTS `granter_company_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_company_profiles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `company_id` bigint NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_company_profile_company_id_profile_id_82570ecf_uniq` (`company_id`,`profile_id`),
  KEY `granter_company_prof_profile_id_74945154_fk_granter_p` (`profile_id`),
  CONSTRAINT `granter_company_prof_company_id_16bd2075_fk_granter_c` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_company_prof_profile_id_74945154_fk_granter_p` FOREIGN KEY (`profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_companyfile`
--

DROP TABLE IF EXISTS `granter_companyfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_companyfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(1500) NOT NULL,
  `uploaded_file` varchar(100) NOT NULL,
  `company_id` bigint NOT NULL,
  `document_type_id` bigint DEFAULT NULL,
  `vector_indexed` tinyint(1) NOT NULL,
  `codename` varchar(1500) DEFAULT NULL,
  `type` varchar(30) NOT NULL,
  `uploaded_by_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_companyfile_company_id_e278b4dd_fk_granter_company_id` (`company_id`),
  KEY `granter_companyfile_document_type_id_5ceadfe3_fk_granter_d` (`document_type_id`),
  KEY `granter_companyfile_uploaded_by_id_442c2144_fk_granter_p` (`uploaded_by_id`),
  CONSTRAINT `granter_companyfile_company_id_e278b4dd_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_companyfile_document_type_id_5ceadfe3_fk_granter_d` FOREIGN KEY (`document_type_id`) REFERENCES `granter_doctype` (`id`),
  CONSTRAINT `granter_companyfile_uploaded_by_id_442c2144_fk_granter_p` FOREIGN KEY (`uploaded_by_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_companymemory`
--

DROP TABLE IF EXISTS `granter_companymemory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_companymemory` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `content` longtext NOT NULL,
  `vector_indexed` tinyint(1) NOT NULL,
  `company_id` bigint NOT NULL,
  `created_by_id` bigint DEFAULT NULL,
  `type` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_companymemory_company_id_1649f842_fk_granter_company_id` (`company_id`),
  KEY `granter_companymemor_created_by_id_627bba35_fk_granter_p` (`created_by_id`),
  CONSTRAINT `granter_companymemor_created_by_id_627bba35_fk_granter_p` FOREIGN KEY (`created_by_id`) REFERENCES `granter_profile` (`id`),
  CONSTRAINT `granter_companymemory_company_id_1649f842_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_consortium`
--

DROP TABLE IF EXISTS `granter_consortium`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_consortium` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `opportunity_id` bigint NOT NULL,
  `project_description` longtext,
  `state` varchar(30) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_consortium_opportunity_id_f321d531_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_consortium_opportunity_id_f321d531_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_consortiumpartner`
--

DROP TABLE IF EXISTS `granter_consortiumpartner`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_consortiumpartner` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `partner_description` longtext,
  `company_id` bigint NOT NULL,
  `consortium_id` bigint NOT NULL,
  `partner_type_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_consortiumpa_company_id_13a72d88_fk_granter_c` (`company_id`),
  KEY `granter_consortiumpa_consortium_id_c667f18f_fk_granter_c` (`consortium_id`),
  KEY `granter_consortiumpa_partner_type_id_1069b08a_fk_granter_c` (`partner_type_id`),
  CONSTRAINT `granter_consortiumpa_company_id_13a72d88_fk_granter_c` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_consortiumpa_consortium_id_c667f18f_fk_granter_c` FOREIGN KEY (`consortium_id`) REFERENCES `granter_consortium` (`id`),
  CONSTRAINT `granter_consortiumpa_partner_type_id_1069b08a_fk_granter_c` FOREIGN KEY (`partner_type_id`) REFERENCES `granter_consortiumpartnertype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_consortiumpartnertype`
--

DROP TABLE IF EXISTS `granter_consortiumpartnertype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_consortiumpartnertype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `codename` varchar(60) NOT NULL,
  `description` longtext,
  `description_en` longtext,
  `description_pt` longtext,
  `title` varchar(100) NOT NULL,
  `title_en` varchar(100) DEFAULT NULL,
  `title_pt` varchar(100) DEFAULT NULL,
  `type` varchar(50) NOT NULL,
  `description_es` longtext,
  `description_it` longtext,
  `description_pl` longtext,
  `title_es` varchar(100) DEFAULT NULL,
  `title_it` varchar(100) DEFAULT NULL,
  `title_pl` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codename` (`codename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_consortiumpartnertype_consortium`
--

DROP TABLE IF EXISTS `granter_consortiumpartnertype_consortium`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_consortiumpartnertype_consortium` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `consortiumpartnertype_id` bigint NOT NULL,
  `consortium_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_consortiumpartne_consortiumpartnertype_id_a66088e1_uniq` (`consortiumpartnertype_id`,`consortium_id`),
  KEY `granter_consortiumpa_consortium_id_9843551d_fk_granter_c` (`consortium_id`),
  CONSTRAINT `granter_consortiumpa_consortium_id_9843551d_fk_granter_c` FOREIGN KEY (`consortium_id`) REFERENCES `granter_consortium` (`id`),
  CONSTRAINT `granter_consortiumpa_consortiumpartnertyp_1bc288b1_fk_granter_c` FOREIGN KEY (`consortiumpartnertype_id`) REFERENCES `granter_consortiumpartnertype` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_doctype`
--

DROP TABLE IF EXISTS `granter_doctype`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_doctype` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext,
  `help_text` longtext,
  `description_en` longtext,
  `description_pt` longtext,
  `help_text_en` longtext,
  `help_text_pt` longtext,
  `name_en` varchar(100) DEFAULT NULL,
  `name_pt` varchar(100) DEFAULT NULL,
  `upload_required` tinyint(1) NOT NULL,
  `description_es` longtext,
  `description_it` longtext,
  `description_pl` longtext,
  `help_text_es` longtext,
  `help_text_it` longtext,
  `help_text_pl` longtext,
  `name_es` varchar(100) DEFAULT NULL,
  `name_it` varchar(100) DEFAULT NULL,
  `name_pl` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_doctype_opportunity`
--

DROP TABLE IF EXISTS `granter_doctype_opportunity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_doctype_opportunity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `doctype_id` bigint NOT NULL,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_doctype_opportun_doctype_id_opportunity_i_4cd5221c_uniq` (`doctype_id`,`opportunity_id`),
  KEY `granter_doctype_oppo_opportunity_id_bcdb2e21_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_doctype_oppo_doctype_id_d657ebb5_fk_granter_d` FOREIGN KEY (`doctype_id`) REFERENCES `granter_doctype` (`id`),
  CONSTRAINT `granter_doctype_oppo_opportunity_id_bcdb2e21_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_eligibilitycriteria`
--

DROP TABLE IF EXISTS `granter_eligibilitycriteria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_eligibilitycriteria` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` longtext NOT NULL,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_opportunityc_opportunity_id_0bac18a9_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_opportunityc_opportunity_id_0bac18a9_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=278 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_eligibilitycriteriatranslations`
--

DROP TABLE IF EXISTS `granter_eligibilitycriteriatranslations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_eligibilitycriteriatranslations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `title` varchar(255) NOT NULL,
  `title_en` varchar(255) DEFAULT NULL,
  `title_pt` varchar(255) DEFAULT NULL,
  `description` longtext NOT NULL,
  `description_en` longtext,
  `description_pt` longtext,
  `eligibility_criteria_id` bigint NOT NULL,
  `description_es` longtext,
  `description_it` longtext,
  `description_pl` longtext,
  `title_es` varchar(255) DEFAULT NULL,
  `title_it` varchar(255) DEFAULT NULL,
  `title_pl` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `eligibility_criteria_id` (`eligibility_criteria_id`),
  CONSTRAINT `granter_eligibilityc_eligibility_criteria_4b5538b7_fk_granter_e` FOREIGN KEY (`eligibility_criteria_id`) REFERENCES `granter_eligibilitycriteria` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=197 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_eligibilityquestion`
--

DROP TABLE IF EXISTS `granter_eligibilityquestion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_eligibilityquestion` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title` longtext NOT NULL,
  `help_text` longtext,
  `state` varchar(30) NOT NULL,
  `company_id` bigint NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_eligibilityq_company_id_1e26737e_fk_granter_c` (`company_id`),
  CONSTRAINT `granter_eligibilityq_company_id_1e26737e_fk_granter_c` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_evaluator`
--

DROP TABLE IF EXISTS `granter_evaluator`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_evaluator` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(150) NOT NULL,
  `codename` varchar(60) NOT NULL,
  `calculation_formula` longtext,
  `state` varchar(30) NOT NULL,
  `scale` varchar(30) NOT NULL,
  `language` varchar(30) NOT NULL,
  `use_assistant_id` tinyint(1) NOT NULL,
  `extra_prompt` longtext,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codename` (`codename`),
  KEY `granter_evaluator_opportunity_id_3ba86cb4_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_evaluator_opportunity_id_3ba86cb4_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_evaluator_evaluator_profiles`
--

DROP TABLE IF EXISTS `granter_evaluator_evaluator_profiles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_evaluator_evaluator_profiles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `evaluator_id` bigint NOT NULL,
  `profile_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_evaluator_evalua_evaluator_id_profile_id_26d615b3_uniq` (`evaluator_id`,`profile_id`),
  KEY `granter_evaluator_ev_profile_id_f5cf5a94_fk_granter_p` (`profile_id`),
  CONSTRAINT `granter_evaluator_ev_evaluator_id_dd75ed8c_fk_granter_e` FOREIGN KEY (`evaluator_id`) REFERENCES `granter_evaluator` (`id`),
  CONSTRAINT `granter_evaluator_ev_profile_id_f5cf5a94_fk_granter_p` FOREIGN KEY (`profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_evaluatorgroup`
--

DROP TABLE IF EXISTS `granter_evaluatorgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_evaluatorgroup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `codename` varchar(100) NOT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codename` (`codename`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_evaluatorgroup_evaluators`
--

DROP TABLE IF EXISTS `granter_evaluatorgroup_evaluators`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_evaluatorgroup_evaluators` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `evaluatorgroup_id` bigint NOT NULL,
  `evaluator_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_evaluatorgroup_e_evaluatorgroup_id_evalua_07dabb4d_uniq` (`evaluatorgroup_id`,`evaluator_id`),
  KEY `granter_evaluatorgro_evaluator_id_3df1a4d4_fk_granter_e` (`evaluator_id`),
  CONSTRAINT `granter_evaluatorgro_evaluator_id_3df1a4d4_fk_granter_e` FOREIGN KEY (`evaluator_id`) REFERENCES `granter_evaluator` (`id`),
  CONSTRAINT `granter_evaluatorgro_evaluatorgroup_id_d5a5744f_fk_granter_e` FOREIGN KEY (`evaluatorgroup_id`) REFERENCES `granter_evaluatorgroup` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_evaluatorgrouptranslations`
--

DROP TABLE IF EXISTS `granter_evaluatorgrouptranslations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_evaluatorgrouptranslations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `title_en` varchar(100) DEFAULT NULL,
  `title_pt` varchar(100) DEFAULT NULL,
  `evaluator_group_id` bigint NOT NULL,
  `title_es` varchar(100) DEFAULT NULL,
  `title_it` varchar(100) DEFAULT NULL,
  `title_pl` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `evaluator_group_id` (`evaluator_group_id`),
  CONSTRAINT `granter_evaluatorgro_evaluator_group_id_385476ef_fk_granter_e` FOREIGN KEY (`evaluator_group_id`) REFERENCES `granter_evaluatorgroup` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_evaluatorreview`
--

DROP TABLE IF EXISTS `granter_evaluatorreview`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_evaluatorreview` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `title` varchar(150) DEFAULT NULL,
  `codename` varchar(250) DEFAULT NULL,
  `reviewed` tinyint(1) NOT NULL,
  `type` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `application_id` bigint NOT NULL,
  `application_output_id` bigint DEFAULT NULL,
  `evaluator_id` bigint NOT NULL,
  `evaluator_group_id` bigint DEFAULT NULL,
  `updated_profile_id` bigint DEFAULT NULL,
  `curated_details` longtext,
  `curated_value` varchar(25) DEFAULT NULL,
  `generated_details` longtext,
  `generated_value` varchar(25) DEFAULT NULL,
  `occurrence` longtext,
  PRIMARY KEY (`id`),
  KEY `granter_evaluatorrev_application_id_2ddec759_fk_granter_a` (`application_id`),
  KEY `granter_evaluatorrev_application_output_i_25c58888_fk_granter_a` (`application_output_id`),
  KEY `granter_evaluatorrev_evaluator_id_c716a93e_fk_granter_e` (`evaluator_id`),
  KEY `granter_evaluatorrev_evaluator_group_id_c6069b5d_fk_granter_e` (`evaluator_group_id`),
  KEY `granter_evaluatorrev_updated_profile_id_0fbea28e_fk_granter_p` (`updated_profile_id`),
  CONSTRAINT `granter_evaluatorrev_application_id_2ddec759_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_evaluatorrev_application_output_i_25c58888_fk_granter_a` FOREIGN KEY (`application_output_id`) REFERENCES `granter_applicationoutput` (`id`),
  CONSTRAINT `granter_evaluatorrev_evaluator_group_id_c6069b5d_fk_granter_e` FOREIGN KEY (`evaluator_group_id`) REFERENCES `granter_evaluatorgroup` (`id`),
  CONSTRAINT `granter_evaluatorrev_evaluator_id_c716a93e_fk_granter_e` FOREIGN KEY (`evaluator_id`) REFERENCES `granter_evaluator` (`id`),
  CONSTRAINT `granter_evaluatorrev_updated_profile_id_0fbea28e_fk_granter_p` FOREIGN KEY (`updated_profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_generalopportunityfile`
--

DROP TABLE IF EXISTS `granter_generalopportunityfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_generalopportunityfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `codename` varchar(500) DEFAULT NULL,
  `name` varchar(500) NOT NULL,
  `uploaded_file` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_generalopportunityfile_opportunities`
--

DROP TABLE IF EXISTS `granter_generalopportunityfile_opportunities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_generalopportunityfile_opportunities` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `generalopportunityfile_id` bigint NOT NULL,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_generalopportuni_generalopportunityfile_i_3f91c4cc_uniq` (`generalopportunityfile_id`,`opportunity_id`),
  KEY `granter_generaloppor_opportunity_id_ff1803f9_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_generaloppor_generalopportunityfi_d25fa7a3_fk_granter_g` FOREIGN KEY (`generalopportunityfile_id`) REFERENCES `granter_generalopportunityfile` (`id`),
  CONSTRAINT `granter_generaloppor_opportunity_id_ff1803f9_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_invoice`
--

DROP TABLE IF EXISTS `granter_invoice`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_invoice` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `issued_date` date NOT NULL,
  `due_date` date NOT NULL,
  `vat` decimal(10,2) NOT NULL,
  `description` longtext NOT NULL,
  `customer_name` varchar(150) NOT NULL,
  `customer_email` varchar(254) NOT NULL,
  `address` longtext NOT NULL,
  `post_code` varchar(10) NOT NULL,
  `city` varchar(50) NOT NULL,
  `country` varchar(50) NOT NULL,
  `tax_id` varchar(50) NOT NULL,
  `application_id` bigint DEFAULT NULL,
  `company_id` bigint NOT NULL,
  `subscription_id` bigint DEFAULT NULL,
  `invoice_link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_invoice_application_id_d1e351aa_fk_granter_a` (`application_id`),
  KEY `granter_invoice_company_id_f39393ec_fk_granter_company_id` (`company_id`),
  KEY `granter_invoice_subscription_id_8b7d9c3c_fk_granter_s` (`subscription_id`),
  CONSTRAINT `granter_invoice_application_id_d1e351aa_fk_granter_a` FOREIGN KEY (`application_id`) REFERENCES `granter_application` (`id`),
  CONSTRAINT `granter_invoice_company_id_f39393ec_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_invoice_subscription_id_8b7d9c3c_fk_granter_s` FOREIGN KEY (`subscription_id`) REFERENCES `granter_subscription` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_match`
--

DROP TABLE IF EXISTS `granter_match`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_match` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `result` varchar(30) NOT NULL,
  `details` varchar(2000) DEFAULT NULL,
  `company_id` bigint NOT NULL,
  `opportunity_id` bigint NOT NULL,
  `hidden_by_expert` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_match_company_id_cd5d64ac_fk_granter_company_id` (`company_id`),
  KEY `granter_match_opportunity_id_52220b3f_fk_granter_opportunity_id` (`opportunity_id`),
  CONSTRAINT `granter_match_company_id_cd5d64ac_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_match_opportunity_id_52220b3f_fk_granter_opportunity_id` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_matchcheck`
--

DROP TABLE IF EXISTS `granter_matchcheck`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_matchcheck` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `project_summary` longtext,
  `fundamentation` longtext,
  `type` varchar(30) NOT NULL,
  `result` varchar(10) NOT NULL,
  `chat_conversation_id` bigint DEFAULT NULL,
  `eligibility_criteria_id` bigint DEFAULT NULL,
  `eligibility_question_id` bigint DEFAULT NULL,
  `match_group_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_matchcheck_eligibility_question_116718a8_fk_granter_e` (`eligibility_question_id`),
  KEY `granter_matchcheck_match_group_id_05389739_fk_granter_m` (`match_group_id`),
  KEY `granter_matchcheck_chat_conversation_id_787bb4e2_fk_granter_c` (`chat_conversation_id`),
  KEY `granter_matchcheck_eligibility_criteria_f55f3c98_fk_granter_e` (`eligibility_criteria_id`),
  CONSTRAINT `granter_matchcheck_chat_conversation_id_787bb4e2_fk_granter_c` FOREIGN KEY (`chat_conversation_id`) REFERENCES `granter_chatconversation` (`id`),
  CONSTRAINT `granter_matchcheck_eligibility_criteria_f55f3c98_fk_granter_e` FOREIGN KEY (`eligibility_criteria_id`) REFERENCES `granter_eligibilitycriteria` (`id`),
  CONSTRAINT `granter_matchcheck_eligibility_question_116718a8_fk_granter_e` FOREIGN KEY (`eligibility_question_id`) REFERENCES `granter_eligibilityquestion` (`id`),
  CONSTRAINT `granter_matchcheck_match_group_id_05389739_fk_granter_m` FOREIGN KEY (`match_group_id`) REFERENCES `granter_matchgroup` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_matchgroup`
--

DROP TABLE IF EXISTS `granter_matchgroup`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_matchgroup` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `status` varchar(30) NOT NULL,
  `fundamentation` longtext,
  `company_id` bigint NOT NULL,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_matchgroup_company_id_df07c150_fk_granter_company_id` (`company_id`),
  KEY `granter_matchgroup_opportunity_id_89333ad9_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_matchgroup_company_id_df07c150_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_matchgroup_opportunity_id_89333ad9_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_notificationpreference`
--

DROP TABLE IF EXISTS `granter_notificationpreference`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_notificationpreference` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `newsletter` tinyint(1) NOT NULL,
  `new_opportunity` tinyint(1) NOT NULL,
  `profile_id` bigint NOT NULL,
  `opportunity_plan` tinyint(1) NOT NULL,
  `opportunity_push` tinyint(1) NOT NULL,
  `application_reminder` tinyint(1) NOT NULL,
  `opportunity_plan_has_prompt` tinyint(1) NOT NULL,
  `new_match` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_notificationpreference_profile_id_7653e776_uniq` (`profile_id`),
  CONSTRAINT `granter_notification_profile_id_7653e776_fk_granter_p` FOREIGN KEY (`profile_id`) REFERENCES `granter_profile` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_opportunity`
--

DROP TABLE IF EXISTS `granter_opportunity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_opportunity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(30) NOT NULL,
  `codename` varchar(100) NOT NULL,
  `state` varchar(30) NOT NULL,
  `name` varchar(350) NOT NULL,
  `fe_value` varchar(50) NOT NULL,
  `url` varchar(1000) NOT NULL,
  `description` longtext,
  `cover_image` varchar(100) NOT NULL,
  `upfront_fee` varchar(250) DEFAULT NULL,
  `force_closing_soon` tinyint(1) NOT NULL,
  `assistant_id` varchar(100) DEFAULT NULL,
  `last_email_reminder` varchar(30) DEFAULT NULL,
  `prep_time` varchar(50) NOT NULL,
  `location` varchar(30) NOT NULL,
  `last_email_push` datetime(6) DEFAULT NULL,
  `free_applications` tinyint(1) NOT NULL,
  `internal_submission` tinyint(1) NOT NULL,
  `small_cover_image` varchar(100) DEFAULT NULL,
  `crawler_data_id` varchar(150) DEFAULT NULL,
  `expected_success_rate` smallint DEFAULT NULL,
  `success_fee` varchar(250) DEFAULT NULL,
  `difficulty_level` varchar(30) NOT NULL,
  `eligibility_criteria` longtext,
  `eligible_expenses` longtext,
  `financial_information` longtext,
  `financing_rate` double DEFAULT NULL,
  `project_duration_months` smallint DEFAULT NULL,
  `project_max_value` int unsigned DEFAULT NULL,
  `project_min_value` int unsigned DEFAULT NULL,
  `admissible_projects` longtext,
  `form_questions` longtext,
  `currency` varchar(10) NOT NULL,
  `difficulty_level_fundamentation` longtext,
  `tags_fundamentation` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codename` (`codename`),
  CONSTRAINT `granter_opportunity_chk_1` CHECK ((`project_max_value` >= 0)),
  CONSTRAINT `granter_opportunity_chk_2` CHECK ((`project_min_value` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=388 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_opportunityfile`
--

DROP TABLE IF EXISTS `granter_opportunityfile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_opportunityfile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `name` varchar(1500) NOT NULL,
  `uploaded_file` varchar(1500) NOT NULL,
  `vector_indexed` tinyint(1) NOT NULL,
  `opportunity_id` bigint NOT NULL,
  `codename` varchar(1500) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_opportunityf_opportunity_id_43ea4ab5_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_opportunityf_opportunity_id_43ea4ab5_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_opportunitytracker`
--

DROP TABLE IF EXISTS `granter_opportunitytracker`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_opportunitytracker` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `crawler_type` varchar(100) NOT NULL,
  `data_id` varchar(150) DEFAULT NULL,
  `last_fetch_data` json DEFAULT NULL,
  `opportunity_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opportunity_id` (`opportunity_id`),
  CONSTRAINT `granter_opportunityt_opportunity_id_b43785ef_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_opportunitytranslations`
--

DROP TABLE IF EXISTS `granter_opportunitytranslations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_opportunitytranslations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `description` longtext,
  `description_en` longtext,
  `description_pt` longtext,
  `admissible_projects` longtext,
  `admissible_projects_en` longtext,
  `admissible_projects_pt` longtext,
  `eligible_expenses` longtext,
  `eligible_expenses_en` longtext,
  `eligible_expenses_pt` longtext,
  `financial_information` longtext,
  `financial_information_en` longtext,
  `financial_information_pt` longtext,
  `eligibility_criteria` longtext,
  `eligibility_criteria_en` longtext,
  `eligibility_criteria_pt` longtext,
  `opportunity_id` bigint NOT NULL,
  `admissible_projects_es` longtext,
  `admissible_projects_it` longtext,
  `admissible_projects_pl` longtext,
  `description_es` longtext,
  `description_it` longtext,
  `description_pl` longtext,
  `eligibility_criteria_es` longtext,
  `eligibility_criteria_it` longtext,
  `eligibility_criteria_pl` longtext,
  `eligible_expenses_es` longtext,
  `eligible_expenses_it` longtext,
  `eligible_expenses_pl` longtext,
  `financial_information_es` longtext,
  `financial_information_it` longtext,
  `financial_information_pl` longtext,
  `fe_value` varchar(50) NOT NULL,
  `fe_value_en` varchar(50) DEFAULT NULL,
  `fe_value_es` varchar(50) DEFAULT NULL,
  `fe_value_it` varchar(50) DEFAULT NULL,
  `fe_value_pl` varchar(50) DEFAULT NULL,
  `fe_value_pt` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `opportunity_id` (`opportunity_id`),
  CONSTRAINT `granter_opportunityt_opportunity_id_abe04aa5_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_plannedopportunity`
--

DROP TABLE IF EXISTS `granter_plannedopportunity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_plannedopportunity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `last_email_reminder` varchar(30) DEFAULT NULL,
  `company_id` bigint NOT NULL,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_plannedoppor_company_id_bb177060_fk_granter_c` (`company_id`),
  KEY `granter_plannedoppor_opportunity_id_99a7a098_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_plannedoppor_company_id_bb177060_fk_granter_c` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_plannedoppor_opportunity_id_99a7a098_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_profile`
--

DROP TABLE IF EXISTS `granter_profile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_profile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `is_admin` tinyint(1) NOT NULL,
  `type` varchar(30) NOT NULL,
  `state` varchar(30) NOT NULL,
  `language` varchar(10) NOT NULL,
  `avatar` varchar(100) NOT NULL,
  `user_id` int NOT NULL,
  `profile_referral_id` bigint DEFAULT NULL,
  `referral_code` varchar(50) DEFAULT NULL,
  `is_evaluator` tinyint(1) NOT NULL,
  `whitelabel_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  UNIQUE KEY `referral_code` (`referral_code`),
  KEY `granter_profile_profile_referral_id_880881fd_fk_granter_p` (`profile_referral_id`),
  KEY `granter_profile_whitelabel_id_55e3fa0a_fk_granter_whitelabel_id` (`whitelabel_id`),
  CONSTRAINT `granter_profile_profile_referral_id_880881fd_fk_granter_p` FOREIGN KEY (`profile_referral_id`) REFERENCES `granter_profile` (`id`),
  CONSTRAINT `granter_profile_user_id_1a24f76f_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `granter_profile_whitelabel_id_55e3fa0a_fk_granter_whitelabel_id` FOREIGN KEY (`whitelabel_id`) REFERENCES `granter_whitelabel` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_question`
--

DROP TABLE IF EXISTS `granter_question`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_question` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `codename` varchar(60) NOT NULL,
  `type` varchar(30) NOT NULL,
  `title` varchar(200) NOT NULL,
  `title_en` varchar(200) DEFAULT NULL,
  `title_pt` varchar(200) DEFAULT NULL,
  `help_text` longtext,
  `help_text_en` longtext,
  `help_text_pt` longtext,
  `max_length` int unsigned DEFAULT NULL,
  `options` json DEFAULT NULL,
  `placeholder` longtext,
  `placeholder_en` longtext,
  `placeholder_pt` longtext,
  `options_en` json DEFAULT NULL,
  `options_pt` json DEFAULT NULL,
  `help_text_es` longtext,
  `help_text_it` longtext,
  `help_text_pl` longtext,
  `options_es` json DEFAULT NULL,
  `options_it` json DEFAULT NULL,
  `options_pl` json DEFAULT NULL,
  `placeholder_es` longtext,
  `placeholder_it` longtext,
  `placeholder_pl` longtext,
  `title_es` varchar(200) DEFAULT NULL,
  `title_it` varchar(200) DEFAULT NULL,
  `title_pl` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `codename` (`codename`),
  CONSTRAINT `granter_question_chk_1` CHECK ((`max_length` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_question_opportunity`
--

DROP TABLE IF EXISTS `granter_question_opportunity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_question_opportunity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question_id` bigint NOT NULL,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_question_opportu_question_id_opportunity__82f34945_uniq` (`question_id`,`opportunity_id`),
  KEY `granter_question_opp_opportunity_id_9abdb4c8_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_question_opp_opportunity_id_9abdb4c8_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`),
  CONSTRAINT `granter_question_opp_question_id_26ac2856_fk_granter_q` FOREIGN KEY (`question_id`) REFERENCES `granter_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_question_partner_type`
--

DROP TABLE IF EXISTS `granter_question_partner_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_question_partner_type` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `question_id` bigint NOT NULL,
  `consortiumpartnertype_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_question_partner_question_id_consortiumpa_2e778444_uniq` (`question_id`,`consortiumpartnertype_id`),
  KEY `granter_question_par_consortiumpartnertyp_2dc3b57f_fk_granter_c` (`consortiumpartnertype_id`),
  CONSTRAINT `granter_question_par_consortiumpartnertyp_2dc3b57f_fk_granter_c` FOREIGN KEY (`consortiumpartnertype_id`) REFERENCES `granter_consortiumpartnertype` (`id`),
  CONSTRAINT `granter_question_par_question_id_ae584836_fk_granter_q` FOREIGN KEY (`question_id`) REFERENCES `granter_question` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_subscription`
--

DROP TABLE IF EXISTS `granter_subscription`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_subscription` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `tier` varchar(100) NOT NULL,
  `owner_company_id` bigint DEFAULT NULL,
  `invoice_period` varchar(100) NOT NULL,
  `is_invoicing` tinyint(1) NOT NULL,
  `per_invoice_amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `owner_company_id` (`owner_company_id`),
  CONSTRAINT `granter_subscription_owner_company_id_8e288168_fk_granter_c` FOREIGN KEY (`owner_company_id`) REFERENCES `granter_company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_tag`
--

DROP TABLE IF EXISTS `granter_tag`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_tag` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `type` varchar(30) NOT NULL,
  `location` varchar(30) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_tag_company`
--

DROP TABLE IF EXISTS `granter_tag_company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_tag_company` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_id` bigint NOT NULL,
  `company_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_tag_company_tag_id_company_id_1f7299a0_uniq` (`tag_id`,`company_id`),
  KEY `granter_tag_company_company_id_e7786a72_fk_granter_company_id` (`company_id`),
  CONSTRAINT `granter_tag_company_company_id_e7786a72_fk_granter_company_id` FOREIGN KEY (`company_id`) REFERENCES `granter_company` (`id`),
  CONSTRAINT `granter_tag_company_tag_id_7e606dc8_fk_granter_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `granter_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_tag_opportunity`
--

DROP TABLE IF EXISTS `granter_tag_opportunity`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_tag_opportunity` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tag_id` bigint NOT NULL,
  `opportunity_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `granter_tag_opportunity_tag_id_opportunity_id_c74acda5_uniq` (`tag_id`,`opportunity_id`),
  KEY `granter_tag_opportun_opportunity_id_971c0ded_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_tag_opportun_opportunity_id_971c0ded_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`),
  CONSTRAINT `granter_tag_opportunity_tag_id_77cf20dd_fk_granter_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `granter_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=727 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_tagtranslations`
--

DROP TABLE IF EXISTS `granter_tagtranslations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_tagtranslations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `title_en` varchar(100) DEFAULT NULL,
  `title_pt` varchar(100) DEFAULT NULL,
  `tag_id` bigint NOT NULL,
  `title_es` varchar(100) DEFAULT NULL,
  `title_it` varchar(100) DEFAULT NULL,
  `title_pl` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag_id` (`tag_id`),
  CONSTRAINT `granter_tagtranslations_tag_id_8c6cb530_fk_granter_tag_id` FOREIGN KEY (`tag_id`) REFERENCES `granter_tag` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=100 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_timeline`
--

DROP TABLE IF EXISTS `granter_timeline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_timeline` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `type` varchar(30) NOT NULL,
  `title` varchar(100) NOT NULL,
  `description` varchar(500) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `time` time(6) DEFAULT NULL,
  `opportunity_id` bigint NOT NULL,
  `time_diff` varchar(30) DEFAULT NULL,
  `is_prediction` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `granter_timeline_opportunity_id_f7daba4f_fk_granter_o` (`opportunity_id`),
  CONSTRAINT `granter_timeline_opportunity_id_f7daba4f_fk_granter_o` FOREIGN KEY (`opportunity_id`) REFERENCES `granter_opportunity` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1304 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_timelinetranslations`
--

DROP TABLE IF EXISTS `granter_timelinetranslations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_timelinetranslations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `title` varchar(100) NOT NULL,
  `title_en` varchar(100) DEFAULT NULL,
  `title_pt` varchar(100) DEFAULT NULL,
  `description` varchar(500) DEFAULT NULL,
  `description_en` varchar(500) DEFAULT NULL,
  `description_pt` varchar(500) DEFAULT NULL,
  `time_diff` varchar(30) DEFAULT NULL,
  `time_diff_en` varchar(30) DEFAULT NULL,
  `time_diff_pt` varchar(30) DEFAULT NULL,
  `timeline_id` bigint NOT NULL,
  `description_es` varchar(500) DEFAULT NULL,
  `description_it` varchar(500) DEFAULT NULL,
  `description_pl` varchar(500) DEFAULT NULL,
  `time_diff_es` varchar(30) DEFAULT NULL,
  `time_diff_it` varchar(30) DEFAULT NULL,
  `time_diff_pl` varchar(30) DEFAULT NULL,
  `title_es` varchar(100) DEFAULT NULL,
  `title_it` varchar(100) DEFAULT NULL,
  `title_pl` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `timeline_id` (`timeline_id`),
  CONSTRAINT `granter_timelinetran_timeline_id_e332c159_fk_granter_t` FOREIGN KEY (`timeline_id`) REFERENCES `granter_timeline` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `granter_whitelabel`
--

DROP TABLE IF EXISTS `granter_whitelabel`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `granter_whitelabel` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `logo_image` varchar(100) DEFAULT NULL,
  `name` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `impersonate_impersonationlog`
--

DROP TABLE IF EXISTS `impersonate_impersonationlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `impersonate_impersonationlog` (
  `id` int NOT NULL AUTO_INCREMENT,
  `session_key` varchar(40) NOT NULL,
  `session_started_at` datetime(6) DEFAULT NULL,
  `session_ended_at` datetime(6) DEFAULT NULL,
  `impersonating_id` int NOT NULL,
  `impersonator_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `impersonate_imperson_impersonating_id_afd114fc_fk_auth_user` (`impersonating_id`),
  KEY `impersonate_imperson_impersonator_id_1ecfe8ce_fk_auth_user` (`impersonator_id`),
  CONSTRAINT `impersonate_imperson_impersonating_id_afd114fc_fk_auth_user` FOREIGN KEY (`impersonating_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `impersonate_imperson_impersonator_id_1ecfe8ce_fk_auth_user` FOREIGN KEY (`impersonator_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_association`
--

DROP TABLE IF EXISTS `social_auth_association`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_association` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `handle` varchar(255) NOT NULL,
  `secret` varchar(255) NOT NULL,
  `issued` int NOT NULL,
  `lifetime` int NOT NULL,
  `assoc_type` varchar(64) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_association_server_url_handle_078befa2_uniq` (`server_url`,`handle`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_code`
--

DROP TABLE IF EXISTS `social_auth_code`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_code` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `email` varchar(254) NOT NULL,
  `code` varchar(32) NOT NULL,
  `verified` tinyint(1) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_code_email_code_801b2d02_uniq` (`email`,`code`),
  KEY `social_auth_code_code_a2393167` (`code`),
  KEY `social_auth_code_timestamp_176b341f` (`timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_nonce`
--

DROP TABLE IF EXISTS `social_auth_nonce`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_nonce` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `server_url` varchar(255) NOT NULL,
  `timestamp` int NOT NULL,
  `salt` varchar(65) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_nonce_server_url_timestamp_salt_f6284463_uniq` (`server_url`,`timestamp`,`salt`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_partial`
--

DROP TABLE IF EXISTS `social_auth_partial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_partial` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `token` varchar(32) NOT NULL,
  `next_step` smallint unsigned NOT NULL,
  `backend` varchar(32) NOT NULL,
  `timestamp` datetime(6) NOT NULL,
  `data` json NOT NULL DEFAULT (_utf8mb3'{}'),
  PRIMARY KEY (`id`),
  KEY `social_auth_partial_token_3017fea3` (`token`),
  KEY `social_auth_partial_timestamp_50f2119f` (`timestamp`),
  CONSTRAINT `social_auth_partial_chk_1` CHECK ((`next_step` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `social_auth_usersocialauth`
--

DROP TABLE IF EXISTS `social_auth_usersocialauth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `social_auth_usersocialauth` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `provider` varchar(32) NOT NULL,
  `uid` varchar(255) NOT NULL,
  `user_id` int NOT NULL,
  `created` datetime(6) NOT NULL,
  `modified` datetime(6) NOT NULL,
  `extra_data` json NOT NULL DEFAULT (_utf8mb3'{}'),
  PRIMARY KEY (`id`),
  UNIQUE KEY `social_auth_usersocialauth_provider_uid_e6b5e668_uniq` (`provider`,`uid`),
  KEY `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` (`user_id`),
  KEY `social_auth_usersocialauth_uid_796e51dc` (`uid`),
  CONSTRAINT `social_auth_usersocialauth_user_id_17d28448_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-08-01 12:19:52
