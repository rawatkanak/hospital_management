from flask import Flask, render_template, request, redirect, url_for, flash
import database
from scheduler import sort_appointments_fcfs
import os

app = Flask(__name__)
app.secret_key = "hospital_secret_key"

# Fresh DB on first run
if not os.path.exists("hospital.db"):
    database.create_tables()

@app.route("/")
def home():
    return redirect(url_for("view_schedule"))

# ---------------- ADD DOCTOR ----------------
@app.route("/add-doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        name = request.form["name"].strip()
        spec = request.form["spec"].strip()

        if not name or not spec:
            flash("Please enter doctor name and specialization", "error")
        else:
            database.add_doctor(name, spec)
            flash(f"Doctor '{name}' added successfully", "success")

    doctors = database.get_doctors()
    return render_template("add_doctor.html", doctors=doctors)

# ---------------- ADD PATIENT ----------------
@app.route("/add-patient", methods=["GET", "POST"])
def add_patient():
    doctors = database.get_doctors()

    if request.method == "POST":
        name = request.form["name"].strip()
        age = request.form["age"].strip()
        doctor_id = request.form.get("doctor")

        if not name or not age or not doctor_id:
            flash("All fields are required", "error")
        else:
            try:
                age = int(age)
                _, appt_no = database.add_patient_and_create_appointment(
                    name, age, int(doctor_id)
                )
                flash(f"Appointment created. Appointment No: {appt_no}", "success")
            except ValueError:
                flash("Age must be a number", "error")

    return render_template("add_patient.html", doctors=doctors)

# ---------------- VIEW SCHEDULE ----------------
@app.route("/schedule")
def view_schedule():
    rows = database.get_appointments()
    rows = sort_appointments_fcfs(rows)
    return render_template("schedule.html", schedule=rows)

# ---------------- CLEAR ALL ----------------
@app.route("/clear")
def clear_all():
    database.clear_patients_and_appointments()
    flash("All appointments cleared", "success")
    return redirect(url_for("view_schedule"))

if __name__ == "__main__":
    app.run(debug=True)
