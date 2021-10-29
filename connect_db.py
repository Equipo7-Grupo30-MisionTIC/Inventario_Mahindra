import sqlite3

URL_BD="static/db/MahindraInv.db"

def consulta_sel(sql) -> list:
    try:
        with sqlite3.connect(URL_BD) as con:  
            cursor=con.cursor()               
            sal=cursor.execute(sql).fetchall() 
    except Exception as ex:
        sal= None
    return sal


def consulta_acc(sql, datos) -> int:
    try:
        with sqlite3.connect(URL_BD) as con:  
            cursor=con.cursor()               
            sal=cursor.execute(sql, datos).rowcount  
            if sal!=0:
                con.commit()                   
    except Exception as ex:
        sal=0
    return sal
    