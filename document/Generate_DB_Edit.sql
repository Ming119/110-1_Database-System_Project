CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(64) NOT NULL,
  `username` varchar(32) NOT NULL,
  `password_hash` varchar(1024) NOT NULL,
  `first_name` varchar(32) NOT NULL,
  `last_name` varchar(32) NOT NULL,
  `role` varchar(16) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `last_login` datetime DEFAULT NULL,
  `create_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `username` (`username`)
);

CREATE TABLE `admin` (
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `admin_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);

CREATE TABLE `staff` (
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `staff_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);

CREATE TABLE `customer` (
  `user_id` int(11) NOT NULL,
  `confirm` tinyint(1) NOT NULL,
  `DOB` date NOT NULL,
  PRIMARY KEY (`user_id`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
);

CREATE TABLE `customer_address` (
  `address_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `country` varchar(8) NOT NULL,
  `city` varchar(32) NOT NULL,
  `address` varchar(255) NOT NULL,
  `postal_code` varchar(8) NOT NULL,
  `telephone` varchar(16) NOT NULL,
  PRIMARY KEY (`address_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `customer_address_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `customer` (`user_id`)
);

CREATE TABLE `product_category` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(63) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `create_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`category_id`),
  UNIQUE KEY `name` (`name`)
);

CREATE TABLE `product` (
  `product_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_id` int(11) NOT NULL,
  `discount_code` varchar(8) DEFAULT NULL,
  `name` varchar(63) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `image_url` varchar(255) NOT NULL,
  `price` float NOT NULL,
  `quantity` int(11) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `create_at` datetime NOT NULL,
  `modified_at` datetime NOT NULL,
  PRIMARY KEY (`product_id`),
  KEY `category_id` (`category_id`),
  KEY `discount_code` (`discount_code`),
  CONSTRAINT `product_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `product_category` (`category_id`),
  CONSTRAINT `product_ibfk_2` FOREIGN KEY (`discount_code`) REFERENCES `product_discount` (`discount_code`)
);

CREATE TABLE `shopping_cart` (
  `customer_id` int(11) NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`customer_id`),
  CONSTRAINT `shopping_cart_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`user_id`)
);

CREATE TABLE `cart_item` (
  `cart_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`cart_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `cart_item_ibfk_1` FOREIGN KEY (`cart_id`) REFERENCES `shopping_cart` (`customer_id`),
  CONSTRAINT `cart_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
);

CREATE TABLE `discount` (
  `discount_code` varchar(8) NOT NULL,
  `name` varchar(64) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `type` varchar(255) NOT NULL,
  `start_at` datetime DEFAULT NULL,
  `end_at` datetime DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  `modified_at` datetime DEFAULT NULL,
  PRIMARY KEY (`discount_code`)
);

CREATE TABLE `product_discount` (
  `discount_code` varchar(8) NOT NULL,
  `discountPercentage` float NOT NULL,
  PRIMARY KEY (`discount_code`),
  CONSTRAINT `product_discount_ibfk_1` FOREIGN KEY (`discount_code`) REFERENCES `discount` (`discount_code`)
);

CREATE TABLE `order_discount` (
  `discount_code` varchar(8) NOT NULL,
  `discountPercentage` float NOT NULL,
  `atLeastAmount` float NOT NULL,
  PRIMARY KEY (`discount_code`),
  CONSTRAINT `order_discount_ibfk_1` FOREIGN KEY (`discount_code`) REFERENCES `discount` (`discount_code`)
);

CREATE TABLE `shipping_discount` (
  `discount_code` varchar(8) NOT NULL,
  `atLeastAmount` float NOT NULL,
  PRIMARY KEY (`discount_code`),
  CONSTRAINT `shipping_discount_ibfk_1` FOREIGN KEY (`discount_code`) REFERENCES `discount` (`discount_code`)
);

CREATE TABLE `order` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) NOT NULL,
  `address_id` int(11) NOT NULL,
  `order_discount` varchar(8) DEFAULT NULL,
  `amount` float NOT NULL,
  `shippingFee` int(11) NOT NULL,
  `shipDate` datetime DEFAULT NULL,
  `status` int(11) NOT NULL,
  `payment_type` varchar(8) DEFAULT NULL,
  `provider` varchar(64) DEFAULT NULL,
  `account_no` int(11) DEFAULT NULL,
  `create_at` datetime DEFAULT NULL,
  PRIMARY KEY (`order_id`),
  KEY `customer_id` (`customer_id`),
  KEY `address_id` (`address_id`),
  KEY `order_discount` (`order_discount`),
  CONSTRAINT `order_ibfk_1` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`user_id`),
  CONSTRAINT `order_ibfk_2` FOREIGN KEY (`address_id`) REFERENCES `customer_address` (`address_id`),
  CONSTRAINT `order_ibfk_3` FOREIGN KEY (`order_discount`) REFERENCES `order_discount` (`discount_code`)
);

CREATE TABLE `order_item` (
  `order_id` int(11) NOT NULL,
  `product_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `amount` float NOT NULL,
  PRIMARY KEY (`order_id`,`product_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `order_item_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `order` (`order_id`),
  CONSTRAINT `order_item_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
);

CREATE TABLE `comments` (
  `cid` int(11) NOT NULL AUTO_INCREMENT,
  `product_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `comment` varchar(256) DEFAULT NULL,
  `rating` int(11) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`cid`),
  KEY `product_id` (`product_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `comments_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`),
  CONSTRAINT `comments_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `customer` (`user_id`)
);



LOCK TABLES `user` WRITE;
INSERT INTO `user` VALUES 
(1,'customer@domain.com','customer','$2b$12$86o2ARAS7a/982/Vksb2.Oc4aPObD.Uzeh2CKajta/EQfNf/AJ9b2','customer','customer','customer',1,NULL,'2021-12-15 19:41:33','2021-12-15 19:41:33'),
(2,'staff@domain.com','staff','$2b$12$QI6ybzmt0xMaeo9HK9vlmuHxKetMprdoXSZgIg/zXis52N197SOZa','staff','staff','staff',1,NULL,'2021-12-15 19:41:33','2021-12-15 19:41:33'),
(3,'admin@domain.com','admin','$2b$12$m2k2uVAgMoGKo4HuTS8d2OgqNjVqITntc5XZyKCi3FS.1sFT33Tzi','admin','admin','admin',1,NULL,'2021-12-15 19:41:34','2021-12-15 19:41:34');
UNLOCK TABLES;

LOCK TABLES `admin` WRITE;
INSERT INTO `admin` VALUES (3);
UNLOCK TABLES;

LOCK TABLES `staff` WRITE;
INSERT INTO `staff` VALUES (2);
UNLOCK TABLES;

LOCK TABLES `customer` WRITE;
INSERT INTO `customer` VALUES (1,0,'2021-12-15');
UNLOCK TABLES;

LOCK TABLES `product_category` WRITE;
INSERT INTO `product_category` VALUES 
(1,'Shoes','Shoes',1,'2021-12-15 19:41:34','2021-12-15 19:41:34'),
(2,'Watch','Watch',1,'2021-12-15 19:41:34','2021-12-15 19:41:34');
UNLOCK TABLES;

LOCK TABLES `product` WRITE;
INSERT INTO `product` VALUES 
(1,1,NULL,'Shoe','Shoe description','https://api.lorem.space/image/shoes?w=304&h=225',100,1,1,'2021-12-15 20:28:56','2021-12-15 20:28:56'),
(2,2,NULL,'Watch','Watch description','https://api.lorem.space/image/watch?w=304&h=225',100,1,1,'2021-12-15 20:28:56','2021-12-15 20:28:56');
UNLOCK TABLES;