from flask import Flask
import views
from flask_session import Session
from flask_mysqldb import MySQL

app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB']='copeye'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
mysql=MySQL(app)
Session(app)

app.add_url_rule('/','login',views.login,methods=['GET', 'POST'])
app.add_url_rule('/index','index',views.index)
app.add_url_rule('/criminal','criminal',views.criminal,methods=['GET', 'POST'])
app.add_url_rule('/facemask','facemask',views.facemask,methods=['GET', 'POST'])
app.add_url_rule('/find_criminal','find_criminal',views.find_criminal,methods=['GET', 'POST'])
app.add_url_rule('/lost_found','lost_found',views.lost_found,methods=['GET', 'POST'])
app.add_url_rule('/signup','signup',views.signup,methods=['GET', 'POST'])
app.add_url_rule('/citizen','citizen',views.citizen,methods=['GET', 'POST'])
app.add_url_rule('/find_lost','find_lost',views.find_lost,methods=['GET', 'POST'])
app.add_url_rule('/about_us','about_us',views.about_us,methods=['GET', 'POST'])
app.add_url_rule('/result_criminal','result_criminal',views.result_criminal,methods=['GET', 'POST'])
app.add_url_rule('/result_facemask','result_facemask',views.result_facemask,methods=['GET', 'POST'])
app.add_url_rule('/result_lostfound','result_lostfound',views.result_lostfound,methods=['GET', 'POST'])



if __name__ == '__main__':
    app.run(debug=True)