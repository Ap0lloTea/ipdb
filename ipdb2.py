# import mysql.connector
import sqlite3
connection = sqlite3.connect('ipdb.db')
# connection = mysql.connector.connect(
#     host="",
#     user="root",
#     password="",
#     database="ipdb"
# )
cursor = connection.cursor()


def GetAddress(sip):
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
                        address = str(data[j][2])
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

def main():
    count = 0
    ip_file = open("ip.txt", "r+", encoding="utf-8")
    new_file = open("addressINFO.txt", "a+", encoding="utf-8")
    for i in ip_file.readlines():
        if count % 100 == 0:
            print("Now"+str(count))
        i = i.strip()
        address = str(GetAddress(i)).strip("\n")
        write_data = i + "\t" + address + "\n"
        new_file.write(write_data)
        count += 1
    ip_file.close()
    new_file.close()


main()

# if connection.is_connected():
    # cursor.close()
connection.close()
print("Connection closed")