import sqlite3

URL_BD="bdc0310.db"

def consulta_sel(sql) -> list:
    try:
        with sqlite3.connect(URL_BD) as con:  #conexión a la base de datos
            cursor=con.cursor()               # Crea un area temporal para manejo     
            sal=cursor.execute(sql).fetchall()  # Ejecutando la consulta y recuperando los resultados
    except Exception as ex:
        sal= None
    return sal


def consulta_acc(sql, datos) -> int:
    try:
        with sqlite3.connect(URL_BD) as con:  #conexión a la base de datos
            cursor=con.cursor()               # Crea un area temporal para manejo     
            sal=cursor.execute(sql, datos).rowcount  # Ejecutando la consulta y recuperando los resultados
            if sal!=0:
                con.commit()                   # Asegura los cambios en la base de datos
    except Exception as ex:
        sal=0
    return sal
    