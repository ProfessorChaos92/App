from flask import Flask,render_template, request, redirect, session
import data
from datetime import date

username  = str

app = Flask(__name__)
app.secret_key = 'ItShouldBeAnything'

@app.route('/')
def inventory():
    if 'user' in session:
        return render_template('home.html')
    print('Redirect error')
    return render_template('login.html')

#Step – 4 (creating route for login)
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if(request.method == 'POST'):
        username = request.form.get('username')
        password = request.form.get('password')   
        if data.LoginValidate(username,password) == True:
            print('Login Success')
            session['user'] = username
            return redirect('/')
        else:
            return render_template('login.html')   #if the username or password does not matches 
    return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('dashboard.html')
    return render_template('login.html')
    
@app.route('/portal')
def portal():
    if 'user' in session:
        return render_template('portal.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')         #session.pop('user') help to remove the session from the browser
        return redirect('/login')
    return redirect('/login')
    
@app.route('/inventory')
def inventory2():
    if 'user' in session:
        return render_template('inventory.html',items = data.QueryAll(session['user']))
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/additem')
def additem():
    if 'user' in session:
        data.InsertRecord(str(request.args['Product']),float(request.args['Price']),int(request.args['Quantity']), username=session['user'])
        return render_template('additem.html', Product=str(request.args['Product']),Quantity=int(request.args['Quantity']))
    return render_template('login.html')
    
@app.route('/thanks', methods = ['POST'])
def thanks():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    registration = data.RegisterUser(username,password,email)
    if registration == 'Success':
        return render_template('thanks.html')
    else:
        return render_template('error.html', registration = registration)


@app.route('/update')
def update():
    list = data.ItemQuery()
    return render_template('update.html', list= list)

@app.route('/updated', methods = ["POST"])
def updated():
    item = request.form.get('Item')
    print(item)
    return render_template('updated.html')

@app.route('/function', methods = ['POST'])
def function():
    if 'user' in session:
        function = request.form['function']
        if(request.method == 'POST'):
            if function == 'LowInventory':
                return render_template('functions.html', result = data.LowInventory(),function=function)
            elif function == 'GetListOfCurrentInvetory':
                CurrentInvetory = data.QueryAll(session['user'])
                with open('output/CurrentInvetory.txt', 'w') as f:
                    f.write("%s\n" % date.today())
                    for i in CurrentInvetory:
                        # write each item on a new line
                        f.write("%s" % i['Item']) 
                        f.write("%s" % '   ') 
                        f.write("%s\n" % i['Quantity'])
                    print('Done')
                return render_template('functions.html')
            elif function == 'TextLowInventory':
                pass
        return render_template('functions.html')
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)
