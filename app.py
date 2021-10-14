from flask import Flask, render_template, request
from markupsafe import escape

app = Flask(__name__)
 
@app.route('/', methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('index.html')
    else:
        usuario= escape(request.form["nomtxt"])
        numedoc= escape(request.form["psswctxt"])  
        return render_template('principal.html')

@app.route('/principal/')
def principal(): 
    return render_template('principal.html')

@app.route('/usuarios/')
def usuarios():
    return render_template('usuarios.html') 

@app.route('/crearusuario/', methods=['GET','POST'])
def crear_usuario(): 
    if request.method=='GET':
        return render_template('crearUsuario.html')
    else:
        nombre= escape(request.form["nomtxt"])
        numedoc= escape(request.form["numdoctxt"])  
        tele= escape(request.form["telftxt"])  
        coduser= escape(request.form["codusrtxt"])
        contr=escape(request.form ["psstxt"])
        chkbx=escape(request.form ["chk"])
        #Se proyecta conexión a base de datos
        mssg=f"(Registro de usuario codigo {coduser} completado correctamente. <a href='/crearusuario'> Volver a pagina principal</a>"
        return mssg
                
@app.route('/modificarusuario/', methods=['GET','POST'])
def modif_usuario():
    if request.method=='GET':
        return render_template('modificarUsuario.html')
    else:
        nombre= escape(request.form["nomtxt"])
        numedoc= escape(request.form["numdoctxt"])  
        tele= escape(request.form["telftxt"])  
        coduser= escape(request.form["codusrtxt"])
        contr=escape(request.form ["psstxt"])
        chkbx=escape(request.form ["chk"])
        #Se proyecta conexión a base de datos
        return render_template('usuarios.html')

@app.route('/productos/')
def productos():
    return render_template('productos.html')

@app.route('/crearproducto/', methods=['GET','POST'])
def crear_producto():
    if request.method=='GET':
        return render_template('crearProducto.html')
    else:
        nombreprove= escape(request.form["nmprovetxt"])
        nombreprodc= escape(request.form["nmprdtxt"])  
        descrp= escape(request.form["dscrtxt"])  
        codunq= escape(request.form["cduqtxt"])
        #Se proyecta conexión a base de datos
        mssg=f"(Registro de producto codigo {codunq} completado correctamente. <a href='/crearproducto'> Volver a pagina anterior/a>"
        return mssg

@app.route('/modificarproducto/', methods=['GET','POST'])
def modif_producto():
    if request.method=='GET':
        return render_template('modificarProducto.html')
    else:
        nombreprove= escape(request.form["nmprovetxt"])
        nombreprodc= escape(request.form["nmprdtxt"])  
        descrp= escape(request.form["dscrtxt"])  
        codunq= escape(request.form["cduqtxt"])
        #Se proyecta conexión a base de datos
        return render_template('productos.html')

@app.route('/proveedores/')
def proveedores():
    return render_template('proveedores.html')

@app.route('/crearproveedor/', methods=['GET','POST'])
def crear_proveedor():
    if request.method=='GET':
        return render_template('crearProveedor.html')
    else:
        nombreprove= escape(request.form["nmprovetxt"])
        codprove= escape(request.form["codprvtxt"])  
        descrprov= escape(request.form["dscrprvtxt"])  
        codprove= escape(request.form["cdprovtxt"])
        #Se proyecta conexión a base de datos
        mssg=f"(Registro de proveedor codigo {codprove} completado correctamente. <a href='/crearproveedor'> Volver a pagina anterior/a>"
        return mssg

@app.route('/modificarproovedor/',methods=['GET','POST'] )
def modif_proveedor():
    if request.method=='GET':
        return render_template('modificarProovedor.html')
    else:
        nombreprove= escape(request.form["nmprovetxt"])
        codprove= escape(request.form["codprvtxt"])  
        descrprov= escape(request.form["dscrprvtxt"])  
        codprove= escape(request.form["cdprovtxt"])
        #Se proyecta conexión a base de datos
        return render_template('proveedores.html')

if __name__ == '__main__':
    app.run()