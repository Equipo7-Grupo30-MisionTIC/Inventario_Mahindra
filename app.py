from flask import Flask, render_template, redirect, session, request, jsonify
from markupsafe import escape
import os
from os import remove
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from werkzeug.utils import secure_filename
from security import login_valido, pass_valido
from connect_db import consulta_acc, consulta_sel
from formularios import Login, ModificarProveedor, ModificarUsuario, Registro, CrearProducto, BuscarProducto, BuscarUsuario, ModificarProducto, BuscarProveedor, RegistroProveedor
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key= os.urandom(24)

@app.route('/', methods=['GET','POST'])
def login():
    frm=Login()
    if request.method=='GET':
        session.clear()
        return render_template('index.html',form=frm, titulo="LOGIN" )
    else:
        usu=escape(request.form["usr"])
        pwd=escape(request.form["pwd"])
        if len(usu.strip())==0 or usu==None or not login_valido(usu):
            return """<script>var r = confirm("ERROR: Debe suministrar un usuario valido.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
        if len(pwd.strip())==0 or pwd==None or not pass_valido(pwd):
            return """<script>var r = confirm("ERROR: Debe suministrar una clave valida.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
        sql= "SELECT nombre, documento, tipo_usuario, contraseña FROM Usuario WHERE id_usuario='{}'".format(usu)
        res= consulta_sel(sql)
        try:
            if len(res)>0:
                cbd=res[0][3]
            check_password_hash(cbd,pwd)
        except UnboundLocalError as ue:
            return """<script>var r = confirm("ERROR: Usuario no existente en el sistema. Intente de nuevo.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if check_password_hash(cbd,pwd):
            session.clear()
            session["nom"]=res[0][0]
            session["doc"]=res[0][1]
            session["usr"]=usu
            session["pwd"]=pwd
            session["tipo"]=res[0][2]
            return redirect("/principal/")
        else:
            return """<script>var r = confirm("ERROR: Usuario o clave invalidos.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""

@app.route('/principal/')
def principal():
    try:
        usu=session["nom"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    return render_template('principal.html', titulo=usu)

@app.route('/dashboard/')
def dashboard_administrativo():
    try:
        usu=session["nom"]
        rol=session["tipo"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    #GRAFICA IZQUIERDA ARRIBA
    if rol==2 or rol==1:
        plt.clf()
        sql2= "SELECT cod_prod, cant_min, cant_disp FROM Producto"
        res2= consulta_sel(sql2)
        resultcod=[]
        resultmin=[]
        resultdisp=[]
        for i in range(len(res2)):
            if (res2[i][2]<res2[i][1])==True:
                resultcod.append(res2[i][0])
                resultmin.append(res2[i][1])
                resultdisp.append(res2[i][2])
            else:
                continue
        serie_1 = resultmin
        serie_2 = resultdisp
        numero_de_grupos = len(serie_1)
        indice_barras = np.arange(numero_de_grupos)
        ancho_barras =0.35
        plt.bar(indice_barras, serie_1, width=ancho_barras, label='Cantidad minima')
        plt.bar(indice_barras + ancho_barras, serie_2, width=ancho_barras, label='Cantidad disponible')
        plt.legend(loc='best')
        plt.xticks(indice_barras + ancho_barras, resultcod)
        plt.ylabel('Unidades')
        plt.xlabel('Codigo del producto')
        plt.title('Productos con alerta: cantidad disponible por debajo de la minima')
        plt.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
        plt.savefig('static/figures/new_plot.png')
        #GRAFICA DERECHA
        sql5= "SELECT cod_prod FROM Producto"
        res5= consulta_sel(sql5)
        codprod=[]
        for i in range(len(res5)):
            str = ','.join(res5[i])
            codprod.append(str)
        sql8= "SELECT id_producto FROM Transaccion WHERE tipo_trans=1"
        res8= consulta_sel(sql8)
        id_ventas=[]
        for i in range(len(res8)):
            str = ','.join(res8[i])
            id_ventas.append(str)
        cars1=[]
        data1=[]
        for i in range(len(codprod)):
            cars1.append(codprod[i])
            data1.append(id_ventas.count(codprod[i]))
        mayorventa=data1.index(max(data1))
        automovil_masvendido=cars1[mayorventa]
        fig1, ax1 = plt.subplots()
        data_graph=[]
        cars_graph=[]
        for i in range (len(data1)):
            if data1[i]==0:
                continue
            if data1[i]!=0:
                data_graph.append(data1[i])
                cars_graph.append(cars1[i])
        ax1.pie(data_graph, labels=cars_graph, autopct='%1.1f%%',shadow=True, startangle=90)
        ax1.axis('equal')
        plt.title('Carros mas vendidos del Inventario Mahindra Mahindra')
        plt.savefig('static/figures/third_plot.png')
        #GRAFICA IZQUIERDA ABAJO
        sql9= "SELECT id_usuario FROM Usuario"
        res9= consulta_sel(sql9)
        codusr=[]
        for i in range(len(res9)):
            str = ','.join(res9[i])
            codusr.append(str)
        sql10= "SELECT id_usuario FROM Transaccion WHERE tipo_trans=1"
        res10= consulta_sel(sql10)
        id_ventas=[]
        for i in range(len(res10)):
            str = ','.join(res10[i])
            id_ventas.append(str)
        usr=[]
        ventas=[]
        for i in range(len(codusr)):
            usr.append(codusr[i])
            ventas.append(id_ventas.count(codusr[i]))
        fig, ax = plt.subplots()
        ax.plot(usr, ventas, marker = 'o')
        plt.grid(axis = 'y', color = 'gray', linestyle = 'dashed')
        plt.title('Indice de ventas por usuario')
        plt.savefig('static/figures/second_plot.png')
        return render_template('dashboard.html', total_actual=len(res8), auto_masvendido=automovil_masvendido, titulo=usu)
    else:
        return """<script>var r = confirm("AVISO: Usted no tiene permisos para acceder a esta area. Requiere permisos de administrador.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""

@app.route('/usuarios/',methods=['GET','POST'])
def usuarios():
    try:
        usu=session["nom"]
        rol=session["tipo"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    if rol==2 or rol==1:
        frm=BuscarUsuario()
        if request.method=='GET':
            return render_template('usuarios.html', form=frm, titulo=usu)
        else:
            numdocusr=escape(request.form["numdocusr"])
            codusr=escape(request.form["codusr"])
            if len(numdocusr.strip())==0 or numdocusr=="0":
                return """<script>var r = confirm("ERROR: Debe suministrar un documento de identificación valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            try:
                numdoc=int(numdocusr)
            except ValueError as ve:
                return """<script>var r = confirm("ERROR: Debe suministrar un documento de identificación valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if len(codusr.strip())==0 or codusr=="0" or not login_valido(codusr) :
                return """<script>var r = confirm("ERROR: Debe suministrar un usuario valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            session["codusr"]=codusr
            sql= "SELECT nombre, telefono, direccion, tipo_usuario, id_estado FROM Usuario WHERE documento={} AND id_usuario='{}'".format(numdocusr,codusr)
            res= consulta_sel(sql)
            try:
                nom=res[0][0]
                numerodoc=numdocusr
                telf=res[0][1]
                direcc=res[0][2]
                usr=codusr
                roluser=""
                estad=""
                if res[0][3]==1:
                    roluser="Superadministrador"
                if res[0][3]==2:
                    roluser="Administrador"
                if res[0][3]==3:
                    roluser="Usuario final"
                if res[0][4]==1:
                    estad="Activo"
                if res[0][4]==2:
                    estad="Inactivo"
            except IndexError as ie:
                return """<script>var r = confirm("ERROR: Debe suministrar un usuario o documento de identificación valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            except TypeError as te:
                return """<script>var r = confirm("ERROR: Intentelo de nuevo. Verifique los datos ingresados");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            return render_template('usuarios.html', form=frm,nom=nom,numerodoc=numerodoc,telf=telf, direcc=direcc, usr=usr, rolusr=roluser, estd=estad, titulo=usu)
    else:
        return """<script>var r = confirm("AVISO: Usted no tiene permisos para acceder a esta area. Requiere permisos de administrador.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""

@app.route('/crearusuario/', methods=['GET','POST'])
def crear_usuario(): 
    try:
        usu=session["nom"]
        rol=session["tipo"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    if rol==2 or rol==1:
        frm=Registro()
        if request.method =="GET":
            return render_template("crearUsuario.html", form=frm, titulo=usu)
        else:
            nom=escape(request.form["nom"])
            numdoc=escape(request.form["numdoc"])
            direc=escape(request.form["direcc"])
            tel=escape(request.form["telf"])
            codusr=escape(request.form["codusr"])
            pwdusr=escape(request.form["pwda"])
            tipoUsr=int(escape(request.form["selct1"]))
            estdUsr=int(escape(request.form["selct2"]))
            adj1=frm.adj1.data
            if adj1==None:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar una imagen valida.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            nim=secure_filename(adj1.filename)
            rim=f"static/users/{nim}"
            if rim!=f"static/users/{codusr}.jpg":
                swerror=True
                return """<script>var r = confirm("ERROR: La imagen a guardar debe estar nombrada con el nombre de usuario asignado y estar en formato jpg.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            else:
                adj1.save(rim)
            swerror=False
            if nom==None or len(nom)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar un nombre de usuario.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if codusr==None or len(codusr)==0 or not login_valido(codusr):
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar un usuario valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if pwdusr==None or len(pwdusr)==0 or not pass_valido(pwdusr):
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar una clave valida.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if pwdusr==codusr:
                swerror=True
                return """<script>var r = confirm("ERROR: El codigo de usuario no puede ser la clave.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if tipoUsr==None or tipoUsr==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe seleccionar un tipo de usuario.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if tipoUsr==2 and rol==2:
                swerror=True
                return """<script>var r = confirm("AVISO: No tiene permisos para asignar a otro administrador. Usted solo puede gestionar usuarios finales.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if estdUsr==None or estdUsr==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe seleccionar un tipo de estado.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if not swerror:
                sql= "INSERT INTO Usuario (id_usuario, nombre, documento, direccion, telefono, tipo_usuario, contraseña, id_estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
                pwd= generate_password_hash(pwdusr)
                res=consulta_acc(sql,(codusr,nom,numdoc,direc,tel,tipoUsr,pwd,estdUsr))
                if res!=0:
                    return """<script>var r = confirm("¡Datos correctamente guardados!.");if (r == true) {location.href='/crearusuario/';} else {location.href='/crearusuario/';}</script>"""
                else:
                    return """<script>var r = confirm("ERROR: Por favor reintente.Verifique los datos ingresados");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            return render_template("crearUsuario.html", form=frm, titulo=usu)
    else:
        return """<script>var r = confirm("AVISO: Usted no tiene permisos para acceder a esta area. Requiere permisos de administrador.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""              

@app.route('/modificarusuario/', methods=['GET','POST'])
def modif_usuario():
    try:
        usu=session["nom"]
        rol=session["tipo"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    if rol==2 or rol==1:
        try:
            codusr=session["codusr"]
        except KeyError as ke:
            return """<script>var r = confirm("ERROR: Para modificar un usuario, debe haberlo buscado primero. Será redirigido a la página de usuarios.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        frm=ModificarUsuario()
        if request.method=='GET':
            sql= "SELECT nombre, documento, telefono, direccion FROM Usuario WHERE id_usuario='{}'".format(codusr)
            res= consulta_sel(sql) 
            try:
                nombre=res[0][0]
                numdoc=res[0][1]
                tel=res[0][2]
                direc=res[0][3]
                codigousr=codusr
                return render_template('modificarUsuario.html', form=frm,nombre=nombre,numdoc=numdoc,tel=tel, direc=direc, codusr=codigousr,titulo=usu)
            except IndexError as ie:
                return """<script>var r = confirm("ERROR: No puede regresar a esta pagina desde aqui. Ingrese desde usuarios y coloque el codigo del que desea modificar");if (r == true) {location.href = "/usuarios/";} else {location.href = "/usuarios/";}</script>"""
        else:
            if frm.btnedt.data==True:
                nom=escape(request.form["nom"])
                numdoc=escape(request.form["numdoc"])
                direc=escape(request.form["direcc"])
                tel=escape(request.form["telf"])
                codusr=escape(request.form["codusr"])
                pwdusr=escape(request.form["pwda"])
                tipoUsr=int(escape(request.form["selct1"]))
                estdUsr=int(escape(request.form["selct2"]))
                adj1=frm.adj1.data
                if adj1==None:
                    swerror=True
                    return """<script>var r = confirm("ERROR: Debe suministrar una imagen valida.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                nim=secure_filename(adj1.filename)
                rim=f"static/users/{nim}"
                if rim!=f"static/users/{codusr}.jpg":
                    swerror=True
                    return """<script>var r = confirm("ERROR: La imagen a guardar debe estar nombrada con el nombre de usuario asignado y estar en formato jpg.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                else:
                    adj1.save(rim)
                swerror=False
                if nom==None or len(nom)==0:
                    swerror=True
                    return """<script>var r = confirm("ERROR: Debe suministrar un nombre de usuario.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                if codusr==None or len(codusr)==0 or not login_valido(codusr):
                    swerror=True
                    return """<script>var r = confirm("ERROR: Debe suministrar un usuario valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                if pwdusr==None or len(pwdusr)==0 or not pass_valido(pwdusr):
                    swerror=True
                    return """<script>var r = confirm("ERROR: Debe suministrar una clave valida.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                if pwdusr==codusr:
                    swerror=True
                    return """<script>var r = confirm("ERROR: El codigo de usuario no puede ser la clave.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                if tipoUsr==None or tipoUsr==0:
                    swerror=True
                    return """<script>var r = confirm("ERROR: Debe seleccionar un tipo de usuario.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                if tipoUsr==2 and rol==2:
                    swerror=True
                    return """<script>var r = confirm("AVISO: No tiene permisos para asignar a otro administrador. Usted solo puede gestionar usuarios finales.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                if estdUsr==None or estdUsr==0:
                    swerror=True
                    return """<script>var r = confirm("ERROR: Debe seleccionar un tipo de estado.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                if not swerror:
                    sql= "UPDATE Usuario SET id_usuario=?, nombre=?, documento=?, direccion=?, telefono=?, tipo_usuario=?, contraseña=?, id_estado=? WHERE id_usuario=? "
                    pwd= generate_password_hash(pwdusr)
                    res=consulta_acc(sql,(codusr,nom,numdoc,direc,tel,tipoUsr,pwd,estdUsr,codusr))
                    if res!=0:
                        return """<script>var r = confirm("¡Datos correctamente editados!.");if (r == true) {location.href='/usuarios/';} else {location.href='/usuarios/';}</script>"""
                    else:
                        return """<script>var r = confirm("ERROR: Por favor reintente. Si ha verificado que los datos son validos y esta intentado editar el codigo unico de usuario, puede que no sea posible por su relación con otros registros de la base de datos. Dado esto, considere editar los registros relacionados.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
                return render_template("modificarUsuario.html", form=frm, titulo=usu)
            if frm.btnelim.data==True:
                codusr=escape(request.form["codusr"])
                numdoc=escape(request.form["numdoc"])
                sql= "DELETE FROM Usuario WHERE id_usuario=? AND documento=?"
                res=consulta_acc(sql,(codusr,numdoc))
                if res!=0:
                    remove(f"static/users/{codusr}.jpg")
                    return """<script>var r = confirm("¡Datos correctamente eliminados!.");if (r == true) {location.href='/usuarios/';} else {location.href='/usuarios/';}</script>"""
                else:
                    return """<script>var r = confirm("ERROR: Por favor reintente.Si ha verificado que los datos son validos y esta intentado eliminar el codigo unico de usuario, puede que no sea posible por su relación con otros registros de la base de datos. Dado esto, considere editar los registros relacionados.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            return render_template("modificarUsuario.html", form=frm, titulo=usu)
    else:
        return """<script>var r = confirm("AVISO: Usted no tiene permisos para acceder a esta area. Requiere permisos de administrador.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""              

@app.route('/productos/', methods=['GET','POST'])
def productos():
    try:
        usu=session["nom"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    frm=BuscarProducto()
    if request.method=='GET':
        return render_template('productos.html', form=frm, titulo=usu)
    else:
        codprod=escape(request.form["codprobs"])
        if len(codprod.strip())==0 or codprod=="0":
            return """<script>var r = confirm("ERROR: Debe suministrar un código valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        sql= "SELECT nombre_prod, descripcion, cant_disp FROM Producto WHERE cod_prod='{}'".format(codprod)
        res= consulta_sel(sql)
        sql2= "SELECT cod_prov FROM Proveedor WHERE cod_prod='{}'".format(codprod)
        res2= consulta_sel(sql2)
        session["codprod"]=codprod
        id_prov=[]
        for i in range(len(res2)):
            str = ','.join(res2[i])
            id_prov.append(str)
        try:
            cod=codprod
            nomprod=res[0][0]
            descr=res[0][1]
            cantdis=res[0][2]
            prov=id_prov
            session["codprod"]=escape(request.form["codprobs"])
        except IndexError as ie:
            return """<script>var r = confirm("ERROR: Debe suministrar un código valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        return render_template('productos.html', form=frm,codigo=cod,nomprod=nomprod,descripcion=descr,cantdis=cantdis,prov=prov, titulo=usu)

@app.route('/crearproducto/', methods=['GET','POST'])
def crear_producto():
    try:
        usu=session["nom"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    frm=CrearProducto()
    if request.method=='GET':
        return render_template('crearProducto.html',form=frm, titulo=usu)
    else:    
        codprov=escape(request.form["codprov"])
        nomprod=escape(request.form["nomprod"])
        descr=escape(request.form["descr"])
        codunq=escape(request.form["codunq"])
        cantmin=escape(request.form["cantmin"])
        cantdisp=escape(request.form["cantdisp"])
        estprod=escape(request.form["selectestd"])
        adj=frm.adj.data
        if adj==None:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar una imagen valida.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        nim=secure_filename(adj.filename)
        rim=f"static/uploads/{nim}"
        if rim!=f"static/uploads/{codunq}.jpg":
            swerror=True
            return """<script>var r = confirm("ERROR: La imagen a guardar debe estar nombrada con el codigo unico del producto  y estar en formato jpg.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        else:
            adj.save(rim)
        swerror=False
        if codprov==None or len(codprov)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar un codigo de proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if codprov!=None or codprov!=0:
            sql= "SELECT cod_prov FROM Proveedor WHERE cod_prov='{}'".format(codprov)
            res=consulta_sel(sql)
            if res==[]:
                swerror=True
                return """<script>var r = confirm("ERROR: El codigo de proveedor no fue encontrado en la base de datos. Intente con mayusculas. En caso contrario, registre el proveedor o contactese con el administrador. Si esta intentando ingresar mas de un proveedor, recuerde registrar el codigo del producto al registrar al proveedor");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if nomprod==None or len(nomprod)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar un nombre de producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if descr==None or len(descr)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar una descripcion.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if codunq==None or len(codunq)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar el codigo unico del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if cantmin==None or len(cantmin)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar la cantidad minima del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if cantdisp==None or len(cantdisp)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar la cantidad disponible del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if estprod==None or len(estprod)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe confirmar el estado del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if not swerror:
            sql= "INSERT INTO Producto (cod_prod, id_proveedor, nombre_prod, descripcion, cant_min, cant_disp, id_estado) VALUES (?, ?, ?, ?, ?, ?, ?)"
            res=consulta_acc(sql,(codunq,codprov,nomprod,descr,cantmin,cantdisp,estprod))
            if res!=0:
                return """<script>var r = confirm("¡Datos correctamente guardados!.");if (r == true) {location.href='/crearproducto/';} else {location.href='/crearproducto/';}</script>"""
            else:
                return """<script>var r = confirm("ERROR: Por favor reintente.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        return render_template("crearProducto.html", form=frm, titulo=usu)

@app.route('/modificarproducto/', methods=['GET','POST'])
def modif_producto():
    try:
        usu=session["nom"]
        rol=session["tipo"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    try:
        codprod=session["codprod"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Para modificar un producto, debe haberlo buscado primero. Será redirigido a la página de productos.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
    frm=ModificarProducto()
    if request.method=='GET':
        sql= "SELECT id_proveedor, nombre_prod, descripcion, cant_min, cant_disp FROM Producto WHERE cod_prod='{}'".format(codprod)
        res= consulta_sel(sql) 
        try:
            codprov=res[0][0]
            nomprod=res[0][1]
            frm.descr.data=res[0][2]
            print(frm.descr.data)
            cantmin=res[0][3]
            cantdisp=res[0][4]
            codigoprod=codprod
            return render_template('modificarProducto.html', form=frm,codprov=codprov,nombreprod=nomprod, codunico=codigoprod, cantidminima=cantmin,cantidispo=cantdisp,titulo=usu)
        except IndexError as ie:
            return """<script>var r = confirm("ERROR: No puede regresar a esta pagina desde aqui. Ingrese desde productos y coloque el codigo del que desea modificar");if (r == true) {location.href = "/productos/";} else {location.href = "/productos/";}</script>"""
    else:
        if frm.btneditar.data==True:
            codprov=escape(request.form["codprov"])
            nomprod=escape(request.form["nomprod"])
            descr=escape(request.form["descr"])
            print(descr)
            codunq=escape(request.form["codunq"])
            cantmin=escape(request.form["cantmin"])
            cantdisp=escape(request.form["cantdisp"])
            estprod=escape(request.form["selectestd"])
            adj=frm.adj.data
            if adj==None:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar una imagen valida.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            nim=secure_filename(adj.filename)
            rim=f"static/uploads/{nim}"
            if rim!=f"static/uploads/{codunq}.jpg":
                swerror=True
                return """<script>var r = confirm("ERROR: La imagen a guardar debe estar nombrada con el codigo unico del producto  y estar en formato jpg.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            else:
                adj.save(rim)
                swerror=False
            if codprov==None or len(codprov)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar un codigo de proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if codprov!=None or codprov!=0:
                sql= "SELECT cod_prov FROM Proveedor WHERE cod_prov='{}'".format(codprov)
                res=consulta_sel(sql)
                if res==[]:
                    swerror=True
                    return """<script>var r = confirm("ERROR: El codigo de proveedor no fue encontrado en la base de datos. Intente con mayusculas. En caso contrario, registre el proveedor o contactese con el administrador. Si esta intentando ingresar mas de un proveedor, recuerde registrar el codigo del producto al registrar al proveedor");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if nomprod==None or len(nomprod)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar un nombre de producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if descr==None or len(descr)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar una descripcion.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if codunq==None or len(codunq)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar el codigo unico del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if cantmin==None or len(cantmin)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar la cantidad minima del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if cantdisp==None or len(cantdisp)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar la cantidad disponible del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if estprod==None or len(estprod)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe confirmar el estado del producto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if not swerror:
                sql= "UPDATE Producto SET cod_prod=?, id_proveedor=?, nombre_prod=?, descripcion=?, cant_min=?, cant_disp=?, id_estado=? WHERE cod_prod=?"
                res=consulta_acc(sql,(codunq,codprov,nomprod,descr,cantmin,cantdisp,estprod,codunq))
                if res!=0:
                    return """<script>var r = confirm("¡Datos correctamente editados!.");if (r == true) {location.href='/productos/';} else {location.href='/productos/';}</script>"""
                else:
                    return """<script>var r = confirm("ERROR: Por favor reintente. Si ha verificado que los datos son validos y esta intentado modificar el codigo unico de producto, puede que no sea posible por su relación con otros registros de la base de datos. Dado esto, considere editar los registros relacionados");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            return render_template("modificarProducto.html", form=frm, titulo=usu)
        if frm.btneliminar.data==True:
            codunq=escape(request.form["codunq"])
            nomprod=escape(request.form["nomprod"])
            sql= "DELETE FROM Producto WHERE cod_prod=? AND nombre_prod=?"
            res=consulta_acc(sql,(codunq,nomprod))
            if res!=0:
                remove(f"static/uploads/{codunq}.jpg")
                return """<script>var r = confirm("¡Datos correctamente eliminados!.");if (r == true) {location.href='/productos/';} else {location.href='/productos/';}</script>"""
            else:
                return """<script>var r = confirm("ERROR: Por favor reintente.Si ha verificado que los datos son validos y esta intentado eliminar el codigo unico de producto, puede que no sea posible por su relación con otros registros de la base de datos. Dado esto, considere editar los registros relacionados.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        return render_template("modificarProducto.html", form=frm, titulo=usu)
    
    
@app.route('/productos_lista_proveedores/')
def lista_proveedores():
    try:
        codprod=session["codprod"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Para generar la lista de proveedores del producto, debe buscar el producto en cuestion dando el codigo correspondiente.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
    sql2= "SELECT * FROM Proveedor WHERE cod_prod='{}'".format(codprod)
    res2= consulta_sel(sql2)
    result=[]
    result.append(f"----INVENTARIO MAHINDRA MAHINDRA - PROVEEDORES DEL PRODUCTO CODIGO {codprod}")
    for i in range(len(res2)):
        j=0
        result.append("--------------------")
        result.append("Codigo proveedor: "+res2[i][j])
        j+=1
        result.append("Nombre: "+res2[i][j])
        j+=1
        result.append("Descripcion: "+res2[i][j])
        j+=1
        result.append("NIT: "+str(res2[i][j]))
        j+=1
        result.append("Direccion: "+res2[i][j])
        j+=1
        result.append("Telefono: "+res2[i][j])
        j+=1
        result.append("Nombre de contacto: "+res2[i][j])
        j+=1
        if res2[i][j]==1:
                estad="Activo"
        if res2[i][j]==2:
                estad="Inactivo"
        result.append("Id estado: "+estad)
        j+=1
        result.append("Codigo producto: "+res2[i][j])
        result.append("--------------------")
    result.append("----PARA VOLVER A LA PAGINA ANTERIOR, DE CLICK DOS VECES AL BOTON ANTERIOR DE SU NAVEGADOR O PULSE ALT+FLECHA IZQUIERDA DOS VECES-------")
    return jsonify(result)

@app.route('/productos_alerta_cantminima/')
def listar_cantidadminima():
    sql2= "SELECT cod_prod, nombre_prod, cant_min, cant_disp FROM Producto"
    res2= consulta_sel(sql2)
    result=[]
    result.append("----INVENTARIO MAHINDRA MAHINDRA - ALERTA DE PRODUCTOS DEBAJO DE CANTIDAD MINIMA-----")
    for i in range(len(res2)):
        if (res2[i][3]<res2[i][2])==True:
            result.append("--------------------")
            result.append("Codigo producto: "+res2[i][0])
            result.append("Nombre producto: "+res2[i][1])
            result.append("Cantidad minima: "+str(res2[i][2]))
            result.append("Cantidad disponible: "+str(res2[i][3]))
            result.append("--------------------")
        else:
            continue
    result.append("----PARA VOLVER A LA PAGINA ANTERIOR, DE CLICK UNA VEZ AL BOTON ANTERIOR DE SU NAVEGADOR O PULSE ALT+FLECHA IZQUIERDA UNA VEZ-------")
    return jsonify(result)

@app.route('/proveedores/',methods=['GET','POST'])
def proveedores():
    try:
        usu=session["nom"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    frm=BuscarProveedor()
    if request.method=='GET':
        return render_template('proveedores.html', form=frm, titulo=usu)
    else:
        codprov=escape(request.form["codprov"])
        if len(codprov.strip())==0 or codprov=="0":
            return """<script>var r = confirm("ERROR: Debe suministrar un codigo de proveedor valido.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        sql= "SELECT nombre, nit, descripcion, direccion, nombre_contacto, telefono, id_estado FROM Proveedor WHERE cod_prov='{}'".format(codprov)
        res= consulta_sel(sql)
        session["codprov"]=codprov
        try:
            cod=codprov
            nom=res[0][0]
            nit=res[0][1]
            descr=res[0][2]
            direcc=res[0][3]
            nomcontact=res[0][4]
            telf=res[0][5]
            estad=""
            if res[0][6]==1:
                estad="Activo"
            if res[0][6]==2:
                estad="Inactivo"
            if res[0][6]==3:
                estad="Bloqueado"
        except IndexError as ie:
            return """<script>var r = confirm("ERROR: Debe suministrar un código valido. Este no existe o es posible que este en mayusculas.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        except TypeError as te:
            return """<script>var r = confirm("ERROR: Intentelo de nuevo.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        return render_template('proveedores.html', form=frm,codprov=cod,nom=nom,nit=nit, descr=descr, direcc=direcc, nomcontact=nomcontact, telf=telf, estd=estad, titulo=usu)

@app.route('/crearproveedor/', methods=['GET','POST'])
def crear_proveedor():
    try:
        usu=session["nom"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    frm=RegistroProveedor()
    if request.method=='GET':
        return render_template('crearProveedor.html', form=frm, titulo=usu)
    else:
        nomprov=escape(request.form["nom"])
        codprov=escape(request.form["codprov"])
        direcc=escape(request.form["direcc"])
        nit=escape(request.form["nit"])
        descr=escape(request.form["descr"])
        telf=escape(request.form["telf"])
        prscon=escape(request.form["prscon"])
        estd=escape(request.form["estd"])
        codprodunq=escape(request.form["codprod"])
        swerror=False
        if nomprov==None or len(nomprov)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar un nombre de proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if codprov==None or len(codprov)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar un codigo de proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if direcc==None or len(direcc)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar una direccion.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if nit==None or len(nit)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar el NIT del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if descr==None or len(descr)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar una descripcion del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if telf==None or len(telf)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar el telefono del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if prscon==None or len(prscon)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe suministrar la persona de contacto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if estd==None or len(estd)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe confirmar el estado del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if codprodunq==None or len(codprodunq)==0:
            swerror=True
            return """<script>var r = confirm("ERROR: Debe confirmar el codigo del producto asociado.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        if not swerror:
            sql= "INSERT INTO Proveedor (cod_prov, nombre, descripcion, nit, direccion, telefono, nombre_contacto, id_estado, cod_prod) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            res=consulta_acc(sql,(codprov,nomprov,descr,nit,direcc,telf,prscon,estd,codprodunq))
            if res!=0:
                return """<script>var r = confirm("¡Datos correctamente guardados!.");if (r == true) {location.href='/crearproveedor/';} else {location.href='/crearproveedor/';}</script>"""
            else:
                return """<script>var r = confirm("ERROR: Por favor reintente.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        return render_template("crearProveedor.html", form=frm, titulo=usu)
    
@app.route('/modificarproveedor/',methods=['GET','POST'] )
def modif_proveedor():
    try:
        usu=session["nom"]
        rol=session["tipo"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Debe ingresar con un usuario reconocido. Será redirigido a la página de Login.");if (r == true) {location.href = "/";} else {location.href = "/";}</script>"""
    try:
        codprov=session["codprov"]
    except KeyError as ke:
        return """<script>var r = confirm("ERROR: Para modificar un proveedor, debe haberlo buscado primero. Será redirigido a la página de proveedores.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
    frm=ModificarProveedor()
    if request.method=='GET':
        sql= "SELECT nombre, descripcion, nit, direccion, telefono, nombre_contacto, cod_prod FROM Proveedor WHERE cod_prov='{}'".format(codprov)
        res= consulta_sel(sql) 
        try:
            nom=res[0][0]
            frm.descr.data=res[0][1]
            nit=res[0][2]
            direccion=res[0][3]
            tel=res[0][4]
            nomcontacto=res[0][5]
            codprod=res[0][6]
            codprovedor=codprov
            return render_template('modificarProveedor.html', form=frm,codprod=codprod,codigoproveedor=codprovedor,nombre=nom,nit=nit, direcc=direccion, telefono=tel, nombrecontacto=nomcontacto, titulo=usu)
        except IndexError as ie:
            return """<script>var r = confirm("ERROR: No puede regresar a esta pagina desde aqui. Ingrese desde proveedores y coloque el codigo del que desea modificar");if (r == true) {location.href = "/proveedores/";} else {location.href = "/proveedores/";}</script>"""
    else:
        if frm.btneditar.data==True:
            nomprov=escape(request.form["nom"])
            codprov=escape(request.form["codprov"])
            direcc=escape(request.form["direcc"])
            nit=escape(request.form["nit"])
            descr=escape(request.form["descr"])
            telf=escape(request.form["telf"])
            prscon=escape(request.form["prscon"])
            estd=escape(request.form["estd"])
            codprodunq=escape(request.form["codprod"])
            swerror=False
            if nomprov==None or len(nomprov)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar un nombre de proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if codprov==None or len(codprov)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar un codigo de proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if direcc==None or len(direcc)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar una direccion.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if nit==None or len(nit)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar el NIT del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if descr==None or len(descr)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar una descripcion del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if telf==None or len(telf)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar el telefono del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if prscon==None or len(prscon)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe suministrar la persona de contacto.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if estd==None or len(estd)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe confirmar el estado del proveedor.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if codprodunq==None or len(codprodunq)==0:
                swerror=True
                return """<script>var r = confirm("ERROR: Debe confirmar el codigo del producto asociado.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            if not swerror:
                sql= "UPDATE Proveedor SET cod_prov=?, nombre=?, descripcion=?, nit=?, direccion=?, telefono=?, nombre_contacto=?, id_estado=?, cod_prod=? WHERE cod_prov=?"
                res=consulta_acc(sql,(codprov,nomprov,descr,nit,direcc,telf,prscon,estd,codprodunq,codprov))
                if res!=0:
                    return """<script>var r = confirm("¡Datos correctamente guardados!.");if (r == true) {location.href='/proveedores/';} else {location.href='/proveedores/';}</script>"""
                else:
                    return """<script>var r = confirm("ERROR: Por favor reintente. Si ha verificado que los datos son validos y esta intentado modificar el codigo unico de proveedor, puede que no sea posible por su relación con otros registros de la base de datos. Dado esto, considere editar los registros relacionados.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
            return render_template("modificarProveedor.html", form=frm, titulo=usu)
        if frm.btneliminar.data==True:
            codprov=escape(request.form["codprov"])
            nit=escape(request.form["nit"])
            sql= "DELETE FROM Proveedor WHERE cod_prov=? AND nit=?"
            res=consulta_acc(sql,(codprov,nit))
            if res!=0:
                return """<script>var r = confirm("¡Datos correctamente eliminados!.");if (r == true) {location.href='/proveedores/';} else {location.href='/proveedores/';}</script>"""
            else:
                return """<script>var r = confirm("ERROR: Por favor reintente.Si ha verificado que los datos son validos y esta intentado eliminar el codigo unico de proveedor, puede que no sea posible por su relación con otros registros de la base de datos. Dado esto, considere editar los registros relacionados.");if (r == true) {window.history.go(-1);} else {window.history.go(-1);}</script>"""
        return render_template("modificarProveedor.html", form=frm, titulo=usu)













