create table CRWAL_INVESTOR_STOCK_TYPE (
                                           TYPE_CODE VARCHAR(10),
                                           DATEON VARCHAR(10),
                                           END_VALUE FLOAT,
                                           DELTA FLOAT,
                                           UPDOWN_PER FLOAT,
                                           VOLUME FLOAT,
                                           COMP_BUY FLOAT,
                                           FOR_BUY FLOAT,
                                           FOR_CONT FLOAT,
                                           FOR_PER FLOAT,
                                           primary key(TYPE_CODE, DATEON)

) ;

select count(*) from CRWAL_INVESTOR_STOCK_TYPE ;

create table CRAWL_INVESTOR_DAILY_VOLUME (
                                             TYPE_CODE VARCHAR(10),
                                             DATEON VARCHAR(10),
                                             PERSONAL FLOAT,
                                             FOREIGNER FLOAT,
                                             COMPANY FLOAT,
                                             FINANCE FLOAT,
                                             INSURANCE FLOAT,
                                             TOOSIN FLOAT,
                                             BANK FLOAT,
                                             ETC_FIN FLOAT,
                                             GOV_FUND FLOAT,
                                             ETC_FUND FLOAT,
                                             primary key(TYPE_CODE, DATEON)
) ;