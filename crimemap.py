from flask import Flask, render_template, request
import dbconfig

if dbconfig.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()


@app.route("/")
def home():
    try:
        data = DB.get_all_inputs()
    except Exception as e:
        print(e)
        data = None
    return render_template("home.html", data=data)


@app.route("/add", methods=["POST"])
def add():
    try:
        data = request.form.get("userinput")
        DB.add_input(data)
    except Exception as e:
        print(e)
    return home()


@app.route("/clear")
def clear():
    try:
        DB.clear_all()
    except Exception as e:
        print(e)
    return home()


@app.route("/submitcrime", methods=['POST'])
def submitcrime():
    category = request.form.get("category")
    date = request.form.get("date")
    latitude = float(request.form.get("latitude"))
    longtitude = float(request.form.get("longtitude"))
    description = request.form.get("description")
    DB.add_crime(category, date, latitude, longtitude, description)
    return home()


if __name__ == '__main__':
    app.run(port=5000, debug=True)
