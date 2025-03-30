## Quick Start

`source /cvmfs/cms.cern.ch/rucio/setup-py3.sh`  
`rucio whoami`

### RSEs

```shell
[alikaan.gueven@clip]$ rucio list-rses
T0_CH_CERN_Disk
T0_CH_CERN_Tape
T2_AT_Vienna
```

*rse = Rucio Storage Element (i.e. sites)*

&nbsp;

### Scopes

- cms
- user.aguven
- group.t2_at_vienna

Use `rucio list-scopes`.

&nbsp;

### Replication Rule Example

`rucio add-rule <scope>:<name> <num copies> <rse> --source-replica-expression <rse> --lifetime <seconds>`

`rucio list-rules --account <RUCIO ACCOUNT>`

`rucio update-rule <rule id> --lifetime 1`

`rucio delete-rule <rule id>`

&nbsp;

```shell
[alikaan.gueven@clip]$ rucio add-rule cms:/store/data/Run2018D/MET/AOD/15Feb2022_UL2018-v1/510000/B57854FC-00E7-FB49-ABDF-1801AC61D29D.root 1 T2_AT_Vienna --source-replica-expression "T1_DE_KIT_Tape|T1_DE_KIT_Disk" --lifetime 3600
3026f8074e4547ebb067f9f725d5b133

[alikaan.gueven@clip]$ rucio rule-info 3026f8074e4547ebb067f9f725d5b133
Id:                         3026f8074e4547ebb067f9f725d5b133
Account:                    aguven
Scope:                      cms
Name:                       /store/data/Run2018D/MET/AOD/15Feb2022_UL2018-v1/510000/B57854FC-00E7-FB49-ABDF-1801AC61D29D.root
RSE Expression:             T2_AT_Vienna
Copies:                     1
State:                      REPLICATING
Locks OK/REPLICATING/STUCK: 0/1/0
Grouping:                   DATASET
Expires at:                 2025-03-27 10:57:42
Locked:                     False
Weight:                     None
Created at:                 2025-03-27 09:57:42
Updated at:                 2025-03-27 09:57:42
Error:                      None
Subscription Id:            None
Source replica expression:  T1_DE_KIT_Tape|T1_DE_KIT_Disk
Activity:                   User Subscriptions
Comment:                    None
Ignore Quota:               False
Ignore Availability:        False
Purge replicas:             False
Notification:               NO
End of life:                None
Child Rule Id:              None

rucio delete-rule 8354a394981744e58546b411e45c648d
rucio update-rule 8354a394981744e58546b411e45c648d --lifetime 1

```

&nbsp;

### Create datasets and containers

`dataset_regex=^\/[a-zA-Z0-9\-_]{1,99}\/[a-zA-Z0-9.\-_]{1,199}\/[A-Z0-9\-]{1,99}#[a-zA-Z0-9.\-_]{1,100}$`

`container_regex=^\/[a-zA-Z0-9\\-_]{1,99}\/[a-zA-Z0-9\\.\\-_]{1,199}\/[A-Z0-9\\-]{1,99}$`

&nbsp;

`dataset_pattern=user.<username>/<primary_name>/<secondary_name>/USER#<numbers>`

`container_pattern=user.<username>/<primary_name>/<secondary_name>/USER`

&nbsp;

Use https://regexr.com to check your strings.

⚠️ User containers can only have `USER` as the data tier. The dataset name shall conform to following regex defined in [CMSRucio schema](https://github.com/dmwm/CMSRucio/blob/8e0c3b9c69a11f1ac74865524e7c2f82f9326a1f/src/policy/CMSRucioPolicy/schema.py#L60).

&nbsp;

`rucio add-dataset <scope>:<dataset_pattern>`

`rucio add-container <scope>:<container_pattern>`

&nbsp;

```shell
[alikaan.gueven@clip]$ rucio list-dids user.aguven:*
+--------------------------------------------------------------+--------------+
| SCOPE:NAME                                                   | [DID TYPE]   |
|--------------------------------------------------------------+--------------|
| user.aguven:/MET/Run2018/USER                                | CONTAINER    |
| user.aguven:/Production/TEST.METRun2017E/USER#0001           | DATASET      |
| user.aguven:/Production/TEST.RunIISummer20UL17RECO/USER#0001 | DATASET      |
| user.aguven:/SDV/Run2023_data/USER                           | CONTAINER    |
| user.aguven:/SDV/missingRun2023data/USER                     | CONTAINER    |
+--------------------------------------------------------------+--------------+
```

*did= data identifier (i.e. container, dataset, single file)*

### Check Quota

```shell
[alikaan.gueven@clip]$ rucio list-account-limits aguven
+--------------+----------+
| RSE          | LIMIT    |
|--------------+----------|
| T2_AT_Vienna | 2.000 TB |
+--------------+----------+

[alikaan.gueven@clip]$ rucio list-account-usage aguven
+-----------------+------------+----------+--------------+
| RSE             | USAGE      | LIMIT    | QUOTA LEFT   |
|-----------------+------------+----------+--------------|
| T1_IT_CNAF_Disk | 55.213 TB  | 0.000 B  | 0.000 B      |
| T1_UK_RAL_Disk  | 39.861 TB  | 0.000 B  | 0.000 B      |
| T2_AT_Vienna    | 95.749 GB  | 2.000 TB | 1.904 TB     |
| T2_IT_Rome      | 41.596 TB  | 0.000 B  | 0.000 B      |
+-----------------+------------+----------+--------------+
```

Even though I don't have any quota outside Vienna, I can still submit dataset replications to any site within CMS up to **50 TB** for single RSE and **500 TB** when RSEs are not specified.

**Replication Rule Example**

https://twiki.cern.ch/twiki/bin/view/CMS/TheRucioCLI

```shell
[alikaan.gueven@clip]$ rucio add-rule \
>     cms:/QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-PUAvg50ForMUOVal_102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM#e670b893-9a7c-4bce-b57f-c0b3849da228 \
>     1 \
>     'rse_type=DISK&cms_type=real\tier=3\tier=0' \
>     --lifetime 3500 \
>     --activity "User AutoApprove" \
>     --ask-approval

eb7577c4a08147b5a56d5e9cfb76ffe6


[alikaan.gueven@clip]$ rucio rule-info eb7577c4a08147b5a56d5e9cfb76ffe6
Id:                         eb7577c4a08147b5a56d5e9cfb76ffe6
Account:                    aguven
Scope:                      cms
Name:                       /QCD_Pt-1000toInf_MuEnrichedPt5_TuneCP5_13TeV_pythia8/RunIIAutumn18MiniAOD-PUAvg50ForMUOVal_102X_upgrade2018_realistic_v15_ext1-v1/MINIAODSIM#e670b893-9a7c-4bce-b57f-c0b3849da228
RSE Expression:             rse_type=DISK&cms_type=real\tier=3\tier=0
Copies:                     1
State:                      INJECT
Locks OK/REPLICATING/STUCK: 0/0/0
Grouping:                   DATASET
Expires at:                 2025-03-27 11:15:29
Locked:                     False
Weight:                     None
Created at:                 2025-03-27 10:17:09
Updated at:                 2025-03-27 10:17:09
Error:                      None
Subscription Id:            None
Source replica expression:  None
Activity:                   User AutoApprove
Comment:                    None
Ignore Quota:               True
Ignore Availability:        False
Purge replicas:             False
Notification:               NO
End of life:                None
Child Rule Id:              None
```

&nbsp;  
**\*\* More details:**  
[https://cmsdmops.docs.cern.ch/Users/Subscribe data/](https://cmsdmops.docs.cern.ch/Users/Subscribe%20data/)  
https://rucio.cern.ch/documentation/  
https://twiki.cern.ch/twiki/bin/viewauth/CMS/TheRucioCLI  
https://twiki.cern.ch/twiki/bin/view/CMS/Rucio

&nbsp;

### Attach a file to a dataset

```shell
[alikaan.gueven@clip]$ rucio add-dataset user.aguven:/Production/Run3_missingfiles/USER#0000
Added user.aguven:/Production/Run3_missingfiles/USER#0000

[alikaan.gueven@clip]$ rucio attach user.aguven:/Production/Run3_missingfiles/USER#0000 'cms:/store/data/Run2023B/JetMET1/AOD/19Dec2023-v1/80000/f5a7e8e1-80bb-4ea5-8a54-4a25193bd180.root'
DIDs successfully attached to user.aguven:/Production/Run3_missingfiles/USER#0000

[alikaan.gueven@clip]$ rucio list-content user.aguven:/Production/Run3_missingfiles/USER#0000 
+---------------------------------------------------------------------------------------------------+--------------+
| SCOPE:NAME                                                                                        | [DID TYPE]   |
|---------------------------------------------------------------------------------------------------+--------------|
| cms:/store/data/Run2023B/JetMET1/AOD/19Dec2023-v1/80000/f5a7e8e1-80bb-4ea5-8a54-4a25193bd180.root | FILE         |
+---------------------------------------------------------------------------------------------------+--------------+

[alikaan.gueven@clip]$ rucio list-files user.aguven:/Production/Run3_missingfiles/USER#0000 
+---------------------------------------------------------------------------------------------------+--------+-------------+------------+----------+
| SCOPE:NAME                                                                                        | GUID   | ADLER32     | FILESIZE   | EVENTS   |
|---------------------------------------------------------------------------------------------------+--------+-------------+------------+----------|
| cms:/store/data/Run2023B/JetMET1/AOD/19Dec2023-v1/80000/f5a7e8e1-80bb-4ea5-8a54-4a25193bd180.root | (None) | ad:9090d748 | 11.651 GB  |          |
+---------------------------------------------------------------------------------------------------+--------+-------------+------------+----------+
Total files : 1
Total size : 11.651 GB
```

**One cannot attach a file to a container!**

&nbsp;

## MISC

```
rucio delete-rule 8354a394981744e58546b411e45c648d

rucio update-rule 8354a394981744e58546b411e45c648d --lifetime 1
cat missingFilesRun2018D_part3.txt | xargs -I '{}' rucio attach user.aguven:/MET/Run2018D_missingFiles_part3/USER#0000 'cms:{}'
cat missingFilesRun2018D_part3.txt | xargs -I '{}' rucio attach user.aguven:/MET/Run2018D_missingFiles_part3/USER#0000 'cms:{}'
rucio add-rule user.aguven:/MET/Run2018D_missingFiles_part3/USER#0000 1 T2_AT_Vienna --source-replica-expression "T1_DE_KIT_Tape|T1_DE_KIT_Disk" --lifetime 1210000

rucio update-rule d13c8abbe6c140aeb54a98ecc24004b4 --lifetime 1
rucio list-rules --account aguven > tmp.txt
```

## Troubleshooting

If you experience any errors check here:

- Problem 1
```shell
[aguven@lxplus ~]$ rucio list-rules --account aguven > tmp.txt
2025-03-30 12:16:50,771	WARNING	This method is being deprecated. Please replace your command with `rucio rule list`
2025-03-30 12:16:50,872	ERROR	ConnectionError: HTTPSConnectionPool(host='cms-rucio-auth.cern.ch', port=443): Max retries exceeded with url: /auth/x509_proxy (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_CERTIFICATE_EXPIRED] ssl/tls alert certificate expired (_ssl.c:1129)')))
2025-03-30 12:16:50,882	ERROR	ConnectionError: HTTPSConnectionPool(host='cms-rucio-auth.cern.ch', port=443): Max retries exceeded with url: /auth/x509_proxy (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_CERTIFICATE_EXPIRED] ssl/tls alert certificate expired (_ssl.c:1129)')))
2025-03-30 12:16:50,895	ERROR	ConnectionError: HTTPSConnectionPool(host='cms-rucio-auth.cern.ch', port=443): Max retries exceeded with url: /auth/x509_proxy (Caused by SSLError(SSLError(1, '[SSL: SSLV3_ALERT_CERTIFICATE_EXPIRED] ssl/tls alert certificate expired (_ssl.c:1129)')))
2025-03-30 12:16:50,895	ERROR	Cannot connect to the Rucio server.
```
Solution 1
```shell
voms-proxy-init -rfc -voms cms -valid 192:0
```
