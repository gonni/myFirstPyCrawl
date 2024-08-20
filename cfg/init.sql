-- zio.crawl_investor_daily_volume definition

CREATE TABLE `crawl_investor_daily_volume` (
                                               `TYPE_CODE` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
                                               `DATEON` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
                                               `PERSONAL` float DEFAULT NULL,
                                               `FOREIGNER` float DEFAULT NULL,
                                               `COMPANY` float DEFAULT NULL,
                                               `FINANCE` float DEFAULT NULL,
                                               `INSURANCE` float DEFAULT NULL,
                                               `TOOSIN` float DEFAULT NULL,
                                               `BANK` float DEFAULT NULL,
                                               `ETC_FIN` float DEFAULT NULL,
                                               `GOV_FUND` float DEFAULT NULL,
                                               `ETC_FUND` float DEFAULT NULL,
                                               PRIMARY KEY (`TYPE_CODE`,`DATEON`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- zio.crwal_investor_stock_type definition

CREATE TABLE `crwal_investor_stock_type` (
                                             `TYPE_CODE` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
                                             `DATEON` varchar(10) COLLATE utf8mb4_general_ci NOT NULL,
                                             `END_VALUE` float DEFAULT NULL,
                                             `DELTA` float DEFAULT NULL,
                                             `UPDOWN_PER` float DEFAULT NULL,
                                             `VOLUME` float DEFAULT NULL,
                                             `COMP_BUY` float DEFAULT NULL,
                                             `FOR_BUY` float DEFAULT NULL,
                                             `FOR_CONT` float DEFAULT NULL,
                                             `FOR_PER` float DEFAULT NULL,
                                             PRIMARY KEY (`TYPE_CODE`,`DATEON`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--

create table CRAWL_MARKET_DAILY_DATA (
                                         TYPE_CODE varchar(10),
                                         DATEON varchar(10),
                                         CLOSING_PRICE float,
                                         UP_DOWN_PER float,
                                         VOLUME float,
                                         VOLUME_AMT float,
                                         PRIMARY KEY (`TYPE_CODE`,`DATEON`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci ;