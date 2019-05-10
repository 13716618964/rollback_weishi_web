import pymysql

def mysql_info(sql,fetch):
    db = pymysql.connect('192.168.1.16', 'root', 'Lxq_204389', 'web_rollback', port=3306, charset='utf8')
    dbc = db.cursor()
    dbc.execute(sql)
    if fetch == 'one' :
        data=dbc.fetchone()
    else:
        data=dbc.fetchall()
    dbc.close()
    db.close()
    return data

def mysql_write(sql):
    db = pymysql.connect('192.168.1.16', 'root', 'Lxq_204389', 'web_rollback', port=3306, charset='utf8')
    dbc = db.cursor()
    try:
        stat=dbc.execute(sql)
        print(stat)
    except:
        return False
    else:
        if stat != 1:
            return False
        db.commit()
        dbc.close()
        db.close()
        return True


def concurrent_test():
    db = pymysql.connect('192.168.1.16', 'root', 'Lxq_204389', 'web_rollback', port=3306, charset='utf8')
    dbc = db.cursor()
    sql='''update t_add_num set num=num+1 where key_words ='concurrent' '''
    try:
        stat=dbc.execute(sql)
        print(stat)
    except:
        return False
    else:
        if stat != 1:
            return False
        db.commit()
        dbc.close()
        db.close()
        return True
