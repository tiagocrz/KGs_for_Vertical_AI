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

-- CHECK 
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

-- CHECK 
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

-- CHECK 
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