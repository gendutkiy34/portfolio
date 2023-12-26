/usr/lib/oracle/18.3/client64/bin/sqlplus -s {string_connection} <<EOF

SET MARKUP CSV ON delimiter "|"

SELECT SUBSTR(content_name,1,3) AS content_prefix,service_name,content_name,TO_CHAR(UPLOAD_DATE,'dd-mm-yyyy') AS UPLOAD_DATE,TO_CHAR(start_date,'dd-mm-yyyy') AS start_date,TO_CHAR(end_date,'dd-mm-yyyy') AS end_date
FROM cdp_comads.text_delivery_view
WHERE TO_CHAR(start_date,'mm-yyyy')='{monyear}' AND content_name LIKE '%BolehNet_%' ;

SPOOL OFF
EXIT
EOF