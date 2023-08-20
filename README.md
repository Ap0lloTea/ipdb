# ipdb: ip address to location (like country and city, ipv4 only)

[Chinese](https://github.com/Ap0lloTea/ipdb/edit/main/READMEcn.md)

This used to be my company's project.

I had a setback and wanted to start over.

So I choose to upload this project.

# SqlLite version(ipdb.db)

temporary use

unzip ipdb.zip you can get ipdb.db (Github max upload file size is 25mb)

write ip list in ip.txt

just run ipdb2.py

result in addressINFO.txt

# MySQL: for your service

install mysql(Google Search)

Modify database login restrictions and access restrictions

import iplist.xlsx in database

change the table name against the database or script (default table name:iprange)

pip install mysql-connector-python

or

pip3 install mysql-connector-python

write database account in ipdb.py

write ip list in ip.txt

run ipdb.py:

python ipdb.py

python3 ipdb.py

python script can create a new file(addressINFO.txt)

this file can save result (ip \t address)

you can change 2 you like result ,just edit ipdb.py

sorry this version only chinese

