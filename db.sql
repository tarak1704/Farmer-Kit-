/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 5.5.5-10.1.13-MariaDB : Database - e-agri
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`e-agri` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `e-agri`;

/*Table structure for table `buyer_chatting` */

DROP TABLE IF EXISTS `buyer_chatting`;

CREATE TABLE `buyer_chatting` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `i_id` int(10) DEFAULT NULL,
  `f_id` int(10) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  `femail` varchar(100) DEFAULT NULL,
  `iemail` varchar(100) DEFAULT NULL,
  `msg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Table structure for table `buyers` */

DROP TABLE IF EXISTS `buyers`;

CREATE TABLE `buyers` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Table structure for table `crop_data` */

DROP TABLE IF EXISTS `crop_data`;

CREATE TABLE `crop_data` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `ctype` varchar(100) DEFAULT NULL,
  `cyear` int(100) DEFAULT NULL,
  `area` int(100) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `investment` int(100) DEFAULT NULL,
  `profit` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Table structure for table `crop_prices` */

DROP TABLE IF EXISTS `crop_prices`;

CREATE TABLE `crop_prices` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `crop` varchar(100) DEFAULT NULL,
  `price` int(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;

/*Table structure for table `crop_selling` */

DROP TABLE IF EXISTS `crop_selling`;

CREATE TABLE `crop_selling` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `fname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `quantity` int(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Table structure for table `farmer` */

DROP TABLE IF EXISTS `farmer`;

CREATE TABLE `farmer` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*Table structure for table `fund_chatting` */

DROP TABLE IF EXISTS `fund_chatting`;

CREATE TABLE `fund_chatting` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `i_id` int(10) DEFAULT NULL,
  `f_id` int(10) DEFAULT NULL,
  `user_type` varchar(100) DEFAULT NULL,
  `femail` varchar(100) DEFAULT NULL,
  `iemail` varchar(100) DEFAULT NULL,
  `msg` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Table structure for table `investment_data` */

DROP TABLE IF EXISTS `investment_data`;

CREATE TABLE `investment_data` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `fid` int(10) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `yeild` varchar(100) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `femail` varchar(100) DEFAULT NULL,
  `fno` varchar(100) DEFAULT NULL,
  `faddr` varchar(100) DEFAULT NULL,
  `iname` varchar(100) DEFAULT NULL,
  `iemail` varchar(100) DEFAULT NULL,
  `ino` varchar(100) DEFAULT NULL,
  `iaddr` varchar(100) DEFAULT NULL,
  `area` int(100) DEFAULT NULL,
  `money` varchar(100) DEFAULT NULL,
  `share` varchar(100) DEFAULT NULL,
  `e_money` varchar(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Table structure for table `investor` */

DROP TABLE IF EXISTS `investor`;

CREATE TABLE `investor` (
  `id` int(100) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pwd` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Table structure for table `make_funds` */

DROP TABLE IF EXISTS `make_funds`;

CREATE TABLE `make_funds` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `cname` varchar(100) DEFAULT NULL,
  `crop_price` int(10) DEFAULT NULL,
  `yeild` varchar(100) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `area` int(100) DEFAULT NULL,
  `money` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `share` varchar(100) DEFAULT NULL,
  `e_money` varchar(100) DEFAULT '0',
  `status` varchar(100) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;

/*Table structure for table `payments` */

DROP TABLE IF EXISTS `payments`;

CREATE TABLE `payments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `farmer_email` varchar(100) NOT NULL,
  `farmer_name` varchar(100) NOT NULL,
  `crop_name` varchar(100) NOT NULL,
  `crop_qty` int(11) NOT NULL,
  `amount` int(11) NOT NULL,
  `created_at` varchar(100) DEFAULT NULL,
  `buyer_email` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Table structure for table `profit_data` */

DROP TABLE IF EXISTS `profit_data`;

CREATE TABLE `profit_data` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `fid` int(100) DEFAULT NULL,
  `i_id` int(100) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `yeild` varchar(100) DEFAULT NULL,
  `area` int(100) DEFAULT NULL,
  `money` varchar(100) DEFAULT NULL,
  `share` varchar(100) DEFAULT NULL,
  `i_money` varchar(100) DEFAULT NULL,
  `profit` varchar(100) DEFAULT NULL,
  `final_amount` varchar(100) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `femail` varchar(100) DEFAULT NULL,
  `iname` varchar(100) DEFAULT NULL,
  `iemail` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `selling_buying` */

DROP TABLE IF EXISTS `selling_buying`;

CREATE TABLE `selling_buying` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `sid` int(10) DEFAULT NULL,
  `fname` varchar(100) DEFAULT NULL,
  `femail` varchar(100) DEFAULT NULL,
  `bname` varchar(100) DEFAULT NULL,
  `bemail` varchar(100) DEFAULT NULL,
  `pno` varchar(100) DEFAULT NULL,
  `addr` varchar(100) DEFAULT NULL,
  `cname` varchar(100) DEFAULT NULL,
  `quantity` int(100) DEFAULT NULL,
  `buyer_need` int(100) DEFAULT NULL,
  `status` varchar(100) DEFAULT 'pending',
  `msg` varchar(100) DEFAULT NULL,
  `total_amt` int(11) NOT NULL,
  `action` varchar(100) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
