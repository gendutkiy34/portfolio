/usr/lib/oracle/18.3/client64/bin/sqlplus -s {string_connection} <<EOF

SET MARKUP CSV ON delimiter "|"

SELECT to_char(CDR_TIMESTAMP,'dd-mm-yyyy') as cdr_date,DIAMETER_RESULT_CODES
,decode(SUB_CALL_TYPE,'1','On-net','2','Off-net','International call') as call_type
,sum(call_duration) as sum_duration
FROM
(SELECT CDR_TIMESTAMP,CALL_REFERENCE_NUMBER,TRANSACTION_ID,SUB_CALL_TYPE,DIAMETER_RESULT_CODES,CALL_DURATION
FROM SCPCDR.INTERNAL_CDR_{day}
WHERE M_MONTH= '{mon}'
UNION ALL
SELECT CDR_TIMESTAMP,CALL_REFERENCE_NUMBER,TRANSACTION_ID,SUB_CALL_TYPE,DIAMETER_RESULT_CODES,CALL_DURATION
FROM SCPCDR.INTERNAL_CDR_{day}@scpcdr_prod_pk_public
WHERE M_MONTH= '{mon}'
)
GROUP BY to_char(CDR_TIMESTAMP,'dd-mm-yyyy'),DIAMETER_RESULT_CODES,decode(SUB_CALL_TYPE,'1','On-net','2','Off-net','International call')
ORDER BY to_char(CDR_TIMESTAMP,'dd-mm-yyyy'),DIAMETER_RESULT_CODES,decode(SUB_CALL_TYPE,'1','On-net','2','Off-net','International call');

SPOOL OFF
EXIT
EOF