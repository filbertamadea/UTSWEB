-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 04, 2022 at 06:42 AM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_book`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_anggota`
--

CREATE TABLE `tb_anggota` (
  `NIM` int(3) NOT NULL,
  `Nama` varchar(50) NOT NULL,
  `Jurusan` varchar(30) NOT NULL,
  `Username` varchar(12) NOT NULL,
  `Password` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_anggota`
--

INSERT INTO `tb_anggota` (`NIM`, `Nama`, `Jurusan`, `Username`, `Password`) VALUES
(1, 'Jemima Smith', 'Linguistic', 'jsmith', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `tb_buku`
--

CREATE TABLE `tb_buku` (
  `KodeBuku` int(3) NOT NULL,
  `Judul` varchar(50) NOT NULL,
  `Stok` int(3) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_buku`
--

INSERT INTO `tb_buku` (`KodeBuku`, `Judul`, `Stok`) VALUES
(1, 'How to Python', 2),
(2, 'Why Python', 1),
(3, 'Python for Dummies', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tb_kembali`
--

CREATE TABLE `tb_kembali` (
  `KodeKembali` int(3) NOT NULL,
  `KodeBuku` int(3) NOT NULL,
  `NIM` int(3) NOT NULL,
  `TglKembali` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_kembali`
--

INSERT INTO `tb_kembali` (`KodeKembali`, `KodeBuku`, `NIM`, `TglKembali`) VALUES
(1, 1, 1, '2022-04-21'),
(2, 1, 1, '2004-04-22');

-- --------------------------------------------------------

--
-- Table structure for table `tb_pinjam`
--

CREATE TABLE `tb_pinjam` (
  `KodePinjam` int(3) NOT NULL,
  `KodeBuku` int(3) NOT NULL,
  `NIM` int(3) NOT NULL,
  `TglPinjam` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `tb_pinjam`
--

INSERT INTO `tb_pinjam` (`KodePinjam`, `KodeBuku`, `NIM`, `TglPinjam`) VALUES
(1, 2, 1, '2022-04-13');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_anggota`
--
ALTER TABLE `tb_anggota`
  ADD PRIMARY KEY (`NIM`);

--
-- Indexes for table `tb_buku`
--
ALTER TABLE `tb_buku`
  ADD PRIMARY KEY (`KodeBuku`);

--
-- Indexes for table `tb_kembali`
--
ALTER TABLE `tb_kembali`
  ADD PRIMARY KEY (`KodeKembali`),
  ADD KEY `KodeBuku` (`KodeBuku`),
  ADD KEY `NIM` (`NIM`);

--
-- Indexes for table `tb_pinjam`
--
ALTER TABLE `tb_pinjam`
  ADD PRIMARY KEY (`KodePinjam`),
  ADD KEY `KodeBuku` (`KodeBuku`) USING BTREE,
  ADD KEY `NIM` (`NIM`) USING BTREE;

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_anggota`
--
ALTER TABLE `tb_anggota`
  MODIFY `NIM` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `tb_buku`
--
ALTER TABLE `tb_buku`
  MODIFY `KodeBuku` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `tb_kembali`
--
ALTER TABLE `tb_kembali`
  MODIFY `KodeKembali` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `tb_pinjam`
--
ALTER TABLE `tb_pinjam`
  MODIFY `KodePinjam` int(3) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `tb_kembali`
--
ALTER TABLE `tb_kembali`
  ADD CONSTRAINT `mm_relation_buku_kembali` FOREIGN KEY (`KodeBuku`) REFERENCES `tb_buku` (`KodeBuku`),
  ADD CONSTRAINT `mm_relation_nim_kembali` FOREIGN KEY (`NIM`) REFERENCES `tb_anggota` (`NIM`);

--
-- Constraints for table `tb_pinjam`
--
ALTER TABLE `tb_pinjam`
  ADD CONSTRAINT `mm_relation_buku` FOREIGN KEY (`KodeBuku`) REFERENCES `tb_buku` (`KodeBuku`),
  ADD CONSTRAINT `mm_relation_nim` FOREIGN KEY (`NIM`) REFERENCES `tb_anggota` (`NIM`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
