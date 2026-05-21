import mysql.connector
from flask  import Flask, render_template , request , redirect ,flash


app = Flask(__name__)

app.secret_key = "some_random_secret_string"

dataBase = mysql.connector.connect(
        host ="localhost",
        user = "root",
        password = "your_password_here",
        database = "expense_traker"
    )

@app.route('/')
def home():

    cursorObject = dataBase.cursor()
    
    cursorObject.execute("SELECT cost FROM cost")
    myResult = cursorObject.fetchall()
    total = 0
    total = sum(float(x[0]) for x in myResult if x[0]) 

    cursorObject.execute("SELECT cost FROM cost WHERE category='Food'")
    food_result = cursorObject.fetchall()
    tot_food = 0
    tot_food = sum(float(f[0]) for f in food_result if f[0])

    cursorObject.execute("SELECT cost FROM cost WHERE category='Enterinment'")
    ent_result = cursorObject.fetchall()
    tot_ent =0
    tot_ent = sum(float(e[0]) for e in ent_result if e[0])

    cursorObject.execute("SELECT cost FROM cost WHERE category='Rent'")
    rent_result = cursorObject.fetchall()
    tot_rent =0
    tot_rent = sum(float(r[0]) for r in rent_result if r[0])

    cursorObject.execute("SELECT cost FROM cost WHERE category='Health'")
    health_result = cursorObject.fetchall()
    tot_health =0
    tot_health = sum(float(h[0]) for h in health_result if h[0])


    if total > 0:
        food_bar = round((tot_food / total)*100,2)
        rent_bar =round((tot_rent / total)*100,2)
        ent_bar = round((tot_ent / total)*100,2)
        health_bar = round((tot_health / total)*100,2)
    else:
        food_bar = rent_bar = ent_bar = health_bar = 0.0

    cursorObject.close()
        
    return render_template('index.html',total_exp =total,tot_food =tot_food,
                           tot_ent=tot_ent,tot_rent= tot_rent,tot_health =tot_health,
                           food_bar=food_bar, rent_bar=rent_bar,ent_bar =ent_bar,health_bar =health_bar)


@app.route('/submit', methods=['POST'])
def submit_data():
     
    item_name = request.form.get('name')
    category= request.form.get('category')
    cost= request.form.get('cost')

    try:
        cursorObject = dataBase.cursor();

        sql = "INSERT INTO cost (name,category,cost)  VALUES(%s ,%s, %s)"
        val = (item_name,category,cost)

        cursorObject.execute(sql,val)
        dataBase.commit()
        cursorObject.close()
    
       
        print(f"Thank you {item_name}, Data Recived !")
        flash(f"Success : Added  to expenses! ","success")

    except mysql.connector.Error as err:
        flash(f"Failed :Coulde not save data in the DataBase ","danger")

    
     
    return redirect('/')



if __name__ == '__main__':
     app.run(debug=True)
     






