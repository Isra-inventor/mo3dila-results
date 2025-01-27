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
# Add this global variable to track debates and assignments
debates = ["AB", "CD", "EF", "GH", "AI","BC","DE","FG","HI"] 
assignments = {}  # To store which judge gets which debate

@app.route('/')
def index():
    # Sort teams based on their score in descending order
    sorted_teams = sorted(teams.items(), key=lambda x: x[1]['score'], reverse=True)

    # Prepare a list with team names, total scores, and speaker scores
    team_data = []

    for team, score_data in sorted_teams:
        speaker=[]
        for i in debatess.keys():
            if team in debatess[i]:
                speaker.append(debatess[i][team])
        team_dict = {
            'team': team,
            'score': score_data['score'],
            'speakers': str(speaker)
        }
        team_data.append(team_dict)
        print(team_dict)
    return render_template('main.html', team_data=team_data)


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
            team1=assigned_debate[0]
            team2=assigned_debate[1]
            if request.method == "POST":
                score11 = request.form.get("score11")
                score12 = request.form.get("score12")
                score13 = request.form.get("score13")
                score21 = request.form.get("score21")
                score22 = request.form.get("score22")
                score23 = request.form.get("score23")
                teams[team1]["score"]+=int(score11)+int(score12)+int(score13)
                teams[team2]["score"]+=int(score21)+int(score22)+int(score23)
                debatess[assigned_debate]={team1:"",team2:""}
                debatess[assigned_debate][team1]=str(score11)+", "+str(score12)+", "+str(score13)
                debatess[assigned_debate][team2]=str(score21)+", "+str(score22)+", "+str(score23)
                print(teams)
                print(debatess)
                
                return redirect(url_for("judge_portal"))  # Refresh the page

            return render_template("judge.html")

        # If the user is not authorized, redirect to login
        return redirect(url_for("login"))

@app.route("/participant-portal")
def participant_portal():
    if session.get("role") == "participant":
        return render_template("participant.html")
    return redirect(url_for("login"))

@app.route("/admin-portal", methods=["GET", "POST"])
def admin_portal():
    if session.get("role") == "admin":
        if request.method == "POST":
            # Get form data
            judge = request.form.get("judge")
            debate = request.form.get("debate")
            if judge and debate:
                # Assign the debate to the judge
                assignments[judge] = debate
                return redirect(url_for("admin_portal")) # Refresh the page

        # Render the admin page with judges, debates, and assignments
        judge_list = [user for user, info in users.items() if info["role"] == "judge"]
        return render_template(
            "admin.html",
            judges=judge_list,
            debates=debates,
            assignments=assignments
        )

    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run()
