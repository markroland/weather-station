CREATE TABLE `station` (
  `id` tinyint(2) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(32) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  `latitude` float(10,6) NOT NULL,
  `longitude` float(10,6) NOT NULL,
  `altitude` smallint(6) NOT NULL DEFAULT '0',
  `api_key` varchar(32) COLLATE utf8_unicode_ci NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

CREATE TABLE `station_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `station_id` tinyint(2) unsigned NOT NULL DEFAULT '0',
  `log_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `temperature` float(5,2) DEFAULT NULL,
  `humidity` float(5,2) DEFAULT NULL,
  `pressure` float(8,2) DEFAULT NULL,
  `light` float(5,2) DEFAULT NULL,
  `wind` float(5,2) DEFAULT NULL,
  `rain` float(4,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
