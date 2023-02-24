from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import mysql
import mysql.connector as sql_db



app = Flask(__name__)
app.secret_key = "message flash" # this is needed for displaying the flash message that is created for inputting data

#the below code is needed in order to connect to the sql server/database
app.config['MYSQL_HOST'] = 'sqlserverr.mysql.database.azure.com' #this is the name of my server
app.config['MYSQL_USER'] = 'ServerAdmin' #this is the username my server uses
app.config['MYSQL_PASSWORD'] = 'Apprentice123!' #this is the password that is needed to access the server
app.config['MYSQL_DB'] = 'cruddatabase' #this is the name of the database that i want to use
app.config['MYSQL_SSL'] = 'DigiCertGlobalRootCA.crt.pem'  #this is the ssl certificate
mysql = MySQL(app)


#cnx = sql_db.connect(user="ServerAdmin", password="Apprentice123!", host="sqlserverr.mysql.database.azure.com", port=3306, database="cruddatabase", ssl_ca="C:\earlm\PycharmProjects\assignmentproject1\Flask CRUD application\DigiCertGlobalRootCA.crt.pem", ssl_disabled=False)
#the above line of code is another way to connect to the server using the same components with a few more added on



@app.route('/')
def Index():
    #this is the code that is needed to update the website with what has been added into the database
    cur = mysql.connection.cursor() #cur is a variable that holds a databse cursor
    cur.execute("SELECT * FROM clients") #SQL command to be able to select all rows in the table called clients which is the table created in azure
    data = cur.fetchall() # fetches all of rows from the table
    cur.close()
    return render_template('index.html', clients = data)
#this function is needed to be able to link to the front end of html/bootstrap

@app.route('/insert', methods = ['POST']) #this is the link to the webpage that the user will be directed to should they press the insert button
def insert():
#this function is needed to insert data into all of the fields of the table
    if request.method == "POST":
        #flash("Data Inserted Successfully ")
        name = request.form['name']
        address = request.form['address']
        date = request.form['date']
        invoicenumber = request.form['invoicenumber']
        description = request.form['description']
        invoicetotals = request.form['invoicetotals']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO clients (name, address, date, invoicenumber, description, invoicetotals) VALUES (%s, %s, %s, %s, %s, %s)", [name, address, date, invoicenumber, description, invoicetotals])
        #the above code is the SQL command needed to allow the user to insert the data inputted into the database
        mysql.connection.commit()
        return redirect(url_for('Index')) #this redirects to the start webpage so that the user can choose what they need to do next

#this is where I define the edit button

@app.route('/update', methods = ['POST', 'GET']) #these are the HTTP methods that the function will be using
def update():
    if request.method == 'POST':
        data_ID = request.form['id']
        name = request.form['name']
        address = request.form['address']
        date = request.form['date']
        invoicenumber = request.form['invoicenumber']
        description = request.form['description']
        invoicetotals = request.form['invoicetotals']

#%s - this means a placeholder string
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE clients 
        SET name=%s, address=%s, date=%s, invoicenumber=%s, description=%s, invoicetotals=%s
        WHERE id=%s
        """, (name, address, date, invoicenumber, description, invoicetotals, data_ID)) #this is the SQL command that is needed to allow the user to be able to update the client table
        flash("Client Successfully Updated") #this shows a flash message on the web application saying what is shown in the parameters
        mysql.connection.commit()
        return redirect(url_for('Index')) #this redirects the user back to the first webpage


@app.route('/delete/<string:data_ID>', methods = ['POST', 'GET'])
def delete(data_ID):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM clients WHERE id = (%s)", (data_ID,)) #correct one
    #cur.execute("DELETE FROM clients WHERE id = (%s)", (data_ID)) #incorrect one
    flash("Client Successfully Deleted") #this is another flash message that shows the client has been successfully deleted
    mysql.connection.commit()
    return redirect(url_for('Index'))


if __name__ == "__main__":
    app.run(debug=True)
    #this is what allows me to run the app in the development environment

