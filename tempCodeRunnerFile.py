
app.config['MYSQL_DB']='copeye'
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
mysql=MySQL(app)