from flask import Flask, request, render_template, send_from_directory
import data.blood as becsClass
import json
from csv import reader, writer
import datetime
import os

becs = Flask(__name__)
bloodbank = becsClass.BECS()
file = "api/data/user.json"

#User login helper function
def loggedIn(userName):
    with open(file) as data:
        decoded = json.load(data)
    
    if userName in decoded.keys():
        lastAction = decoded[userName]["last_action"] 
        timeList = lastAction.split("-")
        if(elapsedBool(timeList) == True):
            if decoded[userName]["logged_in"] == True:
                return True
        else:
            decoded[userName]["logged_in"] = False
            with open(file, 'w') as data:
                json.dump(decoded, data)
    return False

#Determination of time elapsed since last action
def elapsedBool(times): #Change this to a simpler chaeck using datetime.time()
    currTime = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S").split("-")
    
    #Months or yeasrs apart is too much apart
    if currTime[1] != times[1] or currTime[2] != times[2]:
        return False

    #Two days apart and up
    if int(currTime[0]) - int(times[0]) > 1:
        return False
    
    #Adjacent days
    elif int(currTime[0]) - int(times[0]) == 1:
        if int(times[3]) - int(currTime[3]) > 1:
            return True #Less than 24 hours elapsed
        elif int(times[3]) == int(currTime[3]):
            if int(times[4]) - int(currTime[4]) > 1:
                return True #Same hours, so minutes are checked
            elif int(times[4]) == int(currTime[4]):
                if int(times[5]) - int(currTime[5]) >=0:
                    return True #Same hours and minutes, so seconds are checked
                else:
                    return False
            else:
                return False
        else:
            return False
    
    #Same day is always OK - That's the last option
    else:
        return True

#Check if a user is student, regula user or administrator
def isStudent(user):
    with open(file) as data:
        decoded = json.load(data)
    
    if decoded[user]["status"] == "student":
        return True
    else:
        return False

def isUser(user):
    with open(file) as data:
        decoded = json.load(data)
    
    if decoded[user]["status"] == "user":
        return True
    else:
        return False

def isAdmin(user):
    with open(file) as data:
        decoded = json.load(data)
    
    if decoded[user]["status"] == "admin":
        return True
    else:
        return False

#Logging function
def logAction(date, time, user, action):
    logFile = becs.root_path+f"/logfiles/log_{date}.txt"
    logLine = f"{time}: {user} - {action}\n"
    with open(logFile, 'a+') as log:
        log.write(logLine)

#Updating last action for the user
def updateLastAction(user):
    with open(file) as data:
        decoded = json.load(data)
        decoded[user]["last_action"] = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    with open(file, "w") as data:
        json.dump(decoded, data)

#Blood pack handling API

@becs.route("/api/<string:user>/add_portion", methods=["POST"])
def addPortion(user):
    if loggedIn(user):
        if isAdmin(user) or isUser(user):
            data = request.form["bgr"]+request.form["rh"]
            res = bloodbank.addNewPortion(data)
            msg = f"Successfully added a new portion: {res[0]}. Current amount: {res[1]}."
            resultData = ("one", msg)

            updateLastAction(user)

            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = f"Submitted portion {res[0]} to blood bank"
            logAction(date, time, user, action)

            return render_template("front/confirmation.html", message=resultData, user=user)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted submission to blood bank as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/get_portion", methods=["POST"])
def getPortion(user):
    if loggedIn(user):
        if isAdmin(user) or isUser(user):
            data = request.form["bgr"]+request.form["rh"]
            urgency = request.form["urg"]
            res = bloodbank.withdrawPortion(data, urgency)
            if res[0] == "None":
                msg = "No suitable donors were found."
            else:
                msg = f"Pulled portion is: {res[0]}. Current amount left: {res[1]}."
            resultData = ("one", msg)

            updateLastAction(user)
            
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = f"Pulled portion {res[0]} from blood bank"
            logAction(date, time, user, action)
            
            return render_template("front/confirmation.html", message=resultData, user=user)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted withdrawal from blood bank as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/get_portions", methods=["POST"])
def getPortions(user):
    if loggedIn(user):
        if isAdmin(user) or isUser(user):
            ap = ("A+", int(request.form["ap"]))
            op = ("O+", int(request.form["op"]))
            bp = ("B+", int(request.form["bp"]))
            abp = ("AB+", int(request.form["abp"]))
            am = ("A-", int(request.form["am"]))
            om = ("O-", int(request.form["om"]))
            bm = ("B-", int(request.form["bm"]))
            abm = ("AB-", int(request.form["abm"]))
            data = (ap, op, bp, abp, am ,om ,bm ,abm)
            res = bloodbank.massWithdrawal(data) #receives a triple of pulled, unpulled and bool of whether a partial pull was performed
            if res[2] == False:
                msg = f"Successfully pulled the following packs and amounts:"
            else:
                msg = "Some types have no donors. Pullled packs:"
            resultData = ("many", msg, res)

            updateLastAction(user)
            
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = f"Pulled portions {res} to blood bank"
            logAction(date, time, user, action)
            
            return render_template("front/confirmation.html", message=resultData, user=user)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted MCI mass withdrawal from blood bank as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

#User profile control API

@becs.route("/api/signup", methods=["POST"])
def signup():
    userData = request.form
    user = {
        "first_name": userData["fname"],
        "last_name": userData["lname"],
        "id": userData["id"],
        "title": userData["title"],
        "pass": userData["pass"],
        "email": userData["mail"],
        "status": "user",
        "logged_in": False,
        "last_action": ""
    }
    with open(file) as data:
        decoded = json.load(data)
    
    if userData["id"] not in decoded.keys():
        decoded[userData["id"]] = user
        with open(file, "w") as data:
            json.dump(decoded, data)
        res = "User added successfully"
        action = "Signed up to BECS"

    else:
        res = "User exists, check your details"
        action = "Attempted sign up with existing ID"
    
    #Logging to relevant log file
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    time = datetime.datetime.now().strftime("%H-%M-%S")
    logAction(date, time, userData["id"], action)

    return render_template("front/signup.html", message=res)

@becs.route("/api/login", methods=["POST"])
def login():
    user = request.form

    with open(file) as data:
        decoded = json.load(data)
    
    if user["id"] in decoded.keys():
        udata = decoded[user["id"]]
        if user["pass"] == udata["pass"]:
            udata["logged_in"] = True
            udata["last_action"] = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
            decoded[user["id"]] = udata
            with open(file, "w") as outfile:
                json.dump(decoded, outfile)
            
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Successfully logged in"
            logAction(date, time, user["id"], action)

            return render_template("front/amounts.html", message=bloodbank.getPackCounts(), user=udata["id"])

        else:
            msg = "Wrong password"
            action = "Attempted login with wrong password"
    else:
        msg = "User not signed up"
        action = "Attempted login without signing up"
    
    #Logging to relevant log file
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    time = datetime.datetime.now().strftime("%H-%M-%S")
    logAction(date, time, user["id"], action)
    
    return render_template("front/index.html", message=msg)

@becs.route("/api/<string:user>/update", methods=["POST"])
def updateDetails(user):
    if loggedIn(user):
        updated = request.form
        with open(file) as data:
            decoded = json.load(data)
        userData = decoded[user]

        if updated["fname"] != "":
            userData["first_name"] = updated["fname"]
        if updated["lname"] != "":
            userData["last_name"] = updated["lname"]
        if updated["id"] != "":
            userData["id"] = updated["id"]
        if updated["title"] != "":
            userData["title"] = updated["title"]
        if updated["pass"] != "":
            userData["pass"] = updated["pass"]
        if updated["email"] != "":
            userData["email"] = updated["email"]

        decoded[user] = userData
        with open(file, "w") as outfile:
            json.dump(decoded, outfile)
        res = "Updated successfully"

        updateLastAction(user)

        #Logging to relevant log file
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        time = datetime.datetime.now().strftime("%H-%M-%S")
        action = "Updated self user details"
        logAction(date, time, user, action)

        return render_template(f"front/user.html", user=user, data=userData, message=res)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/make_admin", methods=["POST"])
def makeAdmin(user):
    if loggedIn(user):
        if isAdmin(user):
            targetUser = request.form["adminize"]
            with open(file) as data:
                decoded = json.load(data)
            userData = decoded[user]

            if targetUser == user:
                res = "You already are an administrator"
            else:
                if targetUser in decoded.keys():
                    decoded[targetUser]["status"] = "admin"
                    with open(file, "w") as outfile:
                        json.dump(decoded, outfile)
                    res = f"User {targetUser} changed to ADMINISTRATOR"
                else:
                    res = f"User {targetUser} wasn't found in database"

            updateLastAction(user)

            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = f"Made user {targetUser} administrator"
            logAction(date, time, user, action)

            return render_template(f"front/user.html", user=user, data=userData, message=res)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted changing someone's privileges to ADMIN as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/make_user", methods=["POST"])
def makeUser(user):
    if loggedIn(user):
        if isAdmin(user):
            targetUser = request.form["userize"]
            with open(file) as data:
                decoded = json.load(data)
            userData = decoded[user]

            if targetUser == user:
                res = "You can't downdrade yourself"
            else:
                if targetUser in decoded.keys():
                    decoded[targetUser]["status"] = "user"
                    with open(file, "w") as outfile:
                        json.dump(decoded, outfile)
                    res = f"User {targetUser} changed to USER"
                else:
                    res = f"User {targetUser} wasn't found in database"

            updateLastAction(user)

            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = f"Made user {targetUser} regular user"
            logAction(date, time, user, action)

            return render_template(f"front/user.html", user=user, data=userData, message=res)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted changing someone's privileges to USER as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/make_student", methods=["POST"])
def makeStudent(user):
    if loggedIn(user):
        if isAdmin(user):
            targetUser = request.form["studentize"]
            with open(file) as data:
                decoded = json.load(data)
            userData = decoded[user]

            if targetUser == user:
                res = "You can't downdrade yourself"
            else:
                if targetUser in decoded.keys():
                    decoded[targetUser]["status"] = "student"
                    with open(file, "w") as outfile:
                        json.dump(decoded, outfile)
                    res = f"User {targetUser} changed to STUDENT"
                else:
                    res = f"User {targetUser} wasn't found in database"

            updateLastAction(user)

            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = f"Made user {targetUser} research student"
            logAction(date, time, user, action)

            return render_template(f"front/user.html", user=user, data=userData, message=res)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted changing someone's privileges to USER as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/delete_user", methods=["POST"])
def deleteUser(user):
    if loggedIn(user):
        if isAdmin(user):
            targetUser = request.form["remove"]
            with open(file) as data:
                decoded = json.load(data)
            userData = decoded[user]

            if targetUser == user:
                res = "You can't remove yourself"
            else:
                if targetUser in decoded.keys():
                    del decoded[targetUser]
                    with open(file, "w") as outfile:
                        json.dump(decoded, outfile)
                    res = f"User {targetUser} was deleted"
                else:
                    res = f"User {targetUser} wasn't found in database"

            updateLastAction(user)

            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = f"Deleted user {targetUser} from database"
            logAction(date, time, user, action)

            return render_template(f"front/user.html", user=user, data=userData, message=res)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted deletig a user as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/get_logs", methods=["POST"])
def getLogs(user):
    if loggedIn(user):
        if isAdmin(user):
            logFileDir = becs.root_path+'/logfiles/'
            data = request.form
            logDate = [ data['s_day'], data['s_month'], data['s_year'] ]

            if "" in logDate:
                msg = "Entered bad date"
                return render_template(f"front/logexport.html", message=msg, user=user)
            
            directory = os.fsencode(logFileDir)
            for fname in os.listdir(directory):
                fname_str = os.fsdecode(fname)
                if fname_str == f"log_{logDate[0]}-{logDate[1]}-{logDate[2]}.txt":
                    #Logging to relevant log file
                    sd = f"{logDate[0]}/{logDate[1]}/{logDate[2]}"
                    date = datetime.datetime.now().strftime("%d-%m-%Y")
                    time = datetime.datetime.now().strftime("%H-%M-%S")
                    action = f"Downloaded logs from date {sd}"
                    logAction(date, time, user, action)
                    return send_from_directory(logFileDir, fname_str, as_attachment=True)
                else:
                    #Logging to relevant log file
                    sd = f"{logDate[0]}/{logDate[1]}/{logDate[2]}"
                    date = datetime.datetime.now().strftime("%d-%m-%Y")
                    time = datetime.datetime.now().strftime("%H-%M-%S")
                    action = f"Failed request for logs from date {sd} - no logs found"
                    logAction(date, time, user, action)
                    return render_template(f"front/logexport.html", message="File not found", user=user)
        else:
            #Logging to relevant log file
            date = datetime.datetime.now().strftime("%d-%m-%Y")
            time = datetime.datetime.now().strftime("%H-%M-%S")
            action = "Attempted pulling log files as student"
            logAction(date, time, user, action)
            return render_template("front/confirmation.html", message="Unauthorized user for this action - STUDENT", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/api/<string:user>/logout", methods=["POST"])
def logout(user):
    if loggedIn(user):
        with open(file) as data:
            decoded = json.load(data)
        userData = decoded[user]
        userData["logged_in"] = False
        decoded[user] = userData
        with open(file, "w") as outfile:
            json.dump(decoded, outfile)
        
        #Logging to relevant log file
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        time = datetime.datetime.now().strftime("%H-%M-%S")
        action = "Logged out of BECS"
        logAction(date, time, user, action)

        return redirectToHome("Logged out")
    else:
        return redirectToHome("Sign up or log in first")

#Route handling for HTML requests

@becs.route("/", methods=["GET", "POST"])
def redirectToHome(msg=""):
    return render_template("front/index.html", message=msg)

@becs.route("/<string:user>/<page>", methods=["GET", "POST"])
def redirect(user, page):
    if loggedIn(user):
        updateLastAction(user)

        #Logging to relevant log file
        date = datetime.datetime.now().strftime("%d-%m-%Y")
        time = datetime.datetime.now().strftime("%H-%M-%S")
        action = f"Redirected to page {page}"
        logAction(date, time, user, action)

        if page == "amounts.html":
            return render_template(f"front/amounts.html", message=bloodbank.getPackCounts(), user=user)
        elif page == "user.html":
            with open(file) as data:
                decoded = json.load(data)
            userData = decoded[user]
            return render_template(f"front/user.html", user=user, data=userData)
        else:
            return render_template(f"front/{page}", user=user)
    else:
        return redirectToHome("Sign up or log in first")

@becs.route("/signup.html", methods=["GET", "POST"])
def signupPage():
    return render_template(f"front/signup.html", message="")


#Runner

if __name__ == "__main__":
    becs.run(debug=True, host="0.0.0.0", port="5000")