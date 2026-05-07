-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 07, 2026 at 02:16 AM
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
-- Database: `medicare`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `appointment_id` int(11) NOT NULL,
  `patient_id` int(11) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `appt_date` date DEFAULT NULL,
  `appt_time` time DEFAULT NULL,
  `reason` text DEFAULT NULL,
  `status` enum('pending','accepted','rejected','paid') DEFAULT 'pending',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `symptoms` text DEFAULT NULL,
  `is_visible_to_patient` tinyint(1) DEFAULT 1,
  `is_visible_to_doctor` tinyint(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`appointment_id`, `patient_id`, `doctor_id`, `appt_date`, `appt_time`, `reason`, `status`, `created_at`, `symptoms`, `is_visible_to_patient`, `is_visible_to_doctor`) VALUES
(1, 7, 10, '2026-05-07', '05:00:00', 'Knee Surgery', 'paid', '2026-04-30 00:17:21', NULL, 0, 1),
(2, 7, 9, '2026-05-01', '15:30:00', 'Gyno advice', 'paid', '2026-04-30 00:57:14', NULL, 0, 1),
(3, 7, 9, '2026-05-05', '20:00:00', 'Test', 'rejected', '2026-04-30 01:03:52', NULL, 0, 1),
(4, 7, 3, '2027-04-12', '12:33:00', 'fhgfdh', 'paid', '2026-04-30 01:08:00', NULL, 0, 0),
(5, 7, 10, '2026-04-30', '15:20:00', 'Follow up', 'paid', '2026-04-30 01:18:11', NULL, 0, 1),
(6, 7, 10, '2026-06-06', '15:30:00', 'TEST', 'accepted', '2026-05-06 23:42:58', 'TEST', 1, 1),
(7, 7, 3, '2026-05-07', '14:00:00', 'TEST', 'paid', '2026-05-06 23:58:31', 'TEST', 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `user_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `speciality` varchar(100) DEFAULT NULL,
  `degree` varchar(100) DEFAULT NULL,
  `experience` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`user_id`, `name`, `sex`, `speciality`, `degree`, `experience`) VALUES
(3, 'Faria', 'Female', 'Gynecologist & Obstetrician', 'MBBS', 15),
(9, 'Maria', 'Female', 'Gynecologist & Obstetrician', 'MBBS', 10),
(10, 'Abed', 'male', 'General Surgeon', 'MBBS', 30);

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `user_id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL,
  `sex` varchar(10) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `address` text DEFAULT NULL,
  `medical_records` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`user_id`, `name`, `sex`, `age`, `address`, `medical_records`) VALUES
(1, 'Patient ', 'Male', 25, NULL, 'Fever'),
(7, 'Ross', 'Male', 25, NULL, 'ADHD');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `appointment_id` int(11) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `vat` decimal(10,2) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `status` varchar(20) DEFAULT NULL,
  `payment_date` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `appointment_id`, `amount`, `vat`, `total`, `status`, `payment_date`) VALUES
(1, 1, 500.00, 75.00, 575.00, 'paid', '2026-04-30 00:38:16'),
(2, 2, 500.00, 75.00, 575.00, 'paid', '2026-04-30 01:05:34'),
(3, 4, 500.00, 75.00, 575.00, 'paid', '2026-04-30 01:09:01'),
(4, 5, 500.00, 75.00, 575.00, 'paid', '2026-04-30 01:27:07'),
(5, 7, 500.00, 75.00, 575.00, 'paid', '2026-05-06 23:59:42');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('patient','doctor','admin') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `name`, `email`, `password`, `role`) VALUES
(1, 'Admin', 'admin@gmail.com', '12345678', 'admin'),
(2, 'System Admin', 'admin@medicare.com', 'admin123', 'admin'),
(3, 'Faria', 'faria@medicare.com', '12345678', 'doctor'),
(6, 'Dr. Noman', 'noman@medicare.com', '12345678', 'doctor'),
(7, 'Ross', 'ross@gmail.com', '12345678', 'patient'),
(8, 'Faculty', 'faculty@medicare.com', '12345678', 'admin'),
(9, 'Maria', 'maria@medicare.com', '12345678', 'doctor'),
(10, 'Abed', 'abed@medicare.com', '12345678', 'doctor');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`appointment_id`),
  ADD KEY `fk_appt_patient` (`patient_id`),
  ADD KEY `fk_appt_doctor` (`doctor_id`);

--
-- Indexes for table `doctor`
--
ALTER TABLE `doctor`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`user_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD KEY `fk_payment_appt` (`appointment_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `appointment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `fk_appt_doctor` FOREIGN KEY (`doctor_id`) REFERENCES `user` (`user_id`),
  ADD CONSTRAINT `fk_appt_patient` FOREIGN KEY (`patient_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `doctor`
--
ALTER TABLE `doctor`
  ADD CONSTRAINT `fk_doctor_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `patient`
--
ALTER TABLE `patient`
  ADD CONSTRAINT `fk_patient_user` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`) ON DELETE CASCADE;

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `fk_payment_appt` FOREIGN KEY (`appointment_id`) REFERENCES `appointments` (`appointment_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
