DROP DATABASE IF EXISTS cyber_security;
CREATE DATABASE cyber_security;
USE cyber_security;

DROP TABLE IF EXISTS key_id_type;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE key_id_type (
  key_id int NOT NULL AUTO_INCREMENT,
  key_type varchar(5) NOT NULL,
  key_size int NOT NULL,
  PRIMARY KEY (key_id)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS aes;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE aes (
  key_id int NOT NULL,
  key_value varchar(300) NOT NULL,
  UNIQUE KEY key_id_UNIQUE (key_id),
  CONSTRAINT aes_key_id FOREIGN KEY (key_id) REFERENCES key_id_type (key_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS `rsa`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rsa` (
  `key_id` int NOT NULL,
  `public_key` varchar(4500) NOT NULL,
  `private_key` varchar(4500) NOT NULL,
  UNIQUE KEY `key_id_UNIQUE` (`key_id`),
  KEY `key_id_idx` (`key_id`),
  CONSTRAINT `rsa_key_id` FOREIGN KEY (`key_id`) REFERENCES `key_id_type` (`key_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
