from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "israabo@25"  # Needed for sessions

# Mock user data
users = {
    "malak06": {"role": "judge", "password": "malak6mo3dila"},
    "serine07": {"role": "judge", "password": "serine7paradox"},
    "soundous06": {"role": "judge", "password": "serine6paradox"},
    "sabrinama": {"role": "judge", "password": "sabrinamo3dila25"},
    "brahimoud": {"role": "judge", "password": "benoudinamo3dila25"},
    "profkihal": {"role": "judge", "password": "kihalselsabil25"},
    "eleid25":{"role":"judge", "password": "eleidmo3dila25"},
    "judge001":{"role":"judge", "password": "judge001mo3dila"},
    "judge002":{"role":"judge", "password": "judge002mo3dila"},
    "judge003":{"role":"judge", "password": "judge003mo3dila"},
    "judge004":{"role":"judge", "password": "judge004mo3dila"},
    "judge005":{"role":"judge", "password": "judge005mo3dila"},
    # Admin
    "isra": {"role": "admin", "password": "admin123"},
}
teams = {
    "A": {"score": 0},
    "B": {"score": 0},
    "C": {"score": 0},
    "D": {"score": 0},
    "E": {"score": 0},
    "F": {"score": 0},
    "G": {"score": 0},
    "H": {"score": 0},
    "I": {"score": 0},
}
debatess={}
speakers={"hy":0,"ha":0,"hm":0,"ik":0,"ic":0,"is":0,"dk":0,"dn":0,"da":0,"aj":0,"ah":0,"aa":0}
# Add this global variable to track debates and assignments
debates = ["AB", "CD", "EF", "GH", "AI","BC","DE","FG","HI"] 
assignments = {"malak06":"HI","soundous06":"HI","serine07":"DA","sabrinama":"HI","brahimoud":"HI","profkihal":"DA",
          "eleid25":"DA","judge001":"DA","judge002":"DA"}  # To store which judge gets which debate

@app.route('/')
def index():
    # Sort teams based on their score in descending order
    sorted_teams = sorted(teams.items(), key=lambda x: x[1]['score'], reverse=True)
    # Prepare a list with team names, total scores, and speaker scores
    team_data = []

    for team, score_data in sorted_teams:
        team_dict = {
            'team': team,
            'score': score_data['score'],
        }
        team_data.append(team_dict)
    return render_template('main.html', team_data=team_data, speakers=speakers)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate credentials
        user = users.get(username)
        if user and user["password"] == password:
            session["username"] = username
            session["role"] = user["role"]
            if user["role"] == "applicant":
                return redirect(url_for("applicant_portal"))
            elif user["role"] == "judge":
                return redirect(url_for("judge_portal"))
            elif user["role"] == "admin":
                return redirect(url_for("admin_portal"))
        else:
            return "Invalid username or password!"
    
    # If GET request, render the login form
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/shuffle")
def shuffle():
    return render_template("shuffle.html")
@app.route("/judge_portal", methods=["GET", "POST"])
def judge_portal():
        # Check if the user is logged in and is a judge
        if session.get("role") == "judge":
            username = session["username"]
            assigned_debate = assignments.get(username, None)  # Find the assigned debate for this judge
            if not assigned_debate:
                return f"No debate assigned to you. Contact the admin.", 403
            if request.method == "POST":
              if assigned_debate=="HI":
                score11 = request.form.get("scorehy")
                speakers["hy"]+=int(score11)
                score12 = request.form.get("scoreha")
                speakers["ha"]+=int(score12)
                score13 = request.form.get("scorehm")
                speakers["hm"]+=int(score13)
                score14 = request.form.get("scoreh")
                score21 = request.form.get("scoreis")
                speakers["is"]+=int(score21)
                score22 = request.form.get("scoreik")
                speakers["ik"]+=int(score22)
                score23 = request.form.get("scoreic")
                speakers["ic"]+=int(score23)
                score24 = request.form.get("scorei")
                teams["H"]["score"]+=int(score11)+int(score12)+int(score13)+int(score14)
                teams["I"]["score"]+=int(score21)+int(score22)+int(score23)+int(score24)              
                return redirect(url_for("judge_portal"))  # Refresh the page
              
              elif assigned_debate=="DA":
                score11 = request.form.get("scoredk")
                speakers["dk"]+=int(score11)
                score12 = request.form.get("scoredn")
                speakers["dn"]+=int(score12)
                score13 = request.form.get("scoreda")
                speakers["da"]+=int(score13)
                score14 = request.form.get("scored")
                score21 = request.form.get("scoreah")
                speakers["ah"]+=int(score21)
                score22 = request.form.get("scoreaj")
                speakers["aj"]+=int(score22)
                score23 = request.form.get("scoreaa")
                speakers["aa"]+=int(score23)
                score24 = request.form.get("scorea")
                teams["D"]["score"]+=int(score11)+int(score12)+int(score13)+int(score14)
                teams["A"]["score"]+=int(score21)+int(score22)+int(score23)+int(score24)              
                return redirect(url_for("judge_portal"))  # Refresh the page

            return render_template(f"{assigned_debate}.html")

        # If the user is not authorized, redirect to login
        return redirect(url_for("login"))

@app.route("/participant-portal")
def participant_portal():
    if session.get("role") == "participant":
        return render_template("participant.html")
    return redirect(url_for("login"))

@app.route("/admin-portal", methods=["GET", "POST"])
def admin_portal():
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
