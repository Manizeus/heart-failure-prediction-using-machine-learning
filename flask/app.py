from flask import Flask,render_template,url_for
from flask import request
import joblib
import numpy as np
import sqlite3

app=Flask(__name__,static_folder='static')

con=sqlite3.connect("report.db")
con.execute("CREATE TABLE IF NOT EXISTS data(name TEXT, phone TEXT,age REAL,anaemia INTEGER,creatinine INTEGER,diabetes INTEGER, ejectionFraction INTEGER,highBloodPressure INTEGER,platelets REAL,serumCreatinine REAL,serumSodium INTEGER,MorF INTEGER,smoking INTEGER,time INTEGER,result TEXT)")
con.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/result",methods=['POST','GET'])
def register():
    if request.method=='POST':
       
        name=request.form.get('name')
        phone=request.form.get('phoneNumber')
        age=float(request.form.get('Age'))
        anaemia=int(request.form.get('Anaemia'))
        creatinine=int(request.form.get('creatinine'))
        diabetes=int(request.form.get('diabetes'))
        ejectionFraction=int(request.form.get('ejectionFraction'))
        highBloodPressure=int(request.form.get('highBloodPressure'))
        platelets=float(request.form.get('platelets'))
        serumCreatinine=float(request.form.get('serumCreatinine'))
        serumSodium=int(request.form.get('serumSodium'))
        MorF=int(request.form.get('MorF'))
        smoking=int(request.form.get('smoking'))
        time=int(request.form.get('time'))
           
        feature=[age,anaemia,creatinine,diabetes,ejectionFraction,highBloodPressure,platelets,serumCreatinine,serumSodium,MorF,smoking,time]
        arr=[np.array(feature)]   
        model=joblib.load('model.pkl')
        pre=model.predict(arr)
        
        result=str(pre[0])
        if result=='0':
            result="your are not in risky condition (or) this report indicate no one die by given parameters"
        else:
            result="your are in critical condition (or) this report indicate persons die by give parameters"

        con=sqlite3.connect("report.db")
        cur=con.cursor()
        cur.execute("INSERT INTO data(name,phone,age,anaemia,creatinine,diabetes,ejectionFraction,highBloodPressure,platelets,serumCreatinine,serumSodium,MorF,smoking,time,result)values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(name,phone,age,anaemia,creatinine,diabetes,ejectionFraction,highBloodPressure,platelets,serumCreatinine,serumSodium,MorF,smoking,time,result))
        con.commit()

        return render_template('result.html',Name=name,pN=phone,Age=age,Anaemia=anaemia,Creatinine=creatinine,
        Diabetes=diabetes,EF=ejectionFraction,HBP=highBloodPressure,pla=platelets,SC=serumCreatinine,SS=serumSodium,
        MF=MorF,smoke=smoking,Time=time,Result=result)


if __name__=="__main__":
    app.run(host='0.0.0.0')
