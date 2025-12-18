-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 18, 2025 at 05:13 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `dms`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `password` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `password`, `email`) VALUES
(1, '123', 'admin.01@admin.dms.com'),
(2, '456', 'admin.02@admin.dms.com');

-- --------------------------------------------------------

--
-- Table structure for table `appointment`
--

CREATE TABLE `appointment` (
  `app_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `date` date DEFAULT NULL,
  `time` varchar(20) DEFAULT '20:00 - 22:00',
  `confirmation` tinyint(1) NOT NULL DEFAULT 0,
  `checked` tinyint(1) NOT NULL DEFAULT 0,
  `appointment_type` enum('in-person','telemedicine') DEFAULT 'in-person',
  `zoom_meeting_link` varchar(500) DEFAULT NULL,
  `zoom_meeting_id` varchar(100) DEFAULT NULL,
  `zoom_password` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointment`
--

INSERT INTO `appointment` (`app_id`, `d_id`, `p_id`, `date`, `time`, `confirmation`, `checked`, `appointment_type`, `zoom_meeting_link`, `zoom_meeting_id`, `zoom_password`) VALUES
(1, 1, 1, '2025-11-12', '16:15', 1, 1, 'telemedicine', NULL, NULL, NULL),
(5, 2, 1, '2025-09-26', '18:00:00', 0, 0, 'in-person', NULL, NULL, NULL),
(6, 5, 1, '2025-11-23', '16:30:00', 0, 0, 'in-person', NULL, NULL, NULL),
(7, 4, 1, '2025-09-18', '17:30:00', 0, 0, 'in-person', NULL, NULL, NULL),
(8, 1, 1, '2025-09-19', '17:30:00', 2, 0, 'in-person', NULL, NULL, NULL),
(9, 1, 1, '2025-09-22', '15:00:00', 3, 0, 'in-person', NULL, NULL, NULL),
(10, 1, 1, '2025-09-25', '18:30:00', 2, 0, 'in-person', NULL, NULL, NULL),
(11, 1, 4, '2025-09-23', '18:00:00', 1, 0, 'in-person', NULL, NULL, NULL),
(12, 1, 5, '2025-09-22', '18:20:00', 1, 0, 'in-person', NULL, NULL, NULL),
(13, 1, 3, '2025-09-02', '18:20:00', 3, 0, 'in-person', NULL, NULL, NULL),
(14, 2, 1, '2025-09-30', '15:22:00', 0, 0, 'in-person', NULL, NULL, NULL),
(15, 10, 1, '2025-10-03', '17:15:00', 1, 1, 'in-person', NULL, NULL, NULL),
(55, 2, 8, '2025-12-13', '12:00 PM', 1, 0, 'telemedicine', 'https://us05web.zoom.us/j/89193412155?pwd=p28lEgcHZa6WWnsPbmIgoep3bfTka5.1', '89193412155', '3EVVt5'),
(56, 1, 8, NULL, '20:00 - 22:00', 1, 0, 'telemedicine', NULL, NULL, NULL),
(57, 3, 10, '2025-12-15', '10:00 AM', 1, 0, 'telemedicine', 'https://us05web.zoom.us/j/82913424012?pwd=5fHdx60Cjtjs0dg6apuEmmWu61aatY.1', '82913424012', '36QN1j');

-- --------------------------------------------------------

--
-- Table structure for table `card_registry`
--

CREATE TABLE `card_registry` (
  `card_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `card_number` varchar(16) NOT NULL,
  `cvv` varchar(4) NOT NULL,
  `expiration_date` varchar(5) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `card_registry`
--

INSERT INTO `card_registry` (`card_id`, `p_id`, `card_number`, `cvv`, `expiration_date`) VALUES
(1, 8, '3437542423532443', '111', '12/26');

-- --------------------------------------------------------

--
-- Table structure for table `diet`
--

CREATE TABLE `diet` (
  `diet_id` int(11) NOT NULL,
  `age_range` varchar(11) NOT NULL,
  `female_plan` varchar(255) NOT NULL,
  `male_plan` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `diet`
--

INSERT INTO `diet` (`diet_id`, `age_range`, `female_plan`, `male_plan`) VALUES
(1, '10 to 17', 'Carbohydrates: 50%    \nProteins: 20%    \nFats: 25%    \nVitamins & Minerals: 5%\n\nFocus on complex carbs (whole grains), lean proteins (eggs, chicken), healthy fats (nuts, olive oil), fresh fruits, and vegetables. Ensure calcium and iron intake.', 'Carbohydrates: 60% \r\nProteins: 35% \r\nFats: 30% \r\nVitamins & Minerals: 10%  \r\n\r\nSupport growth and activity levels. Include whole grains, lean meats, dairy, eggs, and vegetables.'),
(2, '18 to 20', 'Carbohydrates: 45% \r\nProteins: 25%\r\nFats: 25%\r\nVitamins & Minerals: 5%\r\n\r\nBalance energy needs with high-protein meals. Include leafy greens, legumes, oats, dairy, and low-sugar fruits.', 'Carbohydrates: 50%\nProteins: 25%\nFats: 20%\nVitamins & Minerals: 5%\n\nSupport growth and activity levels. Include whole grains, lean meats, dairy, eggs, and vegetables.'),
(3, '21 to 25', 'Carbohydrates: 45%\r\nProteins: 30%\r\nFats: 20%\r\nVitamins & Minerals: 5%. \r\n\r\nFocus on muscle maintenance, avoid refined carbs. Include fish, tofu, quinoa, berries, and vitamin C-rich foods.', 'Carbohydrates: 50%\r\nProteins: 30%\r\nFats: 15%\r\nVitamins & Minerals: 5%\r\n\r\nEnhance muscle development and metabolism. Include high-protein sources, oats, nuts, green vegetables.'),
(4, '26 to 30', 'Carbohydrates: 40%\r\nProteins: 30%\r\nFats: 25%\r\nVitamins & Minerals: 5%. \r\n\r\nIncrease fiber-rich vegetables, avocado, almonds. Stay hydrated and manage stress-related cravings.', 'Carbohydrates: 45%\r\nProteins: 25% \r\nFats: 25% \r\nVitamins & Minerals: 5%  \r\n\r\nSupport energy levels and prevent insulin resistance. Include whole grains, avocados, lean meats, and berries.'),
(5, '31 to 40', 'Carbohydrates: 40%\r\nProteins: 25%\r\nFats: 30%\r\nVitamins & Minerals: 5%\r\n\r\nSupport metabolism with lean meats, legumes, seeds, and omega-3-rich sources. Cut added sugars and processed food.', 'Carbohydrates: 45%\nProteins: 25%\nFats: 25%\nVitamins & Minerals: 5%\n\nSupport energy levels and prevent insulin resistance. Include whole grains, avocados, lean meats, and berries.'),
(6, '40 to 50', 'Carbohydrates: 35%\r\nProteins: 25%\r\nFats: 30%\r\nVitamins & Minerals: 10%\r\n\r\nManage hormonal changes with high-fiber foods, healthy fats, antioxidants, and low-GI carbs. Control sodium and cholesterol.', 'Carbohydrates: 40%\r\nProteins: 25%\r\nFats: 25%\r\nVitamins & Minerals: 10%\r\n\r\nControl cholesterol and maintain metabolic health. Use low-GI carbs, omega-3s, and dark leafy greens.'),
(7, '50 to 60', 'Carbohydrates: 35%\r\nProteins: 25%\r\nFats: 25%\r\nVitamins & Minerals: 15%\r\n\r\nPrioritize heart-healthy foods: oily fish, legumes, whole grains. Increase calcium, magnesium, and vitamin D.', 'Carbohydrates: 35%\r\nProteins: 30%\r\nFats: 20%\r\nVitamins & Minerals: 15%\r\n\r\nReduce risk of cardiovascular issues. Emphasize plant-based fats, fiber, lean protein, and reduce sodium.'),
(8, '60 to 70', 'Carbohydrates: 30%\r\nProteins: 25%\r\nFats: 25%\r\nVitamins & Minerals: 20%\r\n\r\nImprove immunity with citrus fruits, nuts, and leafy greens. Monitor blood pressure and kidney-friendly diet.', 'Carbohydrates: 30%\r\nProteins: 30%\r\nFats: 20%\r\nVitamins & Minerals: 20%\r\n\r\nPreserve muscle and organ function. Incorporate beans, eggs, yogurt, green vegetables, and hydration.'),
(9, '70+', 'Carbohydrates: 30%\r\nProteins: 30%\r\nFats: 20%\r\nVitamins & Minerals: 20%\r\n\r\nSupport muscle retention with more protein, focus on soft-texture foods, and ensure hydration and multivitamin intake.', 'Carbohydrates: 30%\r\nProteins: 30%\r\nFats: 15%\r\nVitamins & Minerals: 25%\r\n\r\nMaintain strength and manage blood sugar. Prioritize protein-rich soft foods, easy-to-digest carbs, and hydration with supplements if needed.');

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `d_id` int(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `domain_email` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `designation` varchar(255) DEFAULT NULL,
  `phone` varchar(11) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `area` varchar(100) DEFAULT NULL,
  `verified` tinyint(1) NOT NULL DEFAULT 0,
  `otp_code` varchar(6) DEFAULT NULL,
  `otp_expiry` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`d_id`, `password`, `email`, `domain_email`, `name`, `designation`, `phone`, `location`, `area`, `verified`, `otp_code`, `otp_expiry`) VALUES
(1, 'DMC', 'srar.74@gmail.com', 'srar.74@doctor.dms.com', 'Zabia Alazas', 'Deputy Chief Medical Officer, MBBS, CCD (BIRDEM)', '01711451495', 'OPD, BIRDEM General Hospital, Shahbag, Dhaka', 'Shahbag', 1, NULL, NULL),
(2, 'SSMC', 'imtiaz.69@gmail.com', 'imtiaz.69@doctor.dms.com', 'Imtiaz Faruk', 'Professor, MBBS, FCPS, FRCS (Glasgow)', '01819231809', 'Dhaka Medical College and Hospital, Secretariat Road, Central Shaheed Minar Area, Shahbag, Dhaka, Bangladesh', 'Shahbag', 1, NULL, NULL),
(3, 'RMC', 'afialabiba.79@gmail.com', 'afialabiba.79@doctor.dms.com', 'Afia Labiba', 'MBBS, FCPS, FRCS (Ed)', '01971451490', 'Samorita Hospital Limited\r\n89/1, Panthapath, Dhaka-1215, Bangladesh', 'Panthapath', 1, NULL, NULL),
(4, 'MMC', 'faruque@yahoo.com', '', 'Md Faruque Pathan', 'Professor, MBBS, MD (EM), FACE (USA)', '01777335056', 'BIRDEM,122 Kazi Nazrul Islam Avenue, Shahbagh, Dhaka 1000', 'Shahbag', 1, NULL, NULL),
(5, 'RMCH', 'motiur@gmail.com', '', 'Md. Motiur Rahman', 'Registrar (DM), MBBS, FCPS (Medicine), DEM (BIRDEM)', '01991674809', 'Square Provate Hospital, 18 Bir Uttam Qazi Nuruzzaman Sarak West, Panthapath, Dhaka 1205, Bangladesh', 'Panthapath', 1, NULL, NULL),
(6, 'SQUARE', 'pratik@yahoo.com', '', 'Pratik Dewan', 'Consultant (IME), MBBS, DEM, MD (Internal Medicine), BIRDEM Academy', '01752346567', 'Nafi Tower, Level-3 (2nd floor),\r\n53 Gulshan Avenue, Gulshan-1,\r\nDhaka- 1212', 'Gulshan', 1, NULL, NULL),
(7, '123', 'yan@gmail.com', '', 'Yan Ali', 'Senior Consultant, MBBS, MD (Diabetology), MD (Endocrinology), Fellow Newborn Medicine (Canada), MPH(NSU)', '01971451490', 'United Hospital Limited, Plot 15 Rd No 71, Gulshan, Dhaka 1212, Bangladesh', 'Gulshan', 1, NULL, NULL),
(8, 'mat216', 'hosan@gmail.com', '', 'Hosan Ali', NULL, NULL, NULL, NULL, 0, NULL, NULL),
(9, '123', 'admin.01@gmail.com', '', 'dsad', NULL, NULL, NULL, NULL, 0, NULL, NULL),
(10, '890', 'razia@gmail.com', '', 'Razia Akhter', 'Registrar, MBBS, FCPS (Medicine), DEM (BIRDEM)', '0187235210', 'Labaid Specialized Hospital,  House- 01, Road-04, Dhanmondi, Dhaka 1205, Bangladesh.', 'Dhanmondi', 1, NULL, NULL),
(11, 'xyz', 'xyz@gmail.com', 'xyz@doctor.dms.com', 'xyz', 'General Physician', NULL, NULL, NULL, 1, NULL, NULL),
(12, '333', 'adi333@gmail.com', 'adi333@doctor.dms.com', 'aditya333', 'General Physician', NULL, NULL, NULL, 0, NULL, NULL),
(13, 'scrypt:32768:8:1$j95SdhZfIVXeOCjd$e0de97356779ef4db97f4c6c5d8ad9abdceb0731b7244eedbebbd9c5886bd9b317b94e6a6842e90d22251d09cc073f80c114568439231c12db0f56daffbbbd17', 'adi213@gmail.com', 'adi213@doctor.dms.com', 'ADi111', 'General Physician', NULL, NULL, NULL, 0, NULL, NULL),
(14, 'scrypt:32768:8:1$iwIVJDFRxQQAgNaK$32a8d0077d9ee24b9db1595b8b97b55a335251e3b8fe36278630c9f8eac6503356c73d679c1683a1153a012acedee89b068109d3580040b7435bf4d1aa684cf6', 'adi313@gmail.com', 'adi313@doctor.dms.com', 'adi313', 'General Physician', NULL, NULL, NULL, 0, '592132', '2025-12-18 09:46:52'),
(17, 'scrypt:32768:8:1$Bl8jwc5hyNgrEKTg$1f69329f07b6bc04f99cd000afe6d17d1673e12b3aa2e06f53f0d7f7727659390633eb38330c76f7989db2b06bc4f2a4ba8b35182dd91d92d25ec9da65640d7c', 'brunoferandes18811@gmail.com', 'brunoferandes18811@doctor.dms.com', 'bruno', 'General Physician', NULL, NULL, NULL, 1, NULL, '2025-12-18 10:04:53');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_reviews`
--

CREATE TABLE `doctor_reviews` (
  `review_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL CHECK (`rating` between 1 and 5),
  `comment` text DEFAULT NULL,
  `review_date` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_reviews`
--

INSERT INTO `doctor_reviews` (`review_id`, `p_id`, `d_id`, `rating`, `comment`, `review_date`) VALUES
(3, 1, 2, 4, 'He was very friendly.', '2025-04-29 23:52:14'),
(4, 2, 1, 5, '', '2025-04-30 02:41:24'),
(5, 2, 2, 5, '', '2025-04-30 02:48:00'),
(7, 1, 1, 4, 'she was freidnly', '2025-05-03 22:27:16'),
(8, 1, 10, 5, 'Very friendly and listens to problem', '2025-05-01 13:50:27');

-- --------------------------------------------------------

--
-- Table structure for table `doctor_schedule`
--

CREATE TABLE `doctor_schedule` (
  `d_id` int(11) NOT NULL,
  `day1` varchar(255) DEFAULT NULL,
  `day2` varchar(255) DEFAULT NULL,
  `teleday` varchar(255) DEFAULT NULL,
  `day1_starttime` time(6) DEFAULT NULL,
  `day2_starttime` time(6) DEFAULT NULL,
  `teleday_starttime` time(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_schedule`
--

INSERT INTO `doctor_schedule` (`d_id`, `day1`, `day2`, `teleday`, `day1_starttime`, `day2_starttime`, `teleday_starttime`) VALUES
(1, 'Sunday', 'Tuesday', 'Saturday', '08:00:00.000000', '10:00:00.000000', '09:00:00.000000'),
(2, 'Sunday', 'Wednesday', 'Saturday', '09:00:00.000000', '10:00:00.000000', '11:00:00.000000'),
(3, 'Saturday', 'Sunday', 'Monday', '08:00:00.000000', '10:00:00.000000', '10:00:00.000000'),
(17, NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `doctor_slot`
--

CREATE TABLE `doctor_slot` (
  `slot_id` int(11) NOT NULL,
  `d_id` int(11) DEFAULT NULL,
  `day1slot1` tinyint(1) DEFAULT 0,
  `day1slot2` tinyint(1) DEFAULT 0,
  `day1slot3` tinyint(1) DEFAULT 0,
  `day1slot4` tinyint(1) DEFAULT 0,
  `day1slot5` tinyint(1) DEFAULT 0,
  `day1slot6` tinyint(1) DEFAULT 0,
  `day1slot7` tinyint(1) DEFAULT 0,
  `day1slot8` tinyint(1) DEFAULT 0,
  `day2slot1` tinyint(1) DEFAULT 0,
  `day2slot2` tinyint(1) DEFAULT 0,
  `day2slot3` tinyint(1) DEFAULT 0,
  `day2slot4` tinyint(1) DEFAULT 0,
  `day2slot5` tinyint(1) DEFAULT 0,
  `day2slot6` tinyint(1) DEFAULT 0,
  `day2slot7` tinyint(1) DEFAULT 0,
  `day2slot8` tinyint(1) DEFAULT 0,
  `teledayslot1` tinyint(1) DEFAULT 0,
  `teledayslot2` tinyint(1) DEFAULT 0,
  `teledayslot3` tinyint(1) DEFAULT 0,
  `teledayslot4` tinyint(1) DEFAULT 0,
  `teledayslot5` tinyint(1) DEFAULT 0,
  `teledayslot6` tinyint(1) DEFAULT 0,
  `teledayslot7` tinyint(1) DEFAULT 0,
  `teledayslot8` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor_slot`
--

INSERT INTO `doctor_slot` (`slot_id`, `d_id`, `day1slot1`, `day1slot2`, `day1slot3`, `day1slot4`, `day1slot5`, `day1slot6`, `day1slot7`, `day1slot8`, `day2slot1`, `day2slot2`, `day2slot3`, `day2slot4`, `day2slot5`, `day2slot6`, `day2slot7`, `day2slot8`, `teledayslot1`, `teledayslot2`, `teledayslot3`, `teledayslot4`, `teledayslot5`, `teledayslot6`, `teledayslot7`, `teledayslot8`) VALUES
(16, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0),
(18, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0),
(19, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `medicines`
--

CREATE TABLE `medicines` (
  `id` int(11) NOT NULL,
  `pharmacy_id` int(11) NOT NULL,
  `medicine_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  `price` decimal(10,2) DEFAULT NULL,
  `expiry_date` date DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `medicines`
--

INSERT INTO `medicines` (`id`, `pharmacy_id`, `medicine_name`, `quantity`, `price`, `expiry_date`, `created_at`, `updated_at`) VALUES
(1, 1, 'Paracetamol', 100, 20.00, '2024-12-31', '2025-04-19 12:50:25', '2025-04-30 13:03:05'),
(2, 1, 'Amoxicillin', 50, 110.00, '2024-10-15', '2025-04-19 12:50:25', '2025-04-20 19:36:28'),
(4, 2, 'Paracetamol', 20, 20.00, '2024-11-30', '2025-04-19 12:50:25', '2025-04-30 13:03:15'),
(6, 3, 'Cetirizine', 40, 8.99, '2025-03-10', '2025-04-19 12:50:25', '2025-04-19 12:50:25'),
(8, 2, 'Comet', 6, 40.00, '2026-07-19', '2025-04-19 17:10:52', '2025-04-19 17:10:52'),
(9, 1, 'Insuline', 2, 75.00, '2027-03-20', '2025-04-20 17:15:37', '2025-04-20 17:15:37'),
(10, 4, 'Napa', 10, 50.00, '2027-11-20', '2025-04-20 17:46:35', '2025-04-20 17:46:35'),
(11, 2, 'Insuline', 5, 350.00, '2027-04-21', '2025-04-21 15:50:39', '2025-04-21 15:50:39'),
(13, 6, 'paracetemol', 5, 20.00, '2027-04-25', '2025-04-25 07:25:12', '2025-04-25 07:25:12');

-- --------------------------------------------------------

--
-- Table structure for table `notices`
--

CREATE TABLE `notices` (
  `id` int(11) NOT NULL,
  `sender_id` int(11) DEFAULT NULL,
  `recipient_type` varchar(100) NOT NULL,
  `recipient_id` int(11) DEFAULT NULL,
  `message` text NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notices`
--

INSERT INTO `notices` (`id`, `sender_id`, `recipient_type`, `recipient_id`, `message`, `date`) VALUES
(3, 1, 'specific_patient', 1, 'Based on your last visit, a follow-up appointment is recommended within the next 7 days. Please schedule it at your earliest convenience.', '2025-05-14'),
(4, 1, 'both', NULL, 'Website will be closed for repair on 22/05/25.', '2025-05-14'),
(5, 1, 'doctor', 1, 'Mandatory Staff Meeting on Friday at 3 PM in Conference Room A.', '2025-05-14'),
(6, 1, 'specific_doctor', 1, 'you have a meeting tomorrow', '2025-05-15');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `p_id` int(11) DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `status` varchar(50) DEFAULT NULL,
  `delivery_address` text DEFAULT NULL,
  `payment_method` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`order_id`, `p_id`, `order_date`, `status`, `delivery_address`, `payment_method`) VALUES
(1, 6, '2025-04-29', 'pending', 'Joj Golli', 'cash'),
(2, 6, '2025-04-29', 'pending', 'joj golli', 'cash'),
(3, 6, '2025-04-29', 'pending', 'Joj Golli', 'cash'),
(4, 6, '2025-04-29', 'pending', 'Dhanmondi', 'online'),
(5, 6, '2025-04-29', 'responded', 'Mirpur', 'online'),
(6, 6, '2025-04-29', 'responded', 'DHANMODI', 'online'),
(7, 6, '2025-04-29', 'responded', 'Ctg', 'online'),
(8, 6, '2025-04-29', 'responded', 'Gazipur', 'online'),
(9, 6, '2025-04-30', 'pending', 'BanglaMotor', 'online'),
(10, 6, '2025-04-30', 'pending', '194, George Golli,Dhaka\n194', 'online'),
(11, 6, '2025-04-30', 'pending', 'Banglamotor', 'online'),
(12, 1, '2025-04-30', 'pending', 'Kolabagan', 'cash'),
(13, 1, '2025-04-30', 'responded', 'Mirpur', 'online'),
(14, 1, '2025-05-01', 'responded', 'Ctg2', 'cash'),
(15, 1, '2025-05-01', 'responded', 'ctg3', 'online'),
(16, 1, '2025-05-01', 'responded', 'Ctg4', 'cash'),
(17, 1, '2025-05-01', 'responded', 'ctg5', 'online'),
(18, 1, '2025-05-01', 'pending', '194,Hatirpool', 'cash'),
(19, 1, '2025-05-01', 'pending', 'Mirpur-10', 'online'),
(20, 6, '2025-05-03', 'pending', '194,Dhanmondi,Dhaka', 'cash'),
(21, 6, '2025-05-03', 'responded', 'Ctg7', 'online');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `medicine_name` varchar(255) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `medicine_name`, `quantity`, `price`) VALUES
(1, 1, 'Insuline', 1, 75.00),
(2, 2, 'paracetemol', 1, 20.00),
(3, 3, 'paracetemol', 1, 20.00),
(4, 4, 'Napa', 1, 50.00),
(5, 5, 'paracetemol', 1, 20.00),
(6, 6, 'paracetemol', 10, 20.00),
(7, 7, 'paracetemol', 5, 20.00),
(8, 8, 'paracetemol', 1, 20.00),
(9, 8, 'Amoxicillin', 1, 110.00),
(10, 9, 'Comet', 3, 40.00),
(11, 10, 'Comet', 3, 40.00),
(12, 11, 'Comet', 1, 40.00),
(13, 12, 'Comet', 1, 40.00),
(14, 13, 'Comet', 1, 40.00),
(15, 13, 'paracetemol', 2, 20.00),
(16, 14, 'Comet', 5, 40.00),
(17, 14, 'paracetemol', 8, 20.00),
(18, 15, 'Comet', 5, 40.00),
(19, 16, 'paracetemol', 2, 20.00),
(20, 16, 'Comet', 2, 40.00),
(21, 17, 'Insuline', 2, 75.00),
(22, 17, 'Comet', 3, 40.00),
(23, 18, 'Comet', 10, 40.00),
(24, 18, 'paracetemol', 2, 20.00),
(25, 19, 'Comet', 5, 40.00),
(26, 19, 'Insuline', 1, 350.00),
(27, 20, 'Comet', 1, 40.00),
(28, 20, 'paracetemol', 5, 20.00),
(29, 21, 'paracetemol', 1, 20.00);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `p_id` int(11) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `phone` varchar(25) DEFAULT NULL,
  `weight` decimal(5,2) DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `gl_b_breakfast` decimal(3,1) NOT NULL DEFAULT 0.0,
  `gl_a_breakfast` decimal(3,1) NOT NULL DEFAULT 0.0,
  `gl_b_lunch` decimal(3,1) NOT NULL DEFAULT 0.0,
  `gl_b_dinner` decimal(3,1) NOT NULL DEFAULT 0.0,
  `updated_on` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `followup_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`p_id`, `password`, `email`, `name`, `dob`, `phone`, `weight`, `gender`, `gl_b_breakfast`, `gl_a_breakfast`, `gl_b_lunch`, `gl_b_dinner`, `updated_on`, `followup_date`) VALUES
(1, 'patient', 'jakedms471@gmail.com', 'Sim Jake', '2002-11-15', '01991279286', 60.00, 'Male', 2.0, 20.0, 15.9, 7.0, '2025-12-11 12:32:11', NULL),
(2, '098', 'biswasangshu31@gmail.com', 'Angshu', '2001-02-13', '01713328283', 55.00, 'Male', 7.0, 8.0, 8.0, 7.0, '2025-12-12 11:41:07', NULL),
(3, 'na', 'nahianraidah065@gmail.com', 'nahian', '2002-06-13', '01714070157', 76.00, 'Female', 3.0, 6.0, 15.0, 30.0, '2025-12-04 16:20:08', NULL),
(4, '123', 'afialabiba.02@gmail.com', 'labiba', '1999-07-19', '01971451498', 76.00, 'Female', 6.7, 5.0, 10.0, 12.0, '2025-12-12 11:44:48', NULL),
(5, 'en30', 'jay@gmail.com', 'Jay', '1990-09-24', '01714070132', 100.00, 'Male', 6.0, 3.0, 2.0, 10.0, '2025-12-11 12:34:12', NULL),
(6, 'beckham', 'david@gmail.com', 'David', NULL, NULL, NULL, NULL, 0.0, 0.0, 0.0, 0.0, '2025-12-11 12:34:00', NULL),
(7, 'alice', 'alice@gmail.com', 'Alice', NULL, NULL, NULL, NULL, 0.0, 0.0, 0.0, 0.0, '2025-12-12 09:45:36', NULL),
(8, 'anir', 'aniruddha@gmail.com', 'Aniruddha', '2019-06-08', '0123131312413', 35.00, 'Male', 6.0, 7.0, 8.0, 7.0, '2025-12-12 12:41:09', NULL),
(9, '111', 'aditya111@gmail.com', 'Adi111', '2005-12-13', 'None', 88.00, 'Male', 6.0, 7.0, 8.0, 7.0, '2025-12-12 15:42:01', NULL),
(10, '123', 'adi123@gmail.com', 'Adi123', '2004-12-13', 'None', 77.00, 'Male', 7.0, 7.0, 6.0, 6.0, '2025-12-13 03:23:24', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `patient_notifications`
--

CREATE TABLE `patient_notifications` (
  `id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `message` varchar(255) NOT NULL,
  `app_id` int(11) DEFAULT NULL,
  `status` enum('unread','read','dismissed') DEFAULT 'unread',
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient_notifications`
--

INSERT INTO `patient_notifications` (`id`, `p_id`, `message`, `app_id`, `status`, `timestamp`) VALUES
(1, 1, 'Your appointment on 2024-09-23 at 16:30:00 has been Confirmed ✅', 6, 'dismissed', '2025-04-28 20:00:46'),
(2, 1, 'Your appointment on 2025-04-30 at 10.00  - 12.00  has been Confirmed ✅', 26, 'dismissed', '2025-04-28 21:08:29'),
(3, 1, 'Doctor requested to reschedule your appointment on 2025-05-06 at 10.00  - 12.00  🔁', 27, 'dismissed', '2025-04-28 21:10:38'),
(4, 1, 'Your appointment on 2025-05-05 at 17:00  - 19:00 has been Confirmed ✅', 28, 'dismissed', '2025-04-28 21:26:57'),
(5, 1, 'Your appointment on 2025-05-01 at 17:00  - 19:00  has been Confirmed ✅', 29, 'dismissed', '2025-04-28 21:26:59'),
(6, 1, 'Update on your appointment for 2025-05-05 at 17:00  - 19:00', 28, 'dismissed', '2025-04-28 21:29:05'),
(7, 1, 'Update on your appointment for 2025-05-01 at 17:00  - 19:00 ', 29, 'dismissed', '2025-04-28 21:29:09'),
(8, 1, 'Your appointment on 2025-05-02 at 10:00  - 12:00  has been Cancelled ❌', 30, 'dismissed', '2025-04-28 21:33:01'),
(9, 1, 'Your appointment on 2025-05-03 at 18:00  - 20:00  has been Confirmed ✅', 31, 'dismissed', '2025-04-28 21:33:28'),
(10, 4, 'Your appointment on 2025-05-07 at 10.00  - 12.00  has been Confirmed ✅', 32, 'dismissed', '2025-04-30 13:35:46'),
(11, 4, 'Doctor requested to reschedule your appointment on 2025-05-06 at 17:00  - 19:00  🔁', 33, 'dismissed', '2025-04-30 13:36:15'),
(12, 1, 'Your appointment on 2025-05-08 at 10.00  - 12.00  has been Cancelled ❌', 34, 'dismissed', '2025-05-01 14:04:04'),
(13, 1, 'Your appointment on 2025-05-09 at 10:00  - 12:00  has been Cancelled ❌', 36, 'dismissed', '2025-05-03 16:32:09'),
(14, 1, 'Your appointment on 2025-05-10 at 18:00  - 20:00  has been Confirmed ✅', 35, 'dismissed', '2025-05-03 16:32:43'),
(15, 5, 'Your appointment on 2025-05-07 at 10.00  - 12.00  has been Confirmed ✅', 37, 'dismissed', '2025-05-06 12:44:30'),
(16, 5, 'Doctor requested to reschedule your appointment on 2025-05-08 at 17:00  - 19:00  🔁', 38, 'dismissed', '2025-05-06 12:49:09'),
(17, 4, 'Your appointment on 2025-05-12 at 18.00  - 20.00  has been Confirmed ✅', 39, 'dismissed', '2025-05-06 12:53:59'),
(18, 5, 'Doctor requested to reschedule your appointment on 2025-05-13 at 10.00  - 12.00  🔁', 41, 'dismissed', '2025-05-06 13:03:54'),
(19, 1, 'Doctor requested to reschedule your appointment on 2025-05-13 at 10.00  - 12.00  🔁', 40, 'dismissed', '2025-05-06 13:03:59'),
(20, 5, 'Your appointment on 2025-05-16 at 20:00 - 22:00 has been Confirmed ✅', 81, 'dismissed', '2025-05-12 09:05:52'),
(21, 5, 'Update on your appointment for 2025-05-16 at 20:00 - 22:00', 81, 'dismissed', '2025-05-12 09:05:56'),
(22, 1, 'Update on your appointment for 2025-04-30 at 10.00  - 12.00 ', 26, 'dismissed', '2025-05-12 09:08:23'),
(23, 4, 'Update on your appointment for 2025-05-07 at 10.00  - 12.00 ', 32, 'dismissed', '2025-05-12 09:08:27'),
(24, 4, 'Update on your appointment for 2025-05-12 at 18.00  - 20.00 ', 39, 'dismissed', '2025-05-12 09:08:29'),
(25, 5, 'Update on your appointment for 2025-05-07 at 10.00  - 12.00 ', 37, 'dismissed', '2025-05-12 09:08:33'),
(26, 5, 'Doctor requested to reschedule your appointment on 2025-05-09 at 20:00 - 22:00 🔁', 73, 'dismissed', '2025-05-12 09:08:51'),
(27, 4, 'Your appointment on 2025-05-15 at 17:00  - 19:00  has been Confirmed ✅', 84, 'dismissed', '2025-05-12 09:12:09'),
(28, 4, 'Update on your appointment for 2025-05-15 at 17:00  - 19:00 ', 84, 'dismissed', '2025-05-12 09:12:13'),
(29, 4, 'Your appointment on 2025-05-19 at 17:00  - 19:00 has been Cancelled ❌', 85, 'dismissed', '2025-05-12 09:14:19'),
(30, 5, 'Your appointment on 2025-05-19 at 20:00 - 22:00 has been Confirmed ✅', 82, 'dismissed', '2025-05-12 09:21:51'),
(31, 5, 'Doctor requested to reschedule your appointment on 2025-05-15 at 17:00  - 19:00  🔁', 86, 'dismissed', '2025-05-12 09:22:00'),
(32, 1, 'Doctor requested to reschedule your appointment on 2025-05-19 at 20:00 - 22:00 🔁', 80, 'dismissed', '2025-05-12 09:24:35'),
(33, 4, 'Your appointment on 2025-05-12 at 20:00 - 22:00 has been Cancelled ❌', 77, 'dismissed', '2025-05-12 09:25:39'),
(34, 5, 'Your appointment on 2025-05-12 at 20:00 - 22:00 has been Confirmed ✅', 75, 'dismissed', '2025-05-12 09:31:35'),
(35, 5, 'Update on your appointment for 2025-05-12 at 20:00 - 22:00', 75, 'dismissed', '2025-05-12 09:31:39'),
(36, 1, 'Doctor requested to reschedule your appointment on 2025-05-19 at 20:00 - 22:00 🔁', 87, 'dismissed', '2025-05-12 15:04:55'),
(37, 5, 'Doctor requested to reschedule your appointment on 2025-05-12 at 17:00  - 19:00 🔁', 71, 'dismissed', '2025-05-12 15:08:02'),
(38, 5, 'Your appointment on 2025-05-18 at 10:00 - 12:00 has been Confirmed ✅', 88, 'dismissed', '2025-05-12 15:11:40'),
(39, 5, 'Doctor requested to reschedule your appointment on 2025-05-11 at 10:00 - 12:00 🔁', 74, 'dismissed', '2025-05-12 15:14:31'),
(40, 5, 'Doctor requested to reschedule your appointment on 2025-05-15 at 17:00  - 19:00  🔁', 89, 'dismissed', '2025-05-12 15:18:03'),
(41, 5, 'Doctor requested to reschedule your appointment on 2025-05-11 at 10:00 - 12:00 🔁', 74, 'dismissed', '2025-05-12 15:21:33'),
(42, 1, 'Doctor requested to reschedule your appointment on 2025-05-05 at 12:00 - 14:00 🔁', 27, 'dismissed', '2025-05-13 12:55:05'),
(43, 1, 'Your appointment on 2025-05-20 at 08:00 - 10:00 has been Confirmed ✅', 46, 'dismissed', '2025-05-13 12:56:29'),
(44, 1, 'Your appointment on 2025-05-02 at 16:00 - 18:00 has been Cancelled ❌', 26, 'dismissed', '2025-05-13 12:57:36'),
(45, 1, 'Your appointment on 2024-09-18 at 15:20:00 has been Cancelled ❌', 1, 'unread', '2025-05-15 08:39:15'),
(46, 1, 'Doctor requested to reschedule your appointment on 2024-09-19 at 17:30:00 🔁', 8, 'unread', '2025-05-15 08:39:29'),
(47, 1, 'Your appointment on 2024-09-18 at 15:20:00 has been Confirmed ✅', 1, 'unread', '2025-05-15 16:19:03'),
(48, 1, 'Update on your appointment for 2024-09-18 at 15:20:00', 1, 'unread', '2025-05-15 16:19:11'),
(49, 1, 'Your appointment on 2024-09-19 at 17:30:00 has been Cancelled ❌', 8, 'unread', '2025-05-15 16:19:16'),
(50, 1, 'Doctor requested to reschedule your appointment on 2024-09-22 at 15:00:00 🔁', 9, 'unread', '2025-05-15 16:19:25'),
(51, 1, 'Your appointment on 2024-09-25 at 18:30:00 has been Cancelled ❌', 10, 'unread', '2025-05-15 18:57:39'),
(52, 1, 'Your appointment on 2025-05-06 at 08:00 - 10:00 has been Cancelled ❌', 36, 'unread', '2025-05-19 17:30:02'),
(53, 1, 'Update on your appointment for 2025-04-29 at 10.00  - 12.00 ', 25, 'unread', '2025-12-03 14:35:07'),
(54, 1, 'Your appointment on 2025-05-04 at 20:00 - 22:00 has been Confirmed ✅', 41, 'unread', '2025-12-03 14:48:18'),
(55, 1, 'Your appointment on 2025-05-09 at 20:00 - 22:00 has been Confirmed ✅', 42, 'unread', '2025-12-03 16:53:59'),
(56, 1, 'Your appointment on 2025-05-16 at 20:00 - 22:00 has been Cancelled ❌', 45, 'unread', '2025-12-03 16:54:07'),
(57, 1, 'Update on your appointment for 2025-05-04 at 20:00 - 22:00', 41, 'unread', '2025-12-03 16:54:19'),
(58, 3, 'Doctor requested to reschedule your appointment on 2024-09-25 at 18:20:00 🔁', 13, 'unread', '2025-12-04 17:42:26'),
(59, 1, 'Your appointment on 2025-05-20 at 08:00 - 10:00 has been Confirmed ✅', 46, 'unread', '2025-12-09 18:29:36'),
(60, 4, 'Your appointment on 2025-12-14 at 08:00 AM has been Confirmed ✅', 48, 'unread', '2025-12-10 17:13:02'),
(61, 4, 'Your appointment on 2025-12-14 at 08:00 AM has been Confirmed ✅', 48, 'unread', '2025-12-11 06:25:10');

-- --------------------------------------------------------

--
-- Table structure for table `pharmacies`
--

CREATE TABLE `pharmacies` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `longitude` decimal(10,7) NOT NULL,
  `latitude` decimal(10,7) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `pharmacies`
--

INSERT INTO `pharmacies` (`id`, `name`, `address`, `longitude`, `latitude`, `created_at`) VALUES
(1, 'Wellbeing Pharmacy ~ Dhanmondi', 'House # 80, Road # 8/A, Satmasjid Road, Dhaka 1209', 23.7445492, 90.3729289, '2025-04-19 07:48:48'),
(2, 'BD Pharmacy', '393 Free School St, Dhaka 1205', 23.7451762, 90.3898939, '2025-04-19 07:48:48'),
(3, 'Dhanmondi Pharmacy', 'House No, 07 Road No. 2, Dhaka 1205', 23.7399908, 90.3822550, '2025-04-19 07:48:48'),
(4, 'Tamanna Pharmacy Zigatola', '25, 25/7/2, Zigatola, Dhaka 1209', 23.7396055, 90.3723301, '2025-04-19 07:48:48'),
(5, 'Ayesha Pharmacy', 'R949+7CG, Dhaka 1216', 23.8057551, 90.3686451, '2025-04-19 07:48:48'),
(6, 'Khan Pharmecy & Departmental Store', 'Commercial Plot 31, Main Rd 1, Senpara Parbata, Mirpur 10,, Opposite to Mirpur-10 Water Tank, Dhaka 1216', 23.8066974, 90.3733228, '2025-04-19 07:48:48'),
(7, 'AN PHARMACY', '458/1/A Senpara Parbata Ln Below Kazi Office, Behind NAM Garden Mirpur, Dhaka 1216', 23.8033951, 90.3759644, '2025-04-19 07:48:48'),
(8, 'র্ফামা প্যালেস', '৯২, Senpara Parbata Lane, মিরপুর ১০ নং গোলচত্বর, Dhaka 1216', 23.8029435, 90.3744195, '2025-04-19 07:48:48'),
(9, 'Lazz Pharma Badda Branch', 'Cha-89/6, North, Progati Sarani Rd, Dhaka 1212', 23.7924931, 90.4246076, '2025-04-19 07:48:48'),
(10, 'M/S. Dhaka Pharmacy', 'Cha-87/C, Fuji Trade Centre, North Badda, Badda, Dhaka 1212', 23.7899799, 90.4258092, '2025-04-19 07:48:48'),
(11, 'Mediline Pharmacy & Departmental Store', 'Ja-50, Dhaka 1212', 23.7868384, 90.4230626, '2025-04-19 07:48:48');

-- --------------------------------------------------------

--
-- Table structure for table `prescription`
--

CREATE TABLE `prescription` (
  `pres_id` int(11) NOT NULL,
  `p_id` int(11) NOT NULL,
  `d_id` int(11) NOT NULL,
  `detail` text DEFAULT NULL,
  `date` date DEFAULT NULL,
  `morning` varchar(255) NOT NULL,
  `afternoon` varchar(255) NOT NULL,
  `night` varchar(255) NOT NULL,
  `weekly_smbg` int(2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `prescription`
--

INSERT INTO `prescription` (`pres_id`, `p_id`, `d_id`, `detail`, `date`, `morning`, `afternoon`, `night`, `weekly_smbg`) VALUES
(1, 1, 1, 'Metformin, dose: (0 + 1 + 1)\r\nContinue it 15 days,  Empa Gliflozin, dose: (1 + 1 + 1) Continue it 1 month,  Suggested Diet Plan: 1', '2024-09-17', '', '', '', NULL),
(2, 1, 2, 'Alpha-glucosidase inhibitor,\r\ndose: 1 + 1 + 1\r\n\r\nSuggested Diet Plan: \r\nFollow your current one', '2024-09-17', '', '', '', NULL),
(3, 1, 6, 'Insulin (Morning: 10 unit) (After Dinner: 15 unit) ', '2024-09-17', '', '', '', NULL),
(4, 1, 1, 'increase the dose of metformin, dose: 1+ 1+ 1 ', '2024-09-18', '', '', '', NULL),
(5, 1, 1, 'Insulin 30mg', '2024-09-18', '', '', '', NULL),
(6, 1, 1, 'daily walk for 1 hour a day. Maintain regularity.', '2024-09-18', '', '', '', NULL),
(7, 1, 1, 'Increase the dose of Insulin', '2024-09-18', '', '', '', NULL),
(8, 4, 1, 'Metformin dose decrease. dose: 1+ 0 + 1', '2024-09-19', '', '', '', NULL),
(9, 1, 10, 'Increase the dose of insulin', '2024-09-29', '', '', '', NULL),
(10, 1, 1, '- Diabetic diet, \r\n- exercise\r\n- Empa 10', '2024-10-04', '', '', '', NULL),
(12, 1, 1, 'Walk regularly', '2025-04-30', 'Ozempic 1ml', 'Comet', 'Insulin 10ml', NULL),
(14, 1, 1, 'Walk 30 minutes every day.', '2025-05-15', 'Comet', 'Insulin 20ml', 'Insulin 10ml', NULL),
(15, 1, 1, 'Walk regularly', '2025-05-15', 'Insulin 15mg', 'Comet', 'insulin 30mg', NULL),
(16, 1, 1, 'Monitor blood glucose levels daily', '2025-12-05', 'Metformin 500mg before breakfast', 'no medication', 'Metformin 500mg after dinner', NULL),
(17, 1, 1, NULL, '2025-12-06', '', '', '', 2),
(18, 1, 1, NULL, '2025-12-11', '', '', '', 2);

-- --------------------------------------------------------

--
-- Table structure for table `slot`
--

CREATE TABLE `slot` (
  `slot_id` int(11) NOT NULL,
  `slot_time` time DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `slot`
--

INSERT INTO `slot` (`slot_id`, `slot_time`) VALUES
(1, '15:00:00'),
(2, '15:30:00'),
(3, '16:00:00'),
(4, '16:30:00'),
(5, '17:00:00'),
(6, '17:30:00'),
(7, '18:00:00'),
(8, '18:30:00');

-- --------------------------------------------------------

--
-- Table structure for table `sos_alerts`
--

CREATE TABLE `sos_alerts` (
  `p_id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `location` varchar(255) DEFAULT NULL,
  `timestamp` datetime DEFAULT current_timestamp(),
  `responded` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sos_alerts`
--

INSERT INTO `sos_alerts` (`p_id`, `name`, `location`, `timestamp`, `responded`) VALUES
(4, 'labiba', '23.7745978,90.4219535', '2025-04-24 18:42:05', 1),
(6, 'David', '23.7508529,90.4013365', '2025-05-15 02:30:28', 0);

-- --------------------------------------------------------

--
-- Table structure for table `sugar_lvl`
--

CREATE TABLE `sugar_lvl` (
  `Food` varchar(20) NOT NULL,
  `Sugar_level` float(4,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sugar_lvl`
--

INSERT INTO `sugar_lvl` (`Food`, `Sugar_level`) VALUES
('Ice Cream', 16.99);

-- --------------------------------------------------------

--
-- Table structure for table `telemedicine_payment`
--

CREATE TABLE `telemedicine_payment` (
  `pay_id` int(11) NOT NULL,
  `app_id` int(11) NOT NULL,
  `paid` tinyint(1) NOT NULL DEFAULT 0,
  `amount` decimal(10,2) DEFAULT NULL,
  `timestamp` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `telemedicine_payment`
--

INSERT INTO `telemedicine_payment` (`pay_id`, `app_id`, `paid`, `amount`, `timestamp`) VALUES
(1, 55, 1, 1000.00, '2025-12-12 16:48:21'),
(2, 56, 1, 1000.00, '2025-12-12 16:54:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `appointment`
--
ALTER TABLE `appointment`
  ADD PRIMARY KEY (`app_id`),
  ADD KEY `d_id` (`d_id`),
  ADD KEY `p_id` (`p_id`);

--
-- Indexes for table `card_registry`
--
ALTER TABLE `card_registry`
  ADD PRIMARY KEY (`card_id`),
  ADD KEY `p_id` (`p_id`);

--
-- Indexes for table `diet`
--
ALTER TABLE `diet`
  ADD PRIMARY KEY (`diet_id`);

--
-- Indexes for table `doctor`
--
ALTER TABLE `doctor`
  ADD PRIMARY KEY (`d_id`);

--
-- Indexes for table `doctor_reviews`
--
ALTER TABLE `doctor_reviews`
  ADD PRIMARY KEY (`review_id`),
  ADD UNIQUE KEY `unique_review` (`p_id`,`d_id`),
  ADD KEY `d_id` (`d_id`);

--
-- Indexes for table `doctor_schedule`
--
ALTER TABLE `doctor_schedule`
  ADD PRIMARY KEY (`d_id`);

--
-- Indexes for table `doctor_slot`
--
ALTER TABLE `doctor_slot`
  ADD PRIMARY KEY (`slot_id`),
  ADD KEY `d_id` (`d_id`);

--
-- Indexes for table `medicines`
--
ALTER TABLE `medicines`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_medicine_pharmacy` (`pharmacy_id`,`medicine_name`);

--
-- Indexes for table `notices`
--
ALTER TABLE `notices`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sender_id` (`sender_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `p_id` (`p_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `patient_notifications`
--
ALTER TABLE `patient_notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `p_id` (`p_id`);

--
-- Indexes for table `pharmacies`
--
ALTER TABLE `pharmacies`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `prescription`
--
ALTER TABLE `prescription`
  ADD PRIMARY KEY (`pres_id`),
  ADD KEY `p_id` (`p_id`),
  ADD KEY `d_id` (`d_id`);

--
-- Indexes for table `slot`
--
ALTER TABLE `slot`
  ADD PRIMARY KEY (`slot_id`);

--
-- Indexes for table `sos_alerts`
--
ALTER TABLE `sos_alerts`
  ADD PRIMARY KEY (`p_id`);

--
-- Indexes for table `telemedicine_payment`
--
ALTER TABLE `telemedicine_payment`
  ADD PRIMARY KEY (`pay_id`),
  ADD KEY `app_id` (`app_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `appointment`
--
ALTER TABLE `appointment`
  MODIFY `app_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT for table `card_registry`
--
ALTER TABLE `card_registry`
  MODIFY `card_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `diet`
--
ALTER TABLE `diet`
  MODIFY `diet_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `doctor`
--
ALTER TABLE `doctor`
  MODIFY `d_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `doctor_reviews`
--
ALTER TABLE `doctor_reviews`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `doctor_slot`
--
ALTER TABLE `doctor_slot`
  MODIFY `slot_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `medicines`
--
ALTER TABLE `medicines`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `notices`
--
ALTER TABLE `notices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `p_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `patient_notifications`
--
ALTER TABLE `patient_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- AUTO_INCREMENT for table `pharmacies`
--
ALTER TABLE `pharmacies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `prescription`
--
ALTER TABLE `prescription`
  MODIFY `pres_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;

--
-- AUTO_INCREMENT for table `slot`
--
ALTER TABLE `slot`
  MODIFY `slot_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `telemedicine_payment`
--
ALTER TABLE `telemedicine_payment`
  MODIFY `pay_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointment`
--
ALTER TABLE `appointment`
  ADD CONSTRAINT `appointment_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctor` (`d_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `appointment_ibfk_2` FOREIGN KEY (`p_id`) REFERENCES `patient` (`p_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `card_registry`
--
ALTER TABLE `card_registry`
  ADD CONSTRAINT `card_registry_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patient` (`p_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `doctor_reviews`
--
ALTER TABLE `doctor_reviews`
  ADD CONSTRAINT `doctor_reviews_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patient` (`p_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `doctor_reviews_ibfk_2` FOREIGN KEY (`d_id`) REFERENCES `doctor` (`d_id`) ON DELETE CASCADE;

--
-- Constraints for table `doctor_schedule`
--
ALTER TABLE `doctor_schedule`
  ADD CONSTRAINT `doctor_schedule_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctor` (`d_id`);

--
-- Constraints for table `doctor_slot`
--
ALTER TABLE `doctor_slot`
  ADD CONSTRAINT `doctor_slot_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctor` (`d_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `notices`
--
ALTER TABLE `notices`
  ADD CONSTRAINT `notices_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `admin` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `patient` (`p_id`);

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`order_id`) ON DELETE CASCADE;

--
-- Constraints for table `prescription`
--
ALTER TABLE `prescription`
  ADD CONSTRAINT `prescription_ibfk_1` FOREIGN KEY (`d_id`) REFERENCES `doctor` (`d_id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `telemedicine_payment`
--
ALTER TABLE `telemedicine_payment`
  ADD CONSTRAINT `telemedicine_payment_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `appointment` (`app_id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
