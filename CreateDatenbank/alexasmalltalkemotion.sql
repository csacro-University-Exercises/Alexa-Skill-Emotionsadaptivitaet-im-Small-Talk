-- phpMyAdmin SQL Dump
-- version 4.8.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 16. Jun 2019 um 20:03
-- Server-Version: 10.1.34-MariaDB
-- PHP-Version: 7.2.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `alexasmalltalkemotion`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `activity`
--

CREATE TABLE `activity` (
  `ActivityId` int(10) UNSIGNED NOT NULL,
  `ActivityName` varchar(255) COLLATE utf8_german2_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `doneactivities`
--

CREATE TABLE `doneactivities` (
  `UserId` int(10) UNSIGNED NOT NULL,
  `ActivityId` int(10) UNSIGNED NOT NULL,
  `Count` int(10) UNSIGNED NOT NULL DEFAULT '0',
  `Status` int(1) NOT NULL,
  `lastStatusDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `futureactivites`
--

CREATE TABLE `futureactivites` (
  `UserId` int(10) UNSIGNED NOT NULL,
  `ActivityId` int(10) UNSIGNED NOT NULL,
  `Status` int(1) NOT NULL,
  `lastStatusDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `user`
--

CREATE TABLE `user` (
  `UserId` int(10) UNSIGNED NOT NULL,
  `UserName` varchar(255) COLLATE utf8_german2_ci NOT NULL,
  `Feeling` int(1) DEFAULT NULL,
  `lastFeelingDate` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_german2_ci;

--
-- Daten für Tabelle `user`
--

INSERT INTO `user` (`UserId`, `UserName`, `Feeling`, `lastFeelingDate`) VALUES
(1, 'Carolin', NULL, '2019-06-16 20:01:51');

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `activity`
--
ALTER TABLE `activity`
  ADD PRIMARY KEY (`ActivityId`),
  ADD UNIQUE KEY `ActivityName` (`ActivityName`);

--
-- Indizes für die Tabelle `doneactivities`
--
ALTER TABLE `doneactivities`
  ADD PRIMARY KEY (`UserId`,`ActivityId`),
  ADD KEY `ActivityId` (`ActivityId`);

--
-- Indizes für die Tabelle `futureactivites`
--
ALTER TABLE `futureactivites`
  ADD PRIMARY KEY (`UserId`,`ActivityId`),
  ADD KEY `ActivityId` (`ActivityId`);

--
-- Indizes für die Tabelle `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`UserId`),
  ADD UNIQUE KEY `UserName` (`UserName`);

--
-- AUTO_INCREMENT für exportierte Tabellen
--

--
-- AUTO_INCREMENT für Tabelle `activity`
--
ALTER TABLE `activity`
  MODIFY `ActivityId` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT für Tabelle `user`
--
ALTER TABLE `user`
  MODIFY `UserId` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- Constraints der exportierten Tabellen
--

--
-- Constraints der Tabelle `doneactivities`
--
ALTER TABLE `doneactivities`
  ADD CONSTRAINT `FK_activity_doneactivities` FOREIGN KEY (`ActivityId`) REFERENCES `activity` (`ActivityId`),
  ADD CONSTRAINT `FK_user_doneactivites` FOREIGN KEY (`UserId`) REFERENCES `user` (`UserId`);

--
-- Constraints der Tabelle `futureactivites`
--
ALTER TABLE `futureactivites`
  ADD CONSTRAINT `FK_activity_futureactivities` FOREIGN KEY (`ActivityId`) REFERENCES `activity` (`ActivityId`),
  ADD CONSTRAINT `FK_user_futureactivites` FOREIGN KEY (`UserId`) REFERENCES `user` (`UserId`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
