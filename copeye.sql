-- phpMyAdmin SQL Dump
-- version 5.1.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 27, 2022 at 11:29 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `copeye`
--

-- --------------------------------------------------------

--
-- Table structure for table `citizen`
--

CREATE TABLE `citizen` (
  `cid` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(20) NOT NULL,
  `age` int(3) NOT NULL,
  `address` text NOT NULL,
  `wanted` tinyint(1) DEFAULT 0,
  `lost` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `citizen`
--

INSERT INTO `citizen` (`cid`, `name`, `age`, `address`, `wanted`, `lost`) VALUES
(7, 'Alia', 27, 'Mumbai', 0, 0),
(8, 'Emma', 40, 'UK', 0, 0),
(9, 'Selena', 45, 'Washington', 0, 0),
(10, 'Priyanka', 40, 'Delhi', 0, 0),
(11, 'Devansh', 15, 'SRE', 0, 0),
(12, 'Kartik', 20, 'Ind', 0, 0),
(13, 'Kartik', 21, 'Vaishali', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `criminal`
--

CREATE TABLE `criminal` (
  `crid` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(20) NOT NULL,
  `caseid` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `criminal`
--

INSERT INTO `criminal` (`crid`, `name`, `caseid`) VALUES
(5, 'Tony', '12'),
(8, 'Kartik', '101'),
(9, 'selena', '1'),
(10, 'priyanka', '2'),
(11, 'alia', '3'),
(12, 'chris', '4'),
(13, 'taylor', '5'),
(14, 'rdj', '6'),
(15, 'elizabeth', '7'),
(16, 'scar', '8'),
(17, 'harry', '9'),
(18, 'emma', '10'),
(19, 'Johny', '1021'),
(20, 'kdba', '10292'),
(21, 'adkabdkbka', '10192');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `username` varchar(25) NOT NULL,
  `email` text NOT NULL,
  `uid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`username`, `email`, `uid`) VALUES
('Kartik Chauhan', 'kartik@123.com', 39),
('devansh', 'devanshchauhan8077@gmail.com', 40),
('Kartik', 'abc@g.com', 41);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `citizen`
--
ALTER TABLE `citizen`
  ADD PRIMARY KEY (`cid`),
  ADD UNIQUE KEY `cid` (`cid`);

--
-- Indexes for table `criminal`
--
ALTER TABLE `criminal`
  ADD PRIMARY KEY (`crid`),
  ADD UNIQUE KEY `crid` (`crid`),
  ADD UNIQUE KEY `caseid` (`caseid`) USING HASH;

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `email` (`email`(50));

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `citizen`
--
ALTER TABLE `citizen`
  MODIFY `cid` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `criminal`
--
ALTER TABLE `criminal`
  MODIFY `crid` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `uid` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=42;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
