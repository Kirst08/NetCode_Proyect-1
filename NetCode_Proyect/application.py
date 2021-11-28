from flask import Flask, request, render_template,redirect
from dataRequest import connect, New_Register, Nick_existente, Correct_LogIn, recover_password, Correct_User
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask("__name__")
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route("/home")
@app.route("/")
def hello():
    return render_template('Home.html')

@app.route("/login", methods= ["POST","GET"])
def login():

    if request.method == 'POST':

        if not request.form.get("username"):
            return "error en username"
        elif not request.form.get("password"):
            return "error en password"

        # establecemos la coneccion con la base de datos Users
        conn = connect()

        if not Correct_LogIn(conn, request.form.get("password"), request.form.get("username")):
            return "datos erroneos"

        conn.close()

        return redirect("/home2")

    return render_template("login.html")

@app.route("/registro", methods = ["POST","GET"])
def registro():

    if request.method == 'POST':

        if not request.form.get("name"):
            return "error en name"
        elif not request.form.get("nick"):
            return "error en nick"
        if not request.form.get("email"):
            return "error en email"
        elif not request.form.get("password"):
            return "error en password"

        # establecemos la coneccion con la base de datos Users
        conn = connect()

        if Nick_existente(conn, request.form.get("nick")):
            return "nic existente"

        New_Register(conn, request.form.get("name"), request.form.get("nick"), request.form.get("email"), generate_password_hash(request.form.get("password")))

        conn.close()

        return redirect("/login")


    return render_template("registro.html")


@app.route("/recover", methods = ["GET", "POST"])
def recover():
    if request.method == 'POST':

        if not request.form.get("nickname"):
            return "error en nickname"
        elif not request.form.get("email"):
            return "error en email"
        if not request.form.get("password"):
            return "error en password"
        elif not request.form.get("confirm"):
            return "error en confirm"

        # establecemos la coneccion con la base de datos Users
        conn = connect()

        if not  Correct_User(conn, request.form.get("nickname"), request.form.get("email")):
            return "error en los datos del username & email"

        if request.form.get("confirm") != request.form.get("password"):
            return "error las contraseñas son diferentes"

        recover_password(conn, generate_password_hash(request.form.get("password")), request.form.get("nickname"))

        conn.close()

        return redirect("/login")

    return render_template("recover.html")


@app.route("/home2")
def session_open():
    return render_template("home2.html")


@app.route("/Cpython")
def Cpython():
    return render_template("curso_python_prueba.html")

@app.route("/C")
def C():
    return render_template("cursoC.html")

@app.route("/logout", methods = ["GET", "POST"])
def logout():
    if request.method == 'GET':
        #session.clear()
        return redirect("/")

    return render_template("home2.html")

if __name__== '__main__':
    app.run(debug = True)