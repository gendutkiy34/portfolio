/usr/lib/oracle/18.3/client64/bin/sqlplus -s {string_connection} <<EOF

SET MARKUP CSV ON delimiter "|"

SELECT TO_CHAR(CDR_TIMESTAMP,'dd-mm-yyyy') CDR_DATE,TO_CHAR(CDR_TIMESTAMP,'HH24:MI') CDR_HOUR
,CALL_REFERENCE_NUMBER,TRANSACTION_ID,CALLING_PARTY,CALLED_PARTY
,DECODE(SUBSCRIBER_TYPE,'1','PREPAID','2','POSTPAID')SUBSCRIBER_TYPE,CALL_STATUS
,DIAMETER_RESULT_CODES,DIAMETER_ERROR_MESSAGE,CELL_ID,MSC_ADDRESS,VLR_ADDRESS
,DIAMTER_SESSION_ID,INSTANCE_ID
,DECODE(CALL_TYPE,'1','MOC','2','MTC','3','MFC','4','UCB')CALL_TYPE
,DECODE(SUB_CALL_TYPE,'1','On-net','2','Off-net','3','International Call')SUB_CALL_TYPE
,DECODE(IS_ROAMING,'0','false','1','true')IS_ROAMING,DECODE(IS_CHARGING_OVERRULED,'0','false','1','true')IS_CHARGING_OVERRULED
,DECODE(ISBFT,'0','Disabled','1','Enabled')ISBFT,CALL_START_TIME,CALL_DISCONNECTING_TIME,CALL_DURATION,NORMALISED_NUMBER,TRANSLATED_NUMBER,SERVICE_KEY
,DECODE(IS_FOC,'0','false','1','true')IS_FOC
FROM
(SELECT CDR_TIMESTAMP,CALL_REFERENCE_NUMBER,TRANSACTION_ID,CALLING_PARTY,CALLED_PARTY,SUBSCRIBER_TYPE,CALL_STATUS,DIAMETER_RESULT_CODES,DIAMETER_ERROR_MESSAGE,CELL_ID,MSC_ADDRESS,VLR_ADDRESS,DIAMTER_SESSION_ID,INSTANCE_ID,CALL_TYPE,SUB_CALL_TYPE,IS_ROAMING,IS_CHARGING_OVERRULED,ISBFT,CALL_ANSWER_TIME as CALL_START_TIME,CALL_DISCONNECTING_TIME,CALL_DURATION,NORMALISED_NUMBER,TRANSLATED_NUMBER,SERVICE_KEY,IS_FOC
FROM SCPCDR.INTERNAL_CDR_{day}
WHERE M_MONTH= '{mon}' AND ISBFT='1' AND TO_CHAR(CDR_TIMESTAMP,'HH24')='{hour}'
UNION ALL
SELECT CDR_TIMESTAMP,CALL_REFERENCE_NUMBER,TRANSACTION_ID,CALLING_PARTY,CALLED_PARTY,SUBSCRIBER_TYPE,CALL_STATUS,DIAMETER_RESULT_CODES,DIAMETER_ERROR_MESSAGE,CELL_ID,MSC_ADDRESS,VLR_ADDRESS,DIAMTER_SESSION_ID,INSTANCE_ID,CALL_TYPE,SUB_CALL_TYPE,IS_ROAMING,IS_CHARGING_OVERRULED,ISBFT,CALL_ANSWER_TIME as CALL_START_TIME,CALL_DISCONNECTING_TIME,CALL_DURATION,NORMALISED_NUMBER,TRANSLATED_NUMBER,SERVICE_KEY,IS_FOC
FROM SCPCDR.INTERNAL_CDR_{day}@scpcdr_prod_pk_public
WHERE M_MONTH= '{mon}' AND ISBFT='1' AND TO_CHAR(CDR_TIMESTAMP,'HH24')='{hour}'
)
ORDER BY TO_CHAR(CDR_TIMESTAMP,'HH24:MI');

SPOOL OFF
EXIT
EOF