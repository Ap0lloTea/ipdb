import re
import subprocess
# import mysql.connector
import sqlite3
from optparse import OptionParser
import os

def GetAddress(sip, cursor):
    contorl = ["sd", "sc", "sb", "ed", "ec", "eb"]
    sql_abc_s = GetSqlS(GetABC(sip))
    sql_ab_s = GetSqlS(GetAB(sip))
    sql_a_s = GetSqlS(GetA(sip))
    sql_abc_e = GetSqlS(GetABC(sip))
    sql_ab_e = GetSqlS(GetAB(sip))
    sql_a_e = GetSqlS(GetA(sip))
    dic_sql = {"sd":sql_abc_s, "sc":sql_ab_s, "sb":sql_a_s, "ed":sql_abc_e, "ec":sql_ab_e, "eb":sql_a_e, }
    for i in contorl:
        sql = dic_sql.get(i)
        # print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) > 0:
            try:
                for j in range(len(data)):
                    if TIOO(str(data[j][0]), sip, str(data[j][1]), i):
                        address = str(data[j][2]) # CN
                        # address = str(data[j][3]) # EN
                        return address
            except Exception as e:
                print(e)
                return "Unknown "+i+" Error"


# Three in one operation
def TIOO(db_src, sip, db_dst, control):
    ipdb_src = SplitIP(str(db_src))
    ipdb_dst = SplitIP(str(db_dst))
    eqip = SplitIP(sip)
    # control value = a, b, c, d
    if 'b' in control:
        if int(ipdb_src[1]) <= int(eqip[1]) <= int(ipdb_dst[1]):
            return True
        else:
            return False
    elif 'c' in control:
        if int(ipdb_src[2]) <= int(eqip[2]) <= int(ipdb_dst[2]):
            return True
        else:
            return False
    elif 'd' in control:
        if int(ipdb_src[3]) <= int(eqip[3]) <= int(ipdb_dst[3]):
            return True
        else:
            return False
    else:
        return False


def SplitIP(ip):
    iplist = ip.split(".")
    return iplist

def GetA(sip):
    siplist = sip.split(".")
    a_str_ip = siplist[0]+"."
    return a_str_ip


def GetAB(sip):
    siplist = sip.split(".")
    a_str_ip = siplist[0]+"."+siplist[1]+"."
    return a_str_ip


def GetABC(sip):
    siplist = sip.split(".")
    a_str_ip = siplist[0]+"."+siplist[1]+"."+siplist[2]+"."
    return a_str_ip


def GetSqlS(atk_ip):
    sql = "select * from iprange where sip like '"+atk_ip+"%'"
    return sql


def GetSqlE(atk_ip):
    sql = "select * from iprange where eip like '"+atk_ip+"%'"
    return sql


def eqabcd(sip):
    sip = sip.split(".")
    try:
        for i in sip:
            eval(i)
        if len(sip) == 3:
            return "np"
        else:
            return "wr"
    except:
        return "wr"


# return list
def extract_ipv4_addresses(input_string):
    ipv4_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    ipv4_addresses = re.findall(ipv4_pattern, input_string)
    return ipv4_addresses


# return list
def extract_colon_prefixed_numbers(input_string):
    pattern = r':([1-9]|[1-9][0-9]{1,3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])\b'
    matches = re.findall(pattern, input_string)
    return matches


def run_command(command):
    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout
        else:
            return result.stderr
    except Exception as e:
        return str(e)


def main():
    # Check User input
    # parse = OptionParser(usage='python3 netstatL.py -o addressINFO.txt(default)')
    # parse.add_option('-o', '--outfile', dest='OutFile', default="netstat_tmp.txt", type='string', help='output file name')
    # options, args = parse.parse_args()

    # OutFileName = options.OutFile

    # # sqlite connect
    connection = sqlite3.connect('ipdb.db')
    cursor = connection.cursor()
    count = 0
    print("[+] DB connected.")
    # new_file = open(OutFileName, "a+", encoding="utf-8")
    # str
    netstat_output = run_command("netstat -nao")
    netstat_output_list = netstat_output.split("\n")
    for item in netstat_output_list:
        if len(extract_colon_prefixed_numbers(item)) == 2 and "UDP" not in item:
            ports = extract_colon_prefixed_numbers(item)
            # print(item)
            addresses = extract_ipv4_addresses(item)
            if addresses[1] == "127.0.0.1":
                print(item)
                continue
            remote_location = str(GetAddress(addresses[1], cursor)).strip("\n")
            addresses[1] = addresses[1]+":"+ports[1]
            item = item.replace(addresses[1],addresses[1]+"["+remote_location+"]")
            print(item)
        else:
            print(item)
    # new_file.close()
    connection.close()
    print("[+] SQLite Connection closed.")


if __name__ == "__main__":
    main()

