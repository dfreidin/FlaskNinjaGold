from flask import Flask, render_template, redirect, request, session
import random
import time
app = Flask(__name__)
app.secret_key = "swordfish"
@app.route("/")
def index():
    if not session.get("gold"):
        session["gold"] = 0
    if not session.get("activities"):
        session["activities"] = []
    return render_template("index.html", gold=session["gold"], activities=session["activities"])
@app.route("/process_money", methods=["POST"])
def processMoney():
    activity = request.form["activity"]
    t = time.strftime("%c")
    gold = session["gold"]
    earnings = 0
    if activity == "reset":
        session["gold"] = 0
        session["activities"] = []
        return redirect("/")
    elif activity == "farm":
        earnings = random.randint(10,20)
    elif activity == "cave":
        earnings = random.randint(5,10)
    elif activity == "house":
        earnings = random.randint(2,5)
    elif activity == "casino":
        earnings = random.randint(-50,50)
        if gold + earnings < 0:
            earnings = gold * -1
    session["gold"] = gold + earnings
    a_str = "Earned " + str(earnings) + " gold at the " + activity + "! (" + t + ")"
    if earnings > 0:
        c = "pos"
    elif earnings < 0:
        a_str = "Entered a " + activity + " and lost " + str(earnings*-1) + " gold... Ouch... {" + t + ")"
        c = "neg"
    else:
        c = "eq"
    session["activities"].append([c,a_str])
    return redirect("/")
app.run(debug=True)