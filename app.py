from flask import Flask,render_template,session,url_for,redirect,request, flash,send_from_directory
import mysql.connector
import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error,mean_absolute_error
import numpy as np
from tensorflow.keras.preprocessing import image
from sklearn.metrics import r2_score
from tensorflow.keras.models import load_model
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from matplotlib import pyplot as plt
from datetime import datetime


from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score

app=Flask(__name__)
app.config['SECRET_KEY']='abcdefghijklmnop'
mydb = mysql.connector.connect(host="localhost", user="root", passwd="", database="e-agri")
cursor = mydb.cursor()

DF=pd.read_csv("csv_file/final_dataSet_nonan.csv")
x = DF.iloc[:,:-1]
y = DF.iloc[:,-1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=32)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/work')
def work():
    return render_template('work.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/farmer')
def farmer():
    return render_template('farmer.html')

@app.route('/regback',methods = ["POST"])
def regback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        pno=request.form['ph']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        sql = "select * from farmer"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","warning")
            return render_template('farmer.html')
        if pwd==cpwd:
            sql = "INSERT INTO farmer (name,email,pwd,pno,addr) VALUES (%s,%s,%s,%s,%s)"
            val = (name, email, pwd, pno, addr)
            cursor.execute(sql, val)
            mydb.commit()
            flash("Successfully Registered", "success")
        else:
            flash("Password and Confirm password not same","danger")
        return render_template('farmer.html')
    return render_template('farmer.html')


@app.route('/farmerlog')
def farmerlog():
    return render_template('farmerlog.html')

@app.route('/logback',methods=['POST', 'GET'])
def logback():
    if request.method == 'POST':
        username = request.form['email']
        # opt = request.form['opt']
        password1 = request.form['pwd']

        sql = "select * from farmer where email='%s' and pwd='%s' " % (username, password1)
        x = cursor.execute(sql)
        results = cursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('index.html')

        else:
            session['email'] = username
            if len(results) > 0:
                flash("Welcome ", "primary")
                session['name']=results[0][1]
                return render_template('userhome.html', msg=results[0][1])
    return render_template('index.html')

@app.route('/classify')
def classify():
    return render_template('classify.html')
@app.route("/upload", methods=["POST","GET"])
def upload():
    print('a')
    if request.method=='POST':
        myfile=request.files['file']
        fn=myfile.filename
        mypath=os.path.join('images/', fn)
        myfile.save(mypath)

        print("{} is the file name",fn)
        print ("Accept incoming file:", fn)
        print ("Save it to:", mypath)

        new_model = load_model("alg1/FinalModel_1.h5")
        test_image = image.load_img(mypath, target_size=(224, 224))
        test_image = image.img_to_array(test_image)
        test_image = test_image / 255
        test_image = np.expand_dims(test_image, axis=0)
        result = new_model.predict(test_image)
        print("Stop Model")
        classes = ['BrownSpot', 'Corn Gray Leaf Blight', 'Corn Common Rust', 'Corn Northern Leaf Blight',
                   'Corn Healthy', 'Rice Healthy', 'Rice Hispa', 'Rice Leaf Blast',
                   'Potato Early Blight', 'Potato Late Blight', 'Potato Healthy',
                   'Tomato Bactirial Spot', 'Tomato Leaf Blight', 'Tomato yellow Leaf Curl Virus', 'Tomato Healthy',
                   'Diseased Cotton Leaf', 'Healthy Cotton']

        prediction = np.argmax(result)
        if prediction == 7:
            msg = 'Remedies of Rice LeafBlast :: fungicides like triazoles and strobilurins can be used judiciously for control to leaf blast.'
            prediction1 = classes[prediction]
        elif prediction == 0:
            msg = 'Remedies of BrownSpot :: fungicides(e.g., iprodione, propiconazole, azoxystrobin, trifloxystrobin, and carbendazim) & Treat seeds with hot water.'
            prediction1 = classes[prediction]
        elif prediction == 1:
            msg = 'Remedies of Corn Gray Leaf Blight :: Use of preventative management tactics, crop rotation, and practices that remove corn residue or tillage to promote decomposition.'
            prediction1 = classes[prediction]
        elif prediction == 2:
            msg = 'Remedies of Corn Common Rust :: Plant hybrids resistant to anthracnose; rotating crops and plowing crop debris into soil may help reduce incidence of early season infections. '
            prediction1 = classes[prediction]
        elif prediction == 3:
            msg = 'Remedies of Corn Northern Leaf Blight :: Use of preventative management tactics, crop rotation, and practices that remove corn residue or tillage to promote decomposition'
            prediction1 = classes[prediction]
        elif prediction == 6:
            msg = 'Remedies of Hispa :: Various foliar fungicides are available to help control or suppress NCLB development.'
            prediction1 = classes[prediction]
        elif prediction == 8:
            msg = 'Remedies of Potato Early Blight :: Early blight can be minimized by maintaining optimum growing conditions, including proper fertilization, irrigation, and management of other pests.'
            prediction1 = classes[prediction]
        elif prediction == 9:
            msg = 'Remedies of Potato Late Blight :: Late blight is controlled by eliminating cull piles and volunteer potatoes, using proper harvesting and storage practices, and applying fungicides when necessary. Air drainage to facilitate the drying of foliage each day is important.'
            prediction1 = classes[prediction]
        elif prediction == 11:
            msg = 'Remedies of Tomato Bactirial Spot ::  Remove symptomatic plants from the field or greenhouse to prevent the spread of bacteria to healthy plants.  Burn, bury or hot compost the affected plants and DO NOT eat symptomatic fruit'
            prediction1 = classes[prediction]
        elif prediction == 12:
            msg = 'Remedies of Tomato Late Blight ::  For the home gardener, fungicides that contain maneb, mancozeb, chlorothanolil, or fixed copper can help protect plants from late tomato blight.'
            prediction1 = classes[prediction]
        elif prediction == 13:
            msg = 'Remedies of  Tomato Yellow Leaf Curl Virus ::  Maintain good weed control in the field and surrounding areas. '
            prediction1 = classes[prediction]
        elif prediction == 15:
            msg = 'Remedies of  Diseased Cotton Leaf ::  Plow crop residue into the soil to reduce inoculum levels; provide plants with adequate irrigation and nutrients, particularly potassium; applications of appropriate foliar fungicides may be required on susceptible cultivars.. '
            prediction1 = classes[prediction]
        else:
            msg = ''
            prediction1 = classes[prediction]

    return render_template("upload.html",image_name=fn,msg=msg, text=prediction1)
@app.route('/upload/<filename>')
def send_image(filename):
    return send_from_directory("images", filename)

@app.route('/makefund')
def makefund():
    return render_template('makefund.html')

@app.route('/fundsback',methods = ["POST"])
def fundsback():
    if request.method=='POST':
        cname=request.form['cname']
        yeild=request.form['yeild']
        fname=request.form['fname']
        pno=request.form['pno']
        addr=request.form['addr']
        share=request.form['share']
        money=request.form['money']
        area=request.form['area']
        email=session.get('email')

        sq="select * from crop_prices where crop='"+cname+"'"
        cursor.execute(sq)
        data=cursor.fetchall()
        print(data)
        mydb.commit()
        crop_price=data[0][2]
        print("&&&&&&&&&")
        print(crop_price)
        flash("Data Successfully submited", "success")

        sql = "INSERT INTO make_funds (cname,crop_price,yeild,fname,email,pno,area,money,addr,share) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (cname,crop_price,yeild,fname,email,pno,area,money,addr,share)
        cursor.execute(sql, val)
        mydb.commit()
        return render_template('makefund.html')
    return render_template('makefund.html')

@app.route('/viewfunds')
def viewfunds():
    email=session.get('email')
    sql="select * from make_funds where email='"+email+"'"
    cursor.execute(sql)
    data=cursor.fetchall()
    return render_template("viewfunds.html", data=data)

@app.route('/update/<s>/<s1>/<s2>/<s3>/<s4>/<s5>/<s6>/<s7>/<s8>/<s9>')
def update(s=0,s1="",s2="",s3="",s4="",s5="",s6="",s7="",s8="",s9=""):
    return render_template("update.html",s=s,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9)


@app.route('/updateback', methods=["POSt","GET"])
def updateback():
    id = request.form['id']
    cname = request.form['cname']
    yeild = request.form['yeild']
    fname = request.form['fname']
    pno = request.form['pno']
    money = request.form['money']
    area = request.form['area']
    share = request.form['share']
    email = request.form['email']
    sql="update make_funds set cname='%s',yeild='%s',fname='%s',email='%s',pno='%s',area='%s',money='%s',share='%s' where id='%s'" %(cname,yeild,fname,email,pno,area,money,share,id)
    cursor.execute(sql,mydb)
    mydb.commit()
    flash("Data updated","success")
    return redirect(url_for('viewfunds'))

@app.route('/cancel/<s>')
def cancel(s=0):
    sql="delete from make_funds where id='%s'"%(s)
    cursor.execute(sql,mydb)
    mydb.commit()
    flash("Data deleted","info")
    return redirect(url_for('viewfunds'))

@app.route('/addcrop')
def addcrop():
    return render_template('addcrop.html')

@app.route('/investor')
def investor():
    return render_template('investor.html')

@app.route('/investorback',methods = ["POST"])
def investorback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        pno=request.form['ph']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        sql = "select * from investor"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","warning")
            return render_template('investor.html')
        if pwd==cpwd:
            sql = "INSERT INTO investor (name,email,pwd,pno,addr) VALUES (%s,%s,%s,%s,%s)"
            val = (name, email, pwd, pno, addr)
            cursor.execute(sql, val)
            mydb.commit()
            flash("Successfully Registered", "success")
        else:
            flash("Password and Confirm password not same","danger")
        return render_template('investor.html')
    return render_template('investor.html')

@app.route('/investorlog')
def investorlog():
    return render_template('investorlog.html')

@app.route('/investorlogback',methods=['POST', 'GET'])
def investorlogback():
    if request.method == 'POST':
        username = request.form['email']
        # opt = request.form['opt']
        password1 = request.form['pwd']

        sql = "select * from investor where email='%s' and pwd='%s' " % (username, password1)
        x = cursor.execute(sql)
        results = cursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('investorlog.html')

        else:
            session['email'] = username
            if len(results) > 0:
                flash("Welcome ", "primary")
                session['name']=results[0][1]
                session['pno']=results[0][4]
                return render_template('investorhome.html', msg=results[0][1])
    return render_template('investor.html')

@app.route('/addcropback',methods = ["POST"])
def addcropback():
    if request.method=='POST':
        cname=request.form['cname']
        yeild=request.form['yeild']
        year=request.form['year']
        investment=request.form['investment']
        location=request.form['location']
        area=request.form['area']
        profit=request.form['profit']
        fname=session.get('name')

        sql = "INSERT INTO crop_data (fname,cname,ctype,cyear,area,location,investment,profit) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (fname,cname,yeild,year,area,location,investment,profit)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Crop information added", "success")
        return render_template('addcrop.html')
    return render_template('addcrop.html')

@app.route('/cropdata')
def cropdata():
    sql="select * from crop_data"
    x=pd.read_sql_query(sql,mydb)

    return render_template("cropdata.html", cal_name=x.columns.values, row_val=x.values.tolist())
@app.route('/funds')
def funds():
    sql = "select * from make_funds where status='pending'"
    x = pd.read_sql_query(sql, mydb)
    x=x.drop(['status','crop_price', 'e_money'], axis=1)
    return render_template("funds.html", cal_name=x.columns.values, row_val=x.values.tolist())


@app.route('/crop')
def crop():
    return render_template('crop.html')

@app.route('/cropback', methods=["POST","GET"])
def cropback():
    if request.method=='POST':
        s=int(request.form['s'])
        c=int(request.form['c'])
        y=int(request.form['year'])
        a=int(request.form['Area'])
        r=int(request.form['Rain'])
        m = [s, y, c, a, r]
        rf = RandomForestRegressor()
        rf.fit(x_train, y_train)
        rfp = rf.predict([m])
        # rfp = rf.predict(x_test)
        # rfa = r2_score(y_test, rfp)
        # mqer = mean_squared_error(y_test, rfp, squared=False)
        # maer = mean_absolute_error(y_test, rfp)
        # print(rfa,mqer,maer)
        # rfa = r2_score(y_test, rfp)
        # acc=accuracy_score(y_test,rf)
        # pre=precision_score(y_test,rf)
        # recal=recall_score(y_test,rf)
        # b = rf.predict(a)

        msg = rfp[0]
        print(msg)
        flash("Future extimation crop yeild is ", "info")
        # return render_template("crop.html", msg=msg,acc=acc,pre=pre,recal=recal)
        # return render_template("crop.html", msg=msg,acc=rfa,pre=mqer,recal=maer)
        return render_template("crop.html", msg=msg)

@app.route('/investorinfo')
def investorinfo():
    email=session.get('email')
    sql = "select * from investment_data where femail='"+email+"' and status='pending'"
    x = pd.read_sql_query(sql, mydb)
    print(x)
    print(type(x))
    # print(len(x))
    val=len(x)
    s="select * from investment_data where femail='"+email+"' and status='Accepted'"
    y = pd.read_sql_query(s, mydb)
    sal=len(y)
    print(y)
    x = x.drop(['fname', 'femail','fno','faddr','status'], axis=1)
    y = y.drop(['fname', 'femail','fno','faddr','status'], axis=1)
    return render_template("investorinfo.html", row_val=x.values.tolist(),row_val1=y.values.tolist(),v=val,s=sal)

@app.route('/invest/<s>/<s1>/<s2>/<s3>/<s4>/<s5>/<s6>/<s7>/<s8>/<s9>')
def invest(s=0,s1="",s2="",s3="",s4="",s5="",s6="",s7="",s8="",s9=""):
    print(s,s1,s2,s3,s4,s5,s6,s7,s8,s9)
    return render_template("invest.html",s=s,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9)

@app.route('/investback', methods=["POST","GET"])
def investback():
    if request.method=='POST':
        cname = request.form['cname']
        yeild = request.form['yeild']
        fname = request.form['fname']
        pno = request.form['pno']
        id = request.form['id']
        share = request.form['share']
        addr1 = request.form['addr']
        area = request.form['area']

        addr = request.form['location']
        money = request.form['money']
        email = request.form['email']
        print(money)
        e=session.get('email')
        n=session.get('name')
        p=session.get('pno')
        invest = int(request.form['e_money'])
        sq="select money from make_funds where id='"+id+"'"
        x=pd.read_sql_query(sq,mydb)
        m=int(x.values[0][0])
        total_amount=m
        if m < invest:
            flash('Invalid request',"danger")
            return redirect(url_for('funds'))
        elif m==invest:
            msg = ' Hi '
            otp = " is showing interest to invest in your crop and willing to pay the amount of "
            t = 'Regards,'
            t1 = 'E-Agri Kit Services.'
            mail_content = msg + fname + '\n' + n + otp + str(invest) + '.' + '\n' + '\n' + t + '\n' + t1
            sender_address = 'taraksaik2036@gmail.com'
            sender_pass = 'raazahejryshyqsc'
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'E-Agri Kit- Agriculture Aid'
            message.attach(MIMEText(mail_content, 'plain'))
            session1 = smtplib.SMTP('smtp.gmail.com', 587)
            session1.starttls()
            session1.login(sender_address, sender_pass)
            text = message.as_string()
            session1.sendmail(sender_address, receiver_address, text)
            session1.quit()
            s="update make_funds set status='completed' where id='"+id+"'"
            cursor.execute(s,mydb)
            mydb.commit()
            s1="insert into investment_data(fid,cname,yeild,fname,femail,fno,faddr,iname,iemail,ino,iaddr,area,money,share,e_money) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            val=(id,cname, yeild, fname, email, pno, addr, n, e, p, addr1,area, money, share, invest)
            cursor.execute(s1,val)
            mydb.commit()
            flash("Request Submitted to farmer, please wait for reply ", "success")
            return redirect(url_for('funds'))
        else:
            msg = 'Hi'
            otp = "is showing interest to invest in your crop and willing to pay the amount of"
            t = 'Regards,'
            t1 = 'E-Agri Kit Services.'
            mail_content1 = msg + fname + '\n' + n + otp + str(invest) + '.' + '\n' + '\n' + t + '\n' + t1
            sender_address1 = 'taraksaik2036@gmail.com'
            sender_pass1 = 'raazahejryshyqsc'
            receiver_address1 = email
            message1 = MIMEMultipart()
            message1['From'] = sender_address1
            message1['To'] = receiver_address1
            message1['Subject'] = 'E-Agri Kit- Agriculture Aid'
            message1.attach(MIMEText(mail_content1, 'plain'))
            session2 = smtplib.SMTP('smtp.gmail.com', 587)
            session2.starttls()
            session2.login(sender_address1, sender_pass1)
            text1 = message1.as_string()
            session2.sendmail(sender_address1, receiver_address1, text1)
            session2.quit()
            total_amount=m-invest
            s1 = "insert into investment_data(fid,cname,yeild,fname,femail,fno,faddr,iname,iemail,ino,iaddr,area,money,share,e_money) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) "
            val = (id, cname, yeild, fname, email, pno, addr, n, e, p, addr1, area, money, share, invest)
            cursor.execute(s1, val)
            mydb.commit()
            # s2="update make_funds set money='%s' where id='%s'"%(total_amount,id)
            # cursor.execute(s2, mydb)
            # mydb.commit()
            flash("Request Submitted to farmer, please wait for reply ","success")
            return redirect(url_for('funds'))
    return redirect(url_for('funds'))
@app.route('/accept/<s>/<s1>/<s2>/<s3>/<s4>')
def accept(s=0,s1="",s2="",s3=0,s4 = ""):
    name=session.get('name')
    print(name)
    total_amount=int(s2)-int(s4)
    print(s2,s1,total_amount)
    s2 = "update make_funds set money='%s' where id='%s'" % (total_amount, s3)
    cursor.execute(s2, mydb)
    mydb.commit()
    sql="update investment_data set status='Accepted' where id='"+s+"'"
    cursor.execute(sql, mydb)
    mydb.commit()
    msg = 'Hi'
    m=" Congratulations!! "
    otp = " has accepted your request"
    t = 'Regards,'
    t1 = 'E-Agri Kit Services.'
    mail_content1 = s2+ m + ','+ '\n' + name + otp +  '\n' + '\n' + t + '\n' + t1
    sender_address1 = 'taraksaik2036@gmail.com'
    sender_pass1 = 'raazahejryshyqsc'
    receiver_address1 = s1
    message1 = MIMEMultipart()
    message1['From'] = sender_address1
    message1['To'] = receiver_address1
    message1['Subject'] = 'E-Agri Kit- Agriculture Aid'
    message1.attach(MIMEText(mail_content1, 'plain'))
    session2 = smtplib.SMTP('smtp.gmail.com', 587)
    session2.starttls()
    session2.login(sender_address1, sender_pass1)
    text1 = message1.as_string()
    session2.sendmail(sender_address1, receiver_address1, text1)
    session2.quit()
    flash("Your opinon is shared with investor",   "success")
    return redirect(url_for('investorinfo'))

@app.route('/reject/<s>/<s1>/<s2>')
def reject(s=0,s1="",s2=""):
    name=session.get('name')
    print(name)
    sql="update investment_data set status='Reject' where id='"+s+"'"
    cursor.execute(sql, mydb)
    mydb.commit()
    msg = 'Hi'
    # m=" Congratulations!! "
    otp = "Your request is been rejected by "
    t = 'Regards,'
    t1 = 'E-Agri Kit Services.'
    mail_content1 =  msg + s2+ ','+ '\n' + otp + name  + '.'+ '\n' + '\n' + t + '\n' + t1
    sender_address1 = 'taraksaik2036@gmail.com'
    sender_pass1 = 'raazahejryshyqsc'
    receiver_address1 = s1
    message1 = MIMEMultipart()
    message1['From'] = sender_address1
    message1['To'] = receiver_address1
    message1['Subject'] = 'E-Agri Kit- Agriculture Aid '
    message1.attach(MIMEText(mail_content1, 'plain'))
    session2 = smtplib.SMTP('smtp.gmail.com', 587)
    session2.starttls()
    session2.login(sender_address1, sender_pass1)
    text1 = message1.as_string()
    session2.sendmail(sender_address1, receiver_address1, text1)
    session2.quit()
    flash("Your opinon is shared with investor",   "success")
    return redirect(url_for('investorinfo'))

@app.route('/buyer')
def buyer():
    return render_template('buyer.html')

@app.route('/buyerback',methods = ["POST"])
def buyerback():
    if request.method=='POST':
        name=request.form['name']
        email=request.form['email']
        pwd=request.form['pwd']
        pno=request.form['ph']
        addr=request.form['addr']
        cpwd=request.form['cpwd']
        sql = "select * from buyers"
        result = pd.read_sql_query(sql, mydb)
        email1 = result['email'].values
        print(email1)
        if email in email1:
            flash("email already existed","warning")
            return render_template('buyer.html')
        if pwd==cpwd:
            sql = "INSERT INTO buyers (name,email,pwd,pno,addr) VALUES (%s,%s,%s,%s,%s)"
            val = (name, email, pwd, pno, addr)
            cursor.execute(sql, val)
            mydb.commit()
            flash("Successfully Registered", "success")
        else:
            flash("Password and Confirm password not same","danger")
        return render_template('buyer.html')
    return render_template('buyer.html')

@app.route('/buyerlog')
def buyerlog():
    return render_template('buyerlog.html')

@app.route('/buyerlogback',methods=['POST', 'GET'])
def buyerlogback():
    if request.method == 'POST':
        username = request.form['email']
        # opt = request.form['opt']
        password1 = request.form['pwd']

        sql = "select * from buyers where email='%s' and pwd='%s' " % (username, password1)
        x = cursor.execute(sql)
        results = cursor.fetchall()
        print(type(results))
        if not results:
            flash("Invalid Email / Password", "danger")
            return render_template('buyerlog.html')

        else:
            session['email'] = username
            if len(results) > 0:
                flash("Welcome ", "primary")
                session['name']=results[0][1]
                session['pno']=results[0][4]
                return render_template('buyerhome.html', msg=results[0][1])
    return render_template('buyerlog.html')

@app.route('/forgot')
def forgot():
    return render_template('forgot.html')

@app.route('/forgetback',methods=['POST', 'GET'])
def forgetback():
    if request.method == "POST":
        email = request.form['email']
        sql = "select count(*),name,pwd from buyers where email='%s'" % (email)
        x=pd.read_sql_query(sql, mydb)
        count=x.values[0][0]
        pwd=x.values[0][2]
        name=x.values[0][1]
        if count==0:
            flash("Email not valid try again","info")
            return render_template('forgot.html')
        else:
            msg = 'This your password : '
            t = 'Regards,'
            t1 = 'E-Agri Kit Services.'
            mail_content = 'Dear ' + name +','+'\n'+msg  +pwd+ '\n' + '\n' + t + '\n' + t1
            sender_address = 'taraksaik2036@gmail.com'
            sender_pass = 'raazahejryshyqsc'
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'E-Agri Kit- Agriculture Aid'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Password sent to your mail ", "success")
            return render_template("buyerlog.html")

    return render_template('forgot.html')

@app.route('/forgot1')
def forgot1():
    return render_template('forgot1.html')

@app.route('/forgetback1',methods=['POST', 'GET'])
def forgetback1():
    if request.method == "POST":
        email = request.form['email']
        sql = "select count(*),name,pwd from farmer where email='%s'" % (email)
        x=pd.read_sql_query(sql, mydb)
        count=x.values[0][0]
        pwd=x.values[0][2]
        name=x.values[0][1]
        if count==0:
            flash("Email not valid try again","info")
            return render_template('forgot1.html')
        else:
            msg = 'This your password : '
            t = 'Regards,'
            t1 = 'E-Agri Kit Services.'
            mail_content = 'Dear ' + name +','+'\n'+msg  +pwd+ '\n' + '\n' + t + '\n' + t1
            sender_address = 'taraksaik2036@gmail.com'
            sender_pass = 'raazahejryshyqsc'
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'E-Agri Kit- Agriculture Aid'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Password sent to your mail ", "success")
            return render_template("farmerlog.html")

    return render_template('forgot1.html')


@app.route('/forgot2')
def forgot2():
    return render_template('forgot2.html')

@app.route('/forgetback2',methods=['POST', 'GET'])
def forgetback2():
    if request.method == "POST":
        email = request.form['email']
        sql = "select count(*),name,pwd from investor where email='%s'" % (email)
        x=pd.read_sql_query(sql, mydb)
        count=x.values[0][0]
        pwd=x.values[0][2]
        name=x.values[0][1]
        if count==0:
            flash("Email not valid try again","info")
            return render_template('forgot2.html')
        else:
            msg = 'This your password : '
            t = 'Regards,'
            t1 = 'E-Agri Kit Services.'
            mail_content = 'Dear ' + name +','+'\n'+msg  +pwd+ '\n' + '\n' + t + '\n' + t1
            sender_address = 'taraksaik2036@gmail.com'
            sender_pass = 'raazahejryshyqsc'
            receiver_address = email
            message = MIMEMultipart()
            message['From'] = sender_address
            message['To'] = receiver_address
            message['Subject'] = 'E-Agri Kit- Agriculture Aid'
            message.attach(MIMEText(mail_content, 'plain'))
            ses = smtplib.SMTP('smtp.gmail.com', 587)
            ses.starttls()
            ses.login(sender_address, sender_pass)
            text = message.as_string()
            ses.sendmail(sender_address, receiver_address, text)
            ses.quit()
            flash("Password sent to your mail ", "success")
            return render_template("investorlog.html")

    return render_template('forgot2.html')

@app.route('/selling')
def selling():
    sql="select * from crop_prices"
    cursor.execute(sql)
    data=cursor.fetchall()
    mydb.commit()
    return render_template('selling.html',data=data)

@app.route('/sellback',methods = ["POST"])
def sellback():
    if request.method=='POST':
        cname=request.form['cname']
        addr=request.form['addr']
        q=request.form['q']
        fname=session.get('name')
        pno=session.get('pno')
        email=session.get('email')

        sql = "INSERT INTO crop_selling (fname,email,pno,addr,cname,quantity) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (fname, email, pno, addr, cname, q)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Successfully submitted", "success")

        return render_template('selling.html')
    return render_template('selling.html')

@app.route('/viewbuyer')
def viewbuyer():
    email=session.get('email')
    sql = "select * from selling_buying where femail='"+email+"' and status='pending' "
    x = pd.read_sql_query(sql, mydb)
    l=len(x)
    x = x.drop(['sid','fname', 'femail','msg','status'], axis=1)
    flash("No buyers are avalible","success")
    return render_template("viewbuyer.html", cal_name=x.columns.values, row_val=x.values.tolist(),l=l)


@app.route('/viewcrop')
def viewcrop():
    email=session.get('email')
    sql = "select * from crop_selling "
    x = pd.read_sql_query(sql, mydb)
    # x = x.drop(['fname', 'femail','fno','faddr','status'], axis=1)
    return render_template("viewcrop.html", cal_name=x.columns.values, row_val=x.values.tolist())


@app.route('/buy/<s>/<s1>/<s2>/<s3>/<s4>')
def buy(s=0,s1="",s2="",s3="",s4=0):
    sql = f'select * from crop_prices'
    cursor.execute(sql)
    data = cursor.fetchall()
    print(data)
    return render_template('buy.html',s=s,s1=s1,s2=s2,s3=s3,s4=s4,data=data)

@app.route('/buyback',methods=['POST','GET'])
def buyback():
    if request.method=="POST":
        cname = request.form['cname']
        q = request.form['q']
        quantity = request.form['quantity']
        fname = request.form['fname']
        id = request.form['id']
        femail = request.form['femail']
        addr = request.form['addr']
        email = session.get('email')
        name=session.get('name')
        pno=session.get('pno')
        total = request.form['total']
        print(name)
        sql = "INSERT INTO selling_buying (sid,fname,femail,bname,bemail,pno,addr,cname,quantity,buyer_need,total_amt) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (id, fname, femail, name, email,pno,addr, cname, quantity, q,total)
        cursor.execute(sql, val)
        mydb.commit()
        m = " Hi "
        otp = " is showing interest to buy your crop."
        t = 'Regards,'
        t1 = 'E-Agri Kit Services.'
        mail_content1 =  m + fname + ',' + '\n' + name + otp + '\n' + '\n' + t + '\n' + t1
        sender_address1 = 'taraksaik2036@gmail.com'
        sender_pass1 = 'raazahejryshyqsc'
        receiver_address1 = femail
        message1 = MIMEMultipart()
        message1['From'] = sender_address1
        message1['To'] = receiver_address1
        message1['Subject'] = 'E-Agri Kit- Agriculture Aid'
        message1.attach(MIMEText(mail_content1, 'plain'))
        session2 = smtplib.SMTP('smtp.gmail.com', 587)
        session2.starttls()
        session2.login(sender_address1, sender_pass1)
        text1 = message1.as_string()
        session2.sendmail(sender_address1, receiver_address1, text1)
        session2.quit()
        flash("Your opinion is shared with farmer, please wait for response","warning")
        return redirect(url_for('viewcrop'))

@app.route('/postdata/<s>/<s1>/<s2>/<s3>')
def postdata(s=0,s1="",s2="",s3=0):
    return render_template('postdata.html',s=s,s1=s1,s2=s2,s3=s3)
@app.route('/postdataback',methods=['POST','GET'])
def postdataback():
    if request.method=="POST":
        sno = request.form['sno']
        id = request.form['id']
        iemail = request.form['email']
        msg = request.form['msg']
        email = session.get('email')
        u_type="Farmer"
        sql = "INSERT INTO fund_chatting (i_id,f_id,user_type,femail,iemail,msg) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (id, sno, u_type, email, iemail,msg)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Your opinion is shared with investor, please wait for reply","warning")
        return redirect(url_for('investorinfo'))


@app.route('/investdata')
def investdata():
    email=session.get('email')
    sql = "select * from investment_data where iemail='"+email+"' and status='Accepted'"
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['iname', 'iemail','ino','iaddr','status','fno'], axis=1)
    return render_template("investdata.html", cal_name=x.columns.values, row_val=x.values.tolist())

@app.route('/postdata1/<s>/<s1>/<s2>/<s3>')
def postdata1(s=0,s1="",s2="",s3=0):
    return render_template('postdata1.html',s=s,s1=s1,s2=s2,s3=s3)

@app.route('/postdataback1',methods=['POST','GET'])
def postdataback1():
    if request.method=="POST":
        sno = request.form['sno']
        id = request.form['id']
        iemail = request.form['email']
        msg = request.form['msg']
        email = session.get('email')
        u_type="Investor"
        sql = "INSERT INTO fund_chatting (i_id,f_id,user_type,femail,iemail,msg) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (id, sno, u_type, email, iemail,msg)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Your opinion is shared with investor, please wait for reply","warning")
        return redirect(url_for('investdata'))

@app.route('/chatting/<s>/<s1>/<s2>/<s3>')
def chatting(s=0,s1="",s2="",s3=0):
    sql="select msg,user_type from fund_chatting where i_id='"+s+"' ORDER BY i_id"
    x = pd.read_sql_query(sql, mydb)

    return render_template('chatting.html',row_val=x.values.tolist(),x=x)

@app.route('/chatting1/<s>/<s1>/<s2>/<s3>')
def chatting1(s=0,s1="",s2="",s3=0):
    sql="select msg,user_type from fund_chatting where i_id='"+s+"' ORDER BY i_id"
    x = pd.read_sql_query(sql, mydb)

    return render_template('chatting1.html',row_val=x.values.tolist(),x=x)


@app.route('/investmentdata/<s>/<s1>/<s2>/<s3>/<s4>/<s5>/<s6>/<s7>/<s8>/<s9>')
def investmentdata(s=0,s1="",s2="",s3=0,s4="",s5="",s6="",s7="",s8="",s9=" "):

    return render_template('investmentdata.html',s=s,s1=s1,s2=s2,s3=s3,s4=s4,s5=s5,s6=s6,s7=s7,s8=s8,s9=s9)

@app.route('/invest1',methods=['POST','GET'])
def invest1():
    if request.method=="POST":
        sno = request.form['sno']
        id = request.form['id']
        cname = request.form['cname']
        yeild = request.form['yeild']
        iname = request.form['iname']
        iemail = request.form['iemail']
        # money = request.form['amount']
        s7 = request.form['s7']
        area = request.form['area']
        s8=request.form['s8']
        b_amount=request.form['b_amount']
        investment=request.form['investment']
        name=session.get('name')
        email=session.get('email')
        s=int(s7)
        # m=int(money)

        b_money=int(s8)
        p_money=int(investment)
        final_amount =(p_money*b_money)/100
        # final_amount =(b_money*s)/100
        sql = "INSERT INTO profit_data (fid,i_id,cname,yeild,area,money,share,i_money,profit,final_amount,fname,femail,iname,iemail) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (sno, id, cname,yeild,area,s7,s8,b_amount,investment,final_amount,name, email,iname, iemail)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Data submitted","warning")
        return redirect(url_for('investorinfo'))

@app.route('/viewmoney/<s>/<s1>')
def viewmoney(s=0,s1=0):
    email=session.get('email')
    print(s)
    # print(s1)
    sql="select * from profit_data where fid='"+s1+"' and i_id='"+s+"' and iemail='"+email+"'"
    x=pd.read_sql_query(sql,mydb)
    l=len(x)
    # if l==0:
    #     flash("Data not available","primary")
    #     return render_template('viewmoney.html',l=l)
    x=x.drop(['id','fid','i_id','iname','iemail'], axis=1)
    flash('Data not available', "info")
    return render_template('viewmoney.html',row_val=x.values.tolist(),l=l)


@app.route('/cancel1/<s>')
def cancel1(s=0):
    sql="delete from selling_buying where id='%s' "%(s)
    cursor.execute(sql,mydb)
    mydb.commit()
    flash("Data deleted","info")
    return redirect(url_for('viewbuyer'))

@app.route('/accept1/<s>/<s1>/<s2>')
def accept1(s=0,s1="",s2=""):
    name=session.get('name')
    print(name)
    sql="update selling_buying set status='Accepted' where id='"+s+"'"
    cursor.execute(sql, mydb)
    mydb.commit()
    msg = 'Hi'
    m=" Congratulations!! "
    otp = " has accepted your request"
    t = 'Regards,'
    t1 = 'E-Agri Kit Services.'
    mail_content1 = s1+ m + ','+ '\n' + name + otp +  '\n' + '\n' + t + '\n' + t1
    sender_address1 = 'taraksaik2036@gmail.com'
    sender_pass1 = 'raazahejryshyqsc'
    
    receiver_address1 = s2
    message1 = MIMEMultipart()
    message1['From'] = sender_address1
    message1['To'] = receiver_address1
    message1['Subject'] = 'E-Agri Kit- Agriculture Aid'
    message1.attach(MIMEText(mail_content1, 'plain'))
    session2 = smtplib.SMTP('smtp.gmail.com', 587)
    session2.starttls()
    session2.login(sender_address1, sender_pass1)
    text1 = message1.as_string()
    session2.sendmail(sender_address1, receiver_address1, text1)
    session2.quit()
    flash("Your opinon is shared with investor",   "success")
    return redirect(url_for('viewbuyer'))

@app.route('/viewbuyer1')
def viewbuyer1():
    email=session.get('email')
    sql = "select * from selling_buying where femail='"+email+"' and status='Accepted' and action='pending'"
    x = pd.read_sql_query(sql, mydb)
    l=len(x)
    x = x.drop(['sid','fname', 'femail','msg','status','action'], axis=1)
    flash("No buyers are avalible","success")
    return render_template("viewbuyer1.html", cal_name=x.columns.values, row_val=x.values.tolist(),l=l)
@app.route('/postdata2/<s>/<s1>/<s2>/<s3>')
def postdata2(s=0,s1="",s2="",s3=0):
    return render_template('postdata2.html',s=s,s1=s1,s2=s2,s3=s3)

@app.route('/postdataback2',methods=['POST','GET'])
def postdataback2():
    if request.method=="POST":
        sno = request.form['sno']
        id = request.form['id']
        iemail = request.form['email']
        msg = request.form['msg']
        email = session.get('email')
        u_type="Farmer"
        sql = "INSERT INTO buyer_chatting (i_id,f_id,user_type,femail,iemail,msg) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (id, sno, u_type, email, iemail,msg)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Your opinion is shared with investor, please wait for reply","warning")
        return redirect(url_for('viewbuyer1'))
@app.route('/chatting2/<s>/<s1>/<s2>/<s3>')
def chatting2(s=0,s1="",s2="",s3=0):
    sql="select msg,user_type from buyer_chatting where i_id='"+s+"' ORDER BY i_id"
    x = pd.read_sql_query(sql, mydb)

    return render_template('chatting2.html',row_val=x.values.tolist(),x=x)

@app.route('/croprequest')
def croprequest():
    email=session.get('email')
    sql = "select * from selling_buying where bemail='"+email+"' and status='Accepted' and action='pending'"
    x = pd.read_sql_query(sql, mydb)
    x = x.drop(['bname', 'bemail','pno','addr','msg','quantity'], axis=1)
    l=len(x)
    return render_template("croprequest.html", cal_name=x.columns.values, row_val=x.values.tolist(),l=l)


@app.route('/postdata3/<s>/<s1>/<s2>/<s3>')
def postdata3(s=0,s1="",s2="",s3=0):
    return render_template('postdata3.html',s=s,s1=s1,s2=s2,s3=s3)

@app.route('/postdataback3',methods=['POST','GET'])
def postdataback3():
    if request.method=="POST":
        sno = request.form['sno']
        id = request.form['id']
        iemail = request.form['email']
        msg = request.form['msg']
        email = session.get('email')
        u_type="Buyer"
        sql = "INSERT INTO buyer_chatting (i_id,f_id,user_type,femail,iemail,msg) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (id, sno, u_type, email, iemail,msg)
        cursor.execute(sql, val)
        mydb.commit()
        flash("Your opinion is shared with farmer, please wait for reply","warning")
        return redirect(url_for('croprequest'))

@app.route('/chatting3/<s>/<s1>/<s2>/<s3>')
def chatting3(s=0,s1="",s2="",s3=0):
    sql="select msg,user_type from buyer_chatting where i_id='"+s+"' ORDER BY i_id"
    x = pd.read_sql_query(sql, mydb)

    return render_template('chatting3.html',row_val=x.values.tolist(),x=x)

@app.route('/payment' , methods=['POST'])
def payment():
    if request.method == "POST":
        farmer_name = request.form.get('farmer_name')
        farmer_email = request.form.get('farmer_email')
        crop_name = request.form.get('crop_name')
        crop_qty = request.form.get('crop_qty')
        id = request.form.get('id')
        buyer_email=session.get('email')
        amount = request.form.get('amount')
        created_at = str(datetime.now())
        print("S.no of crop",id)
        
        sql = f'insert into payments values (default,%s,%s,%s,%s,%s,%s,%s);'
        data = (farmer_name,farmer_email,crop_name,crop_qty,amount,created_at,buyer_email)

        cursor.execute(sql , data)
        ss="update selling_buying set action='Completed' where id='"+id+"'"
        cursor.execute(ss)
        mydb.commit()

        return redirect(url_for('croprequest'))

@app.route('/viewpayment')
def viewpayment():
    sql="select * from  payments where farmer_email='"+session['email']+"'"
    cursor.execute(sql)
    data=cursor.fetchall()
    return render_template('viewpayment.html',data=data)


@app.route('/guide')
def guide():
    return render_template('guide.html')


if __name__=='__main__':
    app.run(debug=True,threaded=False)