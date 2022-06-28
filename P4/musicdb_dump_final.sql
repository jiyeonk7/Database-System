-- --------------------------------------------------------
-- 호스트:                          127.0.0.1
-- 서버 버전:                        10.4.8-MariaDB - mariadb.org binary distribution
-- 서버 OS:                        Win64
-- HeidiSQL 버전:                  10.2.0.5599
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- musicdb 데이터베이스 구조 내보내기
CREATE DATABASE IF NOT EXISTS `musicdb` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `musicdb`;

-- 테이블 musicdb.device 구조 내보내기
CREATE TABLE IF NOT EXISTS `device` (
  `u_id` int(11) NOT NULL,
  `device_id` int(11) NOT NULL,
  `d_type` varchar(20) NOT NULL,
  PRIMARY KEY (`u_id`,`device_id`),
  CONSTRAINT `device_ibfk_1` FOREIGN KEY (`u_id`) REFERENCES `users` (`u_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 테이블 데이터 musicdb.device:~10 rows (대략적) 내보내기
DELETE FROM `device`;
/*!40000 ALTER TABLE `device` DISABLE KEYS */;
INSERT INTO `device` (`u_id`, `device_id`, `d_type`) VALUES
	(401, 501, 'phone'),
	(402, 502, 'phone'),
	(402, 503, 'tablet'),
	(402, 504, 'pc'),
	(403, 505, 'tablet'),
	(403, 506, 'pc'),
	(404, 507, 'phone'),
	(404, 508, 'tablet'),
	(404, 509, 'pc'),
	(405, 510, 'phone');
/*!40000 ALTER TABLE `device` ENABLE KEYS */;

-- 테이블 musicdb.manager 구조 내보내기
CREATE TABLE IF NOT EXISTS `manager` (
  `m_name` varchar(15) NOT NULL,
  `m_addr` varchar(25) DEFAULT NULL,
  `m_contact` varchar(50) DEFAULT NULL,
  `m_id` int(11) NOT NULL,
  PRIMARY KEY (`m_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 테이블 데이터 musicdb.manager:~6 rows (대략적) 내보내기
DELETE FROM `manager`;
/*!40000 ALTER TABLE `manager` DISABLE KEYS */;
INSERT INTO `manager` (`m_name`, `m_addr`, `m_contact`, `m_id`) VALUES
	('Abe Parrell', 'Gyeonggi', '01034782918', 201),
	('Caren Quizos', 'Seoul', '01029492048', 202),
	('Garret Ralsh', 'Busan', '01038532849', 203),
	('Devin Wells', 'Seoul', '01038598491', 204),
	('Jiyeon Kim', 'Seoul', '01053002891', 165411);
/*!40000 ALTER TABLE `manager` ENABLE KEYS */;

-- 테이블 musicdb.mp 구조 내보내기
CREATE TABLE IF NOT EXISTS `mp` (
  `p_id` int(11) NOT NULL,
  `s_id` int(11) NOT NULL,
  PRIMARY KEY (`p_id`,`s_id`),
  KEY `s_id` (`s_id`),
  CONSTRAINT `mp_ibfk_1` FOREIGN KEY (`p_id`) REFERENCES `playlist` (`playlist_id`),
  CONSTRAINT `mp_ibfk_2` FOREIGN KEY (`s_id`) REFERENCES `music` (`song_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 테이블 데이터 musicdb.mp:~10 rows (대략적) 내보내기
DELETE FROM `mp`;
/*!40000 ALTER TABLE `mp` DISABLE KEYS */;
INSERT INTO `mp` (`p_id`, `s_id`) VALUES
	(301, 100),
	(301, 102),
	(301, 103),
	(301, 104),
	(301, 105),
	(301, 106),
	(302, 101),
	(302, 102),
	(302, 103),
	(302, 104);
/*!40000 ALTER TABLE `mp` ENABLE KEYS */;

-- 테이블 musicdb.music 구조 내보내기
CREATE TABLE IF NOT EXISTS `music` (
  `title` varchar(20) NOT NULL,
  `genre` char(10) DEFAULT NULL,
  `composer` varchar(15) DEFAULT NULL,
  `artist` varchar(20) NOT NULL,
  `release_date` date DEFAULT NULL,
  `album_name` varchar(20) DEFAULT NULL,
  `run_time` int(11) NOT NULL,
  `song_id` int(11) NOT NULL,
  `I_mgr_id` int(11) DEFAULT NULL,
  `D_mgr_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`song_id`),
  KEY `I_mgr_id` (`I_mgr_id`),
  KEY `D_mgr_id` (`D_mgr_id`),
  CONSTRAINT `music_ibfk_1` FOREIGN KEY (`I_mgr_id`) REFERENCES `manager` (`m_id`),
  CONSTRAINT `music_ibfk_2` FOREIGN KEY (`D_mgr_id`) REFERENCES `manager` (`m_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 테이블 데이터 musicdb.music:~10 rows (대략적) 내보내기
DELETE FROM `music`;
/*!40000 ALTER TABLE `music` DISABLE KEYS */;
INSERT INTO `music` (`title`, `genre`, `composer`, `artist`, `release_date`, `album_name`, `run_time`, `song_id`, `I_mgr_id`, `D_mgr_id`) VALUES
	('Four Seasons', 'pop', 'josh cumbee', 'taeyeon', '2019-03-24', 'Four Seasons', 188, 100, 201, 203),
	('Friends', 'ballad', 'nilo', 'nilo', '2019-08-26', 'Friend', 269, 101, 204, NULL),
	('Here I am', 'pop', 'matthew tishler', 'taeyeon', '2019-10-28', 'Purpose', 204, 102, 204, NULL),
	('Guerilla', 'dance', 'steven lee', 'oh my girl', '2019-10-25', 'Queendom', 227, 103, 201, 202),
	('Friends', 'pop', 'marshmello', 'anne-marie', '2018-04-27', 'Speak Your Mind', 202, 104, 204, NULL),
	('Congratualtions', 'ballad', NULL, 'eric nam', '1029-10-30', 'Love Die Young', 176, 105, 204, NULL),
	('Runaway', 'dance', NULL, 'eric nam', '2019-05-08', 'Runaway', 153, 106, 204, NULL),
	('Love You Like Crazy', 'pop', 'kenzie', 'taeyeon', '2019-10-28', 'Purpose', 179, 107, 201, NULL),
	('Speechless', 'ost', 'michael kosarin', 'naomi scott', '2019-05-22', 'Aladdin', 208, 108, 201, NULL),
	('Freedom', 'pop', 'chanhyuk lee', 'akmu', '2019-09-25', 'Sail', 213, 109, 201, NULL);
/*!40000 ALTER TABLE `music` ENABLE KEYS */;

-- 테이블 musicdb.playlist 구조 내보내기
CREATE TABLE IF NOT EXISTS `playlist` (
  `total_time` int(11) NOT NULL,
  `num_song` int(11) NOT NULL,
  `playlist_id` int(11) NOT NULL,
  `p_user` int(11) NOT NULL,
  PRIMARY KEY (`playlist_id`),
  KEY `p_user` (`p_user`),
  CONSTRAINT `playlist_ibfk_1` FOREIGN KEY (`p_user`) REFERENCES `users` (`u_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 테이블 데이터 musicdb.playlist:~2 rows (대략적) 내보내기
DELETE FROM `playlist`;
/*!40000 ALTER TABLE `playlist` DISABLE KEYS */;
INSERT INTO `playlist` (`total_time`, `num_song`, `playlist_id`, `p_user`) VALUES
	(1150, 6, 301, 401),
	(902, 4, 302, 402);
/*!40000 ALTER TABLE `playlist` ENABLE KEYS */;

-- 테이블 musicdb.users 구조 내보내기
CREATE TABLE IF NOT EXISTS `users` (
  `u_name` varchar(50) NOT NULL,
  `u_id` varchar(50) NOT NULL,
  `u_password` varchar(50) NOT NULL,
  `u_contact` varchar(50) DEFAULT NULL,
  `u_ssn` varchar(50) NOT NULL,
  `u_num` int(11) NOT NULL,
  PRIMARY KEY (`u_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- 테이블 데이터 musicdb.users:~5 rows (대략적) 내보내기
DELETE FROM `users`;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`u_name`, `u_id`, `u_password`, `u_contact`, `u_ssn`, `u_num`) VALUES
	('Betty Ewalsh', 'itsy_betsy7', 'walshbe7', '01028403958', '9805142084943', 401),
	('Harriot Kevary', 'hk0523', 'kevarygo89', '01027842738', '8803242859374', 402),
	('Karen Joseph', 'kjoseph', 'kjaorseenph7', '01027492837', '9906281938475', 403),
	('Loraine Morrel', 'golmque3', 'morrelloraine3', '01023974822', '0211173847562', 404),
	('Nathan Owen', 'nathan0783', 'owenisgreat555', '01084343294', '9012271938874', 405);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
