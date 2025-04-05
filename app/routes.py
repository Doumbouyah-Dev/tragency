from flask import (
    Flask, render_template, request, redirect, url_for, flash, session, jsonify
)
from app import app, db, jwt, api
from app.models import Users, Tasks
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta
from app.resources.user import UserRegister


@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(UserRegister, "/register")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"].lower()
        password = request.form["password"]

        if Users.query.filter_by(email=email).first():
            flash("Email already registered", "danger")
            return redirect(url_for("register"))

        hashed_password = generate_password_hash(password)
        user = Users(username=username, email=email, password=hashed_password)
        user.save_to_db()
        flash("Registration successful. Please login.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email').lower()
        password = request.form.get('password')

        user = Users.query.filter((Users.email == identifier) | (Users.username == identifier)).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            access_token = create_access_token(identity=user.id, expires_delta=timedelta(days=1))
            flash("Login successful", "success")
            return redirect(url_for('task_list'))
        else:
            flash("Invalid credentials", "danger")

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login'))


@app.route('/dashboard')
def dashboard():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    user = Users.query.get(user_id)
    tasks = Tasks.query.filter_by(user_id=user_id).all()
    return render_template("dashboard.html", user=user, tasks=tasks)


@app.route("/create_task", methods=["GET", "POST"])
def create_task():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    if request.method == "POST":
        task = Tasks(
            taskname=request.form["taskname"],
            taskdescription=request.form["taskdescription"],
            startdate=request.form["startdate"],
            enddate=request.form["enddate"],
            status=request.form["status"],
            priority=request.form["priority"],
            visibility=request.form["visibility"],
            user_id=user_id
        )
        task.save_to_db()
        flash("Task created successfully!", "success")
        return redirect(url_for("task_list"))

    return render_template("create_task.html")


@app.route('/tasks')
def task_list():
    user_id = session.get("user_id")
    if not user_id:
        return redirect(url_for("login"))

    tasks = Tasks.query.filter_by(user_id=user_id).all()
    return render_template('tasks.html', tasks=tasks)


@app.route('/task/<int:task_id>')
def task_detail(task_id):
    task = Tasks.query.get(task_id)
    return render_template('task_detail.html', task=task)
