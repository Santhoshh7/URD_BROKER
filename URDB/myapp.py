from calendar import c
from subprocess import BELOW_NORMAL_PRIORITY_CLASS
from flask import Flask, render_template, request, jsonify, Response, json, redirect,url_for,flash,session
from flask_pymongo import PyMongo, ObjectId
from flask_session import Session
import re

URD=Flask(__name__)
URD.config['MONGO_URI']="mongodb://localhost:27017/myapp"
URD.config['SECRET_KEY']='987612345@SECRET'
URD.config["SESSION_PERMANENT"] = False
URD.config["SESSION_TYPE"] = "filesystem"
mongo = PyMongo(URD)
sessionv=Session(URD)

db=mongo.db.houses
db1=mongo.db.renter
db2=mongo.db.Tenant


@URD.route("/",methods=["GET","POST"])
def ehome():
    return render_template("home.html")

@URD.route("/Rhome",methods=["GET","POST"])
def Rhome():
    return render_template("Rhome.html")



@URD.route("/Thome",methods=["GET","POST"])
def Thome():
    return render_template("Thome.html")

@URD.route("/home",methods=["GET","POST"])
def home():
    return render_template("Rhome.html")


@URD.route("/Rlogin",methods=["GET","POST"])
def Rlogin():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        test=list(db.find({'email':request.form['email'],'password':request.form['password']},{"_id":0,"username":0}))
        check=list(db.find({'email':request.form['email'],'password':request.form['password']},{'name':0,'password':0,"_id":0,"email":0,"contact":0}))
        if((test) and (check[0]['option']=='RENTER')):
            session["email"]=email
            return redirect("/Renter")
        else:
            flash("Invalid Login")
            return redirect("/Rhome")

            



@URD.route("/Logout",methods=["GET","POST"])
def Logout():
    session["email"]=None
    return render_template("home.html")   


@URD.route("/TStatus",methods=["GET","POST"])

def TStatus():
    tdet=[]
    if 'email' in session:
        data=list(db2.find({}))
        for i in data:
            tdet.append(i)  
    return render_template("TStatus.html",tdet=tdet)       
                                

@URD.route("/Tlogin",methods=["GET","POST"])
def Tlogin():
        if request.method=="POST":
            email=request.form['email']
            password=request.form['password']
            
            test=list(db.find({'email':request.form['email'],'password':request.form['password']},{"_id":0,"name":0,"contact":0,"option":0}))
            check=list(db.find({'email':request.form['email'],'password':request.form['password']},{'name':0,'password':0,"_id":0,"email":0,"contact":0}))
            if((test) and (check[0]['option']=='TENANT')):
                session["email"]=email
                return redirect("/Tenant")
            else:
                flash("Invalid Login")
                return redirect("/Thome")

@URD.route("/Error",methods=["GET","POST"])
def ERR():
    return redirect("/")
    return render_template("error.html")

@URD.route("/Tenant",methods=["GET","POST"])
def Tenant():
    lst1=[]
    bemail=session["email"]
    ch=(list(db1.find({'bemail':bemail})))
    ch1=db.renter.find({'tid':{'$exists':{"$ne":None}}})
    if request.method=="POST":
        if(len(ch)<2):
            if (list((db1.find({'city':request.form.get('city'),'BHK':request.form.get('BHK'),'Htype':request.form.get('Htype'),'Ftype':request.form.get('Ftype'),'status':"None"})))):
                data=list(db1.find({'city':request.form.get('city'),'BHK':request.form.get('BHK'),'Htype':request.form.get('Htype'),'Ftype':request.form.get('Ftype')}))
                for i in data:
                    lst1.append(i)
            else:
                flash(f"Sorry no houses found")
        else:
            flash(f"You have already booked two houses")

    return render_template("Tenant.html",lst1=lst1)

@URD.route("/Tbook/<id>", methods=["POST"])
def Tbook(id):
    book = request.form.get('book')
    bemail=session["email"]
    i=list(db1.find({"_id":ObjectId(id)},{"_id":1}))
    i1=i[0]['_id']
    x=list(db1.find({"_id":ObjectId(id)}))

    id=db2.insert_one({
        'tid': i1,
        'city':x[0]['city'],
        'area':x[0]['area'],
        'landmark':x[0]['landmark'],
        'BHK':x[0]['BHK'],
        'Htype':x[0]['Htype'],
        'Ftype': x[0]['Ftype'],
        'rent':x[0]['rent'],
        'aemail':x[0]['aemail'],
        'bemail':bemail,
        'status':x[0]['status'],
        'Confirmation':x[0]['Confirmation'],
        'Meet':x[0]['Meet'],
        'comment':""
            })
    j=list(db2.find({"tid":i1},{"_id":0}))
    j1=j[0]['tid']

    if(book=="Requested"):
        m = db2.update_one({"tid":j1}, { "$set": { "Meet": "Requested", "Confirmation": 'Requested'} })
    elif(book=="Nmeet"):
        m1 = db2.update_one({"tid":j1}, { "$set": { "Meet": "Nmeet" ,"Confirmation": 'Nmeet'} })
    elif(book=="None"):
        m3 = db2.update_one({"tid":j1}, { "$set": { "Meet": "None" ,"Confirmation": 'None'} })

    l=list(db2.find({"tid":i1},{"_id":0}))
    l1=l[0]['tid']

    id=db1.insert_one({
        'tid': l1,
        'aemail':l[0]['aemail'],
        'bemail':bemail,
        'city':l[0]['city'],
        'area':l[0]['area'],
        'landmark':l[0]['landmark'],
        'BHK':l[0]['BHK'],
        'Htype':l[0]['Htype'],
        'Ftype': l[0]['Ftype'],
        'rent':l[0]['rent'],
        'status':"None",
        'Confirmation':"Requested",
        'Meet':"Requested",
        'comment':""
            })  

    return redirect(url_for('Tenant'))

@URD.route("/update/<id>",methods=["GET","POST"])
def update(id):
    udet=[]
    if request.method=="GET":
        data=list(db1.find({"_id":ObjectId(id)}))
        for i in data:
            udet.append(i)
    if request.method=="POST":
        print("hi")
        myqueryy = {'_id':ObjectId(id)}
        newvaluess = { "$set": {'city':request.form.get('city'),'area':request.form['area'],'landmark':request.form['lmark'],'BHK':request.form.get('BHK'),'Htype':request.form.get('Htype'),'Ftype':request.form.get('Ftype'),'rent':request.form['rent']}}
        yy = db1.update_many(myqueryy, newvaluess)
        flash("data updated")
    return render_template("update.html",udet=udet)
    

# @URD.route("/action/<id>",methods=["GET","POST"])
# def action(id):
#     action=request.form['action']
#     act=list(db1.find({'action':action},{"_id":0}))
    
#     return redirect(url_for('RStatus'))

@URD.route("/comment/<id>",methods=["GET","POST"])
def comment(id):
    h=list(db2.find({"_id":ObjectId(id)},{"_id":0,"tid":1}))
    h1=h[0]['tid']
    jl=list(db1.find({"tid":h1},{"_id":1}))
    jl1=jl[0]['_id']
    comment=request.form['comment']

    ch=(list(db2.find({"_id":ObjectId(id),"$or":[{"Meet":"Meet"},{'status':"House_booked"}]})))
    if(ch):
        w11 = db2.update_one({"_id":ObjectId(id)}, { "$set": { "comment": comment}})
        w1 = db1.update_one({"_id":jl1}, { "$set": { "comment": comment}})
        flash(f"commented")
    else:
        flash(f"You can't comment")
    return redirect(url_for('TStatus'))



@URD.route("/Delete/<id>",methods=["GET","POST"])
def dele(id):
    if 'email' in session:
        db1.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('RStatus'))

@URD.route("/TDelete/<id>",methods=["GET","POST"])
def Tdele(id):
    if 'email' in session:
        db2.delete_one({'_id':ObjectId(id)})
    return redirect(url_for('TStatus'))
    

@URD.route("/Renter",methods=["GET","POST"])

def Rent():
    global aemail
    a=0
    if request.method=="POST":
        city=request.form['city']
        area=request.form['area']
        lmark=request.form['lmark']
        BHK=request.form['BHK']
        Htype=request.form['Htype']
        Ftype=request.form['Ftype']
        rent=request.form['rent']
        req=request.form['req']
        aemail=session["email"]
        id=db1.insert_one({
        'city':city,
        'area':area,
        'landmark':lmark,
        'BHK':BHK,
        'req':req,
        'Htype': Htype,
        'Ftype': Ftype,
        'rent':rent,
        'aemail':aemail,
        'status':"None",
        'Confirmation':"None",
        'Meet':"None",
        'Book':"0",
        'comment':""
            })
        flash("data added successfully")

    return render_template("Renter.html")

@URD.route("/RStatus",methods=["GET","POST"])
def RStatus():
    det=[]
    if 'email' in session:
        data=list(db1.find({"aemail":session["email"]}))
        for i in data:
            det.append(i)
    return render_template("RStatus.html",det=det)    

@URD.route("/status/<id>",methods=["GET","POST"])
def book(id):
    status=request.form['status']
    
    if(list(db1.find({'_id':ObjectId(id), "Meet": {'$in' : ["Meet","Nmeet"]}}))):
        if(status=="Req_Accepted"):
            t=list(db1.find({'_id':ObjectId(id)},{"_id":0,"tid":1}))
            t1=t[0]['tid']
            r=list(db2.find({"tid":ObjectId(t1)},{"_id":0,"tid":1}))
            r1=r[0]['tid']
            q21=db2.update_many({"tid":r1}, { "$set":{"status": "House_Booked","Confirmation": "Req_Accepted"}})
            Q3=db1.update_many({"_id":ObjectId(id)}, { "$set":{"status": "House Booked","Confirmation": "House_Booked"}})
            Q3=db1.update_many({"_id":r1}, { "$set":{"status": "House Booked","Confirmation": "House_Booked"}})
        elif(status=="Deny"):
            t5=list(db1.find({'_id':ObjectId(id)},{"_id":0,"tid":1}))
            t6=t5[0]['tid']
            r1=list(db2.find({"tid":ObjectId(t1)},{"_id":0,"tid":1}))
            r11=r1[0]['tid']
            q211=db2.update_many({"tid":r11}, { "$set":{"status": "Booking_Denied","Confirmation": "Booking_Denied"}})
            Q31=db1.update_many({"_id":ObjectId(id)}, { "$set":{"status": "Booking_Denied","Confirmation": "Booking_Denied"}})
            Q32=db1.update_many({"_id":r11}, { "$set":{"status": "None","Confirmation": "None"}})
    elif(status=="None"):
            t51=list(db1.find({'_id':ObjectId(id)},{"_id":0,"tid":1}))
            t61=t51[0]['tid']
            r121=list(db2.find({"tid":ObjectId(t61)},{"_id":0,"tid":1}))
            r111=r121[0]['tid']
            q1211=db2.update_many({"tid":r111}, { "$set":{"status": "None","Confirmation": "None"}})
            Q1311=db1.update_many({"_id":ObjectId(id)}, { "$set":{"status": "None","Confirmation": "None"}})
            Q132=db1.update_many({"_id":r11}, { "$set":{"status": "None","Confirmation": "None"}})
    return redirect(url_for('RStatus'))    

@URD.route("/rmeet/<id>",methods=["GET","POST"])
def rmeet(id):
    rmeet=request.form['rmeet']
    if(list(db1.find({'_id':ObjectId(id),'Meet': 'Requested'}))):
        if(rmeet=="Accept"):
            q1=db1.update_many({"_id":ObjectId(id)}, { "$set":{"Meet": "Meet","Confirmation": "Meet_Accepted"}})
            t=list(db1.find({'_id':ObjectId(id)},{"_id":0,"tid":1}))
            t1=t[0]['tid']
            r=list(db2.find({"tid":ObjectId(t1)},{"_id":0,"tid":1}))
            r1=r[0]['tid']
            x14 = db2.update_many({"tid":r1}, { "$set": { "Meet":"Meet","Confirmation": "Accepted" } })
        elif(rmeet=="Deny"):
            mq1=db1.update_many({"_id":ObjectId(id)}, { "$set":{"Meet": "Denied","Confirmation": "Denied"}})
            mt=list(db1.find({'_id':ObjectId(id)},{"_id":0,"tid":1}))
            mt1=mt[0]['tid']
            mr=list(db2.find({"tid":ObjectId(t1)},{"_id":0,"tid":1}))
            mr1=mr[0]['tid']
            mx14 = db2.update_many({"tid":mr1}, { "$set": { "Meet":"Denied","Confirmation": "Denied" } })
    elif(rmeet=="None"):
        nmq1=db1.update_many({"_id":ObjectId(id)}, { "$set":{"Meet": "None","Confirmation": "None"}})
        nmt=list(db1.find({'_id':ObjectId(id)},{"_id":0,"tid":1}))
        nmt1=nmt[0]['tid']
        nmr=list(db2.find({"tid":ObjectId(t1)},{"_id":0,"tid":1}))
        nmr1=nmr[0]['tid']
        nmx14 = db2.update_many({"tid":nmr1}, { "$set": { "Meet":"None","Confirmation": "None" } })
    return redirect(url_for('RStatus'))    



@URD.route("/Signup",methods=["POST","GET"])
def Signup():
    if request.method=="POST":
        name=request.form['username']
        password=request.form['password']
        email=request.form['email']
        contact=request.form['contact']
        option=request.form['option'] 
        dist_mail=list(db.find({'email':request.form['email']}))
        if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):

            flash(f"Please enter a valid email id")

        elif(dist_mail):
            flash(f'"email already exists please enter a new email"','danger')

        elif not re.fullmatch(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,10}$', password):
            flash(f"Password should contain 8-10 characters with atleast 1 uppercase letter, lowercase letter, digit, and a special character")

        else:

            id=db.insert_one({
                'name':name,
                'email':email,
                'password':password,
                'contact':contact,
                'option':option
            })
            flash("Signup Succesful")
            return redirect("/")
    return render_template("Signup.html")


@URD.route("/Tstatus/<id>",methods=["GET","POST"])
def tstatus(id):
    tstatus=request.form['tstatus']
    if(list(db2.find({'_id':ObjectId(id), "Confirmation":"Accepted"}))):
        i=list(db2.find({"_id":ObjectId(id)},{"_id":0,"tid":1,"bemail":1}))
        i1=i[0]['tid']
        i2=i[0]['bemail']
        if(tstatus=="Final_Request"):
            q1=db2.update_many({"_id":ObjectId(id)}, { "$set":{"status": "Final_Request","Confirmation": "Final_Request"}})
            Q3=db1.update_many({"tid":i1,"bemail":i2}, { "$set":{"status": "Final_Request","Confirmation": "Final_Request"}})
        elif(tstatus=="Deny"):
            mq1=db2.update_many({"_id":ObjectId(id)}, { "$set":{"status": "Deny","Confirmation": "Deny"}})
            mQ3=db1.update_many({"tid":i1,"bemail":i2}, { "$set":{"status": "Deny","Confirmation": "Deny"}})
    elif(tstatus=="None"):
        nmq1=db2.update_many({"_id":ObjectId(id)}, { "$set":{"status": "None","Confirmation": "None"}})
        nmQ3=db1.update_many({"tid":i1,"bemail":i2}, { "$set":{"status": "None","Confirmation": "None"}})
    return redirect(url_for('TStatus')) 



if __name__ == "__main__":
    URD.run(debug=True,port=2023)