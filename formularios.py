from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import PasswordField, TextField, SubmitField, FileField, TextAreaField, IntegerField, SelectField
from flask_wtf.file import FileField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import InputRequired


class Login(FlaskForm):
    usr= TextField("Usuario *", validators=[InputRequired(message="El campo usuario es requerido")])
    pwd= PasswordField ("Clave *", validators=[InputRequired(message="El campo Clave es requerido")])
    btn= SubmitField("Login")
    
class Registro(FlaskForm):
    nom= TextField("Nombre *", validators=[InputRequired(message="El campo usuario es requerido")])
    numdoc= IntegerField("Numero de documento *", validators=[InputRequired(message="El numero de documento es requerido")])
    direcc=TextField("Dirección *", validators=[InputRequired(message="El campo dirección es requerido")])
    telf=TextField("Telefono *", validators=[InputRequired(message="El telefono es requerido")])
    codusr=TextField("Usuario *", validators=[InputRequired(message="El codigo de usuario es requerido")])
    pwda= PasswordField ("Contraseña a asignar *", validators=[InputRequired(message="El campo Contraseña es requerido")])
    selct1 = SelectField("Tipo de usuario *",id="selerol", choices=[(0, "Select"),(2, "Administrador"), (3, "Usuario final")])
    selct2 = SelectField("Estado *", id="selestado", choices=[(0, "Select"),(1, "Activo"), (2, "Inactivo"), (3, "Bloqueado")])
    adj1=FileField("Cargar imagen de referencia*")
    btnusr= SubmitField("Crear usuario", id="btnsm")

class ModificarUsuario(FlaskForm):
    nom= TextField("Nombre *", validators=[InputRequired(message="El campo usuario es requerido")])
    numdoc= IntegerField("Numero de documento *", validators=[InputRequired(message="El numero de documento es requerido")])
    direcc=TextField("Dirección *", validators=[InputRequired(message="El campo dirección es requerido")])
    telf=TextField("Telefono *", validators=[InputRequired(message="El telefono es requerido")])
    codusr=TextField("Usuario *", validators=[InputRequired(message="El codigo de usuario es requerido")])
    pwda= PasswordField ("Contraseña a asignar *", validators=[InputRequired(message="El campo Contraseña es requerido")])
    selct1 = SelectField("Tipo de usuario *",id="selerol", choices=[(0, "Select"),(2, "Administrador"), (3, "Usuario final")])
    selct2 = SelectField("Estado *", id="selestado", choices=[(0, "Select"),(1, "Activo"), (2, "Inactivo"), (3, "Bloqueado")])
    adj1=FileField("Cargar imagen de referencia*")
    btnedt= SubmitField("Editar usuario", id="btneditar")
    btnelim= SubmitField("Eliminar usuario", id="btneliminar")

class CrearProducto(FlaskForm):
    codprov= TextField("Codigo del proveedor *", validators=[InputRequired(message="El campo Codigo del proveedor es requerido")])
    nomprod= TextField("Nombre del producto *", validators=[InputRequired(message="El campo nombre del producto es requerido")])
    descr= TextAreaField("Descripcion*", validators=[InputRequired(message="El campo descripcion requerido")])
    codunq=TextField("Codigo unico*", validators=[InputRequired(message="El codigo unico es requerido")])
    cantmin=IntegerField("Cantidad minima en bodega*",id="cantmin", validators=[InputRequired(message="La cantidad minima en bodega es requerida")])
    cantdisp=IntegerField("Cantidad disponible en bodega*", id="cantdisp", validators=[InputRequired(message="La cantidad disponible en bodega es requerida")])
    selectestd = SelectField("Estado *", id="selestadoprod", choices=[(0, "Select"),(1, "Activo"), (2, "Inactivo"), (3, "Bloqueado"), (4, "Agotado"), (3, "No disponible")])
    adj=FileField("Cargar imagen de referencia*")
    btncrear= SubmitField("Guardar", id="btncrear")

class BuscarProducto(FlaskForm):
    codprobs= TextField("Codigo del producto *", validators=[InputRequired(message="El campo Codigo del producto es requerido")])
    btnbusc= SubmitField("Buscar", id="btnbuscaproducto")

class ModificarProducto(FlaskForm):
    codprov= TextField("Codigo del proveedor *", validators=[InputRequired(message="El campo Codigo del proveedor es requerido")])
    nomprod= TextField("Nombre del producto *", validators=[InputRequired(message="El campo nombre del producto es requerido")])
    descr= TextAreaField("Descripcion*", validators=[InputRequired(message="El campo descripcion requerido")])
    codunq=TextField("Codigo unico*", validators=[InputRequired(message="El codigo unico es requerido")])
    cantmin=IntegerField("Cantidad minima en bodega*",id="cantmin", validators=[InputRequired(message="La cantidad minima en bodega es requerida")])
    cantdisp=IntegerField("Cantidad disponible en bodega*", id="cantdisp", validators=[InputRequired(message="La cantidad disponible en bodega es requerida")])
    selectestd = SelectField("Estado *", id="selestadoprod", choices=[(0, "Select"),(1, "Activo"), (2, "Inactivo"), (3, "Bloqueado"), (4, "Agotado"), (3, "No disponible")])
    adj=FileField("Cargar imagen de referencia*")
    btneditar= SubmitField("Editar", id="btneditar")
    btneliminar= SubmitField("Eliminar", id="btneliminar")

class BuscarUsuario(FlaskForm):
    numdocusr= IntegerField("Número de documento *", validators=[InputRequired(message="El campo numero de documento es requerido")])
    codusr= TextField("Usuario *", validators=[InputRequired(message="El campo usuario es requerido")])
    btnusr= SubmitField("Buscar", id="btnbuscausuario")
        
class BuscarProveedor(FlaskForm):
    codprov= IntegerField("Codigo de proveedor *", validators=[InputRequired(message="El campo Codigo del proveedor es requerido")])
    btnprov= SubmitField("Buscar", id="btnbuscaproveedor")

class RegistroProveedor(FlaskForm):
    nom= TextField("Nombre del proveedor *", validators=[InputRequired(message="El campo Nombre del proveedor es requerido")])
    codprov=TextField("Codigo del proveedor *", validators=[InputRequired(message="El Codigo de proveedor es requerido")])
    descr= TextAreaField("Descripcion*", validators=[InputRequired(message="El campo descripcion requerido")])
    nit= IntegerField("NIT *", validators=[InputRequired(message="El campor NIT es requerido")])
    direcc=TextField("Dirección *", validators=[InputRequired(message="El campo dirección es requerido")])
    telf=TextField("Telefono *", validators=[InputRequired(message="El campo Telefono es requerido")])
    prscon=TextField("Persona de contacto *", validators=[InputRequired(message="El campo Persona de contacto es requerido")])
    estd = SelectField("Estado *", id="selestadoprov", choices=[(0, "Select"),(1, "Activo"), (2, "Inactivo"), (3, "Bloqueado")])
    codprod=TextField("Codigo del producto asociado*", validators=[InputRequired(message="El campo Codigo del producto asociado es requerido")])
    btncrprov= SubmitField("Guardar", id="btncrearproveedor")
    
class ModificarProveedor(FlaskForm):
    nom= TextField("Nombre del proveedor *", validators=[InputRequired(message="El campo Nombre del proveedor es requerido")])
    codprov=TextField("Codigo del proveedor *", validators=[InputRequired(message="El Codigo de proveedor es requerido")])
    descr= TextAreaField("Descripcion*", validators=[InputRequired(message="El campo descripcion requerido")])
    nit= IntegerField("NIT *", validators=[InputRequired(message="El campor NIT es requerido")])
    direcc=TextField("Dirección *", validators=[InputRequired(message="El campo dirección es requerido")])
    telf=TextField("Telefono *", validators=[InputRequired(message="El campo Telefono es requerido")])
    prscon=TextField("Persona de contacto *", validators=[InputRequired(message="El campo Persona de contacto es requerido")])
    estd = SelectField("Estado *", id="selestadoprov", choices=[(0, "Select"),(1, "Activo"), (2, "Inactivo"), (3, "Bloqueado")])
    codprod=TextField("Codigo del producto asociado*", validators=[InputRequired(message="El campo Codigo del producto asociado es requerido")])
    btneditar= SubmitField("Editar", id="btneditar")
    btneliminar= SubmitField("Eliminar", id="btneliminar")
