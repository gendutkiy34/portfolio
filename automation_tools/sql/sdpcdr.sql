/usr/lib/oracle/18.3/client64/bin/sqlplus -s {string_connection} <<EOF

SET MARKUP CSV ON delimiter "|"

select to_char(timestamp,'dd-mm-yyyy') as cdrdate,to_char(timestamp,'HH24:MI:SS') as cdrtime,
clienttransactionid,aparty as MSISDN,internalcause,basiccause,transactionid,offercode,accessflag,
callcharge as price,contentproviderid as cp_id,categoryid,cp_name,networkmode,shortcode,keyword,
taskid,username,thirdpartyerrorcode,channel,cp_loginname
FROM scmcdr.SCM_CC_{mon}
WHERE m_day='{day}' AND  aparty like '%{msisdn}'
ORDER BY to_char(timestamp,'HH24:MI:SS');

SPOOL OFF
EXIT
EOF