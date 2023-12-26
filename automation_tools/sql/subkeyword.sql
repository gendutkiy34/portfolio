/usr/lib/oracle/18.3/client64/bin/sqlplus -s {string_connection} <<EOF

SET MARKUP CSV ON delimiter "|"

SELECT KEY_VALUES AS OFFERCODE,KEYWORD ,SHORTCODE ,SERVICE_NAME ,to_char(CREATE_DATE,'dd-mm-yyyy') AS  CREATE_DATE
FROM MOUSER.SMS_SYNONYMS
{condition} 
ORDER BY KEYWORD;

SPOOL OFF
EXIT
EOF