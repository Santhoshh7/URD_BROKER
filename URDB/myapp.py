from flask import Flask, render_template, request, jsonify, Response, json, redirect,url_for
from flask_pymongo import PyMongo, ObjectId

URD=Flask(__name__)
URD.config['MONGO_URI']="mongodb://localhost:27017/myapp"
mongo = PyMongo(URD)

db=mongo.db.houses
@URD.route("/",methods=["GET","POST"])
def ehome():
    return render_template("home.html")

@URD.route("/Rhome",methods=["GET","POST"])
def Rhome():
    db=mongo.db.renter

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
        name=request.form['username']
        password=request.form['password']
        test=list(db.find({'name':request.form['username'],'password':request.form['password']},{"_id":0,"email":0}))
        check=list(db.find({'name':request.form['username'],'password':request.form['password']},{'name':0,'password':0,"_id":0,"email":0,"contact":0}))
        print(check)
        if((test) and (check[0]['option']=='R')):
            return redirect("/Renter")
        else:
            return redirect("/Error")

        
                                

@URD.route("/Tlogin",methods=["GET","POST"])
def Tlogin():
        if request.method=="POST":
            name=request.form['username']
            password=request.form['password']
            test=list(db.find({'name':request.form['username'],'password':request.form['password']},{"_id":0,"email":0}))
            check=list(db.find({'name':request.form['username'],'password':request.form['password']},{'name':0,'password':0,"_id":0,"email":0,"contact":0}))
            if((test) and (check[0]['option']=='T')):
                return redirect("/Tenent")
            else:
                return redirect("/Error")

@URD.route("/Error",methods=["GET","POST"])
def ERR():
    if request.method=="POST":

        return redirect("/")
    return render_template("error.html")

@URD.route("/Renter",methods=["GET","POST"])
def Rent():
        return render_template("Renter.html")

@URD.route("/Tenent",methods=["GET","POST"])
def Tenent():
        return render_template("Tenent.html")

@URD.route("/Signup",methods=["POST","GET"])
def Sign():
    if request.method=="POST":
        print("welcomeimm")
        name=request.form['username']
        password=request.form['password']
        email=request.form['email']
        contact=request.form['contact']
        option=request.form['option']
        print("helo")
        print(name)
        id=db.insert_one({
            'name':name,
            'password':password,
            'email':email,
            'contact':contact,
            'option':option
        })
        return redirect("/")
    return render_template("Signup.html")


if __name__ == "__main__":
    URD.run(debug=True,port=2023)