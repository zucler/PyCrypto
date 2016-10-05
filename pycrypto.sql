-- MySQL dump 10.13  Distrib 5.7.9, for osx10.9 (x86_64)
--
-- Host: localhost    Database: pycrypto
-- ------------------------------------------------------
-- Server version	5.7.11

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
-- Table structure for table `BUY`
--

DROP TABLE IF EXISTS `BUY`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `BUY` (
  `EXCHANGEID` int(11) NOT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `PAIRID` int(11) NOT NULL,
  `RATE` float NOT NULL,
  `VOLUME` float NOT NULL,
  KEY `ID_idx` (`EXCHANGEID`),
  KEY `ID_idx1` (`PAIRID`),
  CONSTRAINT `FK_BUY1` FOREIGN KEY (`EXCHANGEID`) REFERENCES `EXCHANGE` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_BUY2` FOREIGN KEY (`PAIRID`) REFERENCES `PAIR` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `BUY`
--

LOCK TABLES `BUY` WRITE;
/*!40000 ALTER TABLE `BUY` DISABLE KEYS */;
/*!40000 ALTER TABLE `BUY` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EXCHANGE`
--

DROP TABLE IF EXISTS `EXCHANGE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EXCHANGE` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(255) NOT NULL,
  `SELLPATH` varchar(255) NOT NULL DEFAULT '-',
  `BUYPATH` varchar(255) NOT NULL DEFAULT '-',
  `SELLVOLUMEPATH` varchar(255) NOT NULL DEFAULT '-',
  `BUYVOLUMEPATH` varchar(255) NOT NULL DEFAULT '-',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EXCHANGE`
--

LOCK TABLES `EXCHANGE` WRITE;
/*!40000 ALTER TABLE `EXCHANGE` DISABLE KEYS */;
INSERT INTO `EXCHANGE` VALUES (1,'Coinsbank','*.sell[*].rate','*.buy[*].rate','*.sell[*].amount','*.buy[*].amount'),(2,'BTC-E','*.asks[*][0]','*.bids[*][0]','*.asks[*][1]','*.bids[*][1]'),(3,'Poloniex','asks[*][0]','bids[*][0]','asks[*][1]','bids[*][1]'),(4,'Bitfinex','asks[*].price','bids[*].price','asks[*].amount','bids[*].amount'),(5,'Livecoin','asks[*][0]','bids[*][0]','asks[*][1]','bids[*][1]'),(6,'Bittrex','result.sell[*].Rate','result.buy[*].Rate','result.sell[*].Quantity','result.buy[*].Quantity'),(7,'HitBTC','asks[*][0]','bids[*][0]','asks[*][1]','bids[*][1]');
/*!40000 ALTER TABLE `EXCHANGE` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `EXCHANGEPAIR`
--

DROP TABLE IF EXISTS `EXCHANGEPAIR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `EXCHANGEPAIR` (
  `EXCHANGEID` int(11) NOT NULL,
  `PAIRID` int(11) NOT NULL,
  `APIURL` varchar(255) NOT NULL DEFAULT '-',
  `ENABLED` tinyint(1) DEFAULT '1',
  UNIQUE KEY `APIURL_UNIQUE` (`APIURL`),
  KEY `ID_idx` (`PAIRID`),
  KEY `FK_EXCHANGEPAIR1_idx` (`EXCHANGEID`),
  CONSTRAINT `FK_EXCHANGEPAIR1` FOREIGN KEY (`EXCHANGEID`) REFERENCES `EXCHANGE` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_EXCHANGEPAIR2` FOREIGN KEY (`PAIRID`) REFERENCES `PAIR` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `EXCHANGEPAIR`
--

LOCK TABLES `EXCHANGEPAIR` WRITE;
/*!40000 ALTER TABLE `EXCHANGEPAIR` DISABLE KEYS */;
INSERT INTO `EXCHANGEPAIR` VALUES (4,1,'https://api.bitfinex.com/v1/book/LTCBTC',1),(7,1,'https://api.hitbtc.com/api/1/public/LTCBTC/orderbook?format_price=number&format_amount=number',1),(5,1,'https://api.livecoin.net/exchange/order_book?currencyPair=LTC/BTC',1),(1,1,'https://bit-x.com/api/public/orderBook?pair=LTCBTC',0),(6,1,'https://bittrex.com/api/v1.1/public/getorderbook?market=BTC-LTC&type=both&depth=50',1),(2,1,'https://btc-e.com/api/3/depth/ltc_btc',1),(3,1,'https://poloniex.com/public?command=returnOrderBook&currencyPair=BTC_LTC&depth=50',1);
/*!40000 ALTER TABLE `EXCHANGEPAIR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `PAIR`
--

DROP TABLE IF EXISTS `PAIR`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `PAIR` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `NAME` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `ID_UNIQUE` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `PAIR`
--

LOCK TABLES `PAIR` WRITE;
/*!40000 ALTER TABLE `PAIR` DISABLE KEYS */;
INSERT INTO `PAIR` VALUES (1,'LTCBTC');
/*!40000 ALTER TABLE `PAIR` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `SELL`
--

DROP TABLE IF EXISTS `SELL`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `SELL` (
  `EXCHANGEID` int(11) NOT NULL,
  `DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `PAIRID` int(11) NOT NULL,
  `RATE` float NOT NULL,
  `VOLUME` float NOT NULL,
  KEY `ID_idx` (`EXCHANGEID`),
  KEY `ID_idx1` (`PAIRID`),
  CONSTRAINT `FK_SELL1` FOREIGN KEY (`EXCHANGEID`) REFERENCES `EXCHANGE` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `FK_SELL2` FOREIGN KEY (`PAIRID`) REFERENCES `PAIR` (`ID`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `SELL`
--

LOCK TABLES `SELL` WRITE;
/*!40000 ALTER TABLE `SELL` DISABLE KEYS */;
/*!40000 ALTER TABLE `SELL` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `TRADE`
--

DROP TABLE IF EXISTS `TRADE`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `TRADE` (
  `DATE` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `FROMEX` int(11) NOT NULL,
  `TOEX` int(11) NOT NULL,
  `BUYPRICE` float NOT NULL,
  `SELLPRICE` float NOT NULL,
  `VOLUME` float NOT NULL,
  `PAIRID` int(11) NOT NULL,
  PRIMARY KEY (`DATE`),
  UNIQUE KEY `DATE_UNIQUE` (`DATE`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `TRADE`
--

LOCK TABLES `TRADE` WRITE;
/*!40000 ALTER TABLE `TRADE` DISABLE KEYS */;
/*!40000 ALTER TABLE `TRADE` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-10-05 19:22:02
