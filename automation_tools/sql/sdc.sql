/usr/lib/oracle/18.3/client64/bin/sqlplus -s {string_connection} <<EOF

SET MARKUP CSV ON delimiter "|"

SELECT b.CP_ID,b.CP_NAME ,a.OFFER_ID as OFFER_CODE,DECODE(a.TYPE_OF_DIRECTION,'0','MT','1','MO')TYPE_OF_DIRECTION,a.SENDER_MASKING_ADDRESS 
,a.MO_SHORT_CODE ,a.MO_KEYWORD ,DECODE(a.OPERATION_TYPE,'5','Bulk')OPERATION_TYPE
,a.CHARGE_AMOUNT ,a.ALLOWED_SERIES_ON_MO ,a.ALLOWED_SERIES_ON_MT ,a.CONNECTION_REFERENCE 
,TO_CHAR(a.CREATE_DATE,'yyyy-mm-dd HH24:MI') CREATE_DATE ,TO_CHAR(a.UPDATE_DATE,'yyyy-mm-dd HH24:MI') UPDATE_DATE
FROM scmuser.SUBSCRIPTION_SDC a
LEFT JOIN SCMUSER.SUBSCRIPTION_OFFER b ON a.OFFER_ID=b.OFFER_CODE
{condition}
ORDER BY a.OFFER_ID,a.MO_SHORT_CODE ;

SPOOL OFF
EXIT
EOF