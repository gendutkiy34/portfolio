/usr/lib/oracle/18.3/client64/bin/sqlplus -s {string_connection} <<EOF


SET MARKUP CSV ON delimiter "|"

SELECT ENCRYPTED_MSISDN,CONCAT('62',MSISDN) AS MSISDN
FROM 
(SELECT ENCRYPTED_MSISDN,MSISDN 
FROM SCMUSER.SUBSCRIBER_PROFILE_1
UNION
SELECT ENCRYPTED_MSISDN,MSISDN 
FROM SCMUSER.SUBSCRIBER_PROFILE_2)
WHERE ENCRYPTED_MSISDN in ('{encryption}');

SPOOL OFF
EXIT
EOF