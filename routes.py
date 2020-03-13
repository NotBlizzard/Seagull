from flask import render_template, request, jsonify, send_from_directory, url_for, redirect
from db import session
from model import User, Image
from flask_login import current_user, login_user, logout_user
from seagull_settings import app, bcrypt, oauth
from oauth import github, oauth
import uuid
from model import User
import os
from werkzeug.utils import secure_filename
from operator import and_




@app.route("/")
def root():
  if current_user.is_authenticated:
    user = session.query(User).filter_by(id=current_user.get_id()).first()
    return render_template("hello.html", auth=True, user=user)
  else:
    return render_template("hello.html", auth=False, user=False)


@app.route("/<image_name>")
def get_image(image_name):
  return send_from_directory(os.getenv("UPLOAD_PATH"), image_name)

@app.route("/delete", methods=["POST"])
def delete():
  images = request.json['images']
  images_that_are_user = session.query(Image).filter(and_(Image.id.in_(images),Image.user_id == current_user.get_id())).all()
  # user owns every image sent from the client
  if len(images) == len(images_that_are_user):
    filenames = []
    for image in images_that_are_user:
      os.remove(os.path.join(os.getenv("UPLOAD_PATH"), image.image_path))


    session.query(Image).filter(Image.id.in_(images)).delete(synchronize_session=False)
   # images_for_deletion.delete()
    session.commit()

    return jsonify({"success": True, "deleted": images})

@app.route("/upload", methods=["POST"])
def upload():
  if not current_user.is_authenticated:
    return "Unauthorized", 401

  if 'file' not in request.files:
    return "Missing file", 400

  file = request.files['file']
  if file.filename == '':
    return "Invalid file", 400

  filename_split = os.path.splitext(file.filename)
  file.filename = f"{str(uuid.uuid4())}{filename_split[1]}"
  if file and filename_split[1] in ['.png', '.jpg', '.jpeg', '.gif']:
    file.save(os.path.join(os.getenv("UPLOAD_PATH"), file.filename))

  image = Image(user_id=current_user.get_id(), image_path=file.filename)
  session.add(image)
  session.commit()
  image = session.query(Image).filter_by(image_path=file.filename).first()
  return jsonify({"filename": file.filename, "id": image.id})



@app.route("/login", methods=["POST"])
def login():
  if current_user.is_authenticated:
    return jsonify({"error": "You are already authenticated."})

  if request.method == "POST":
    username = request.json["username"]
    password = request.json["password"]

    # check if the user exists
    user = session.query(User).filter_by(username=username).first()
    if not user:
      return jsonify({"error": "User does not exist."})

    is_user = bcrypt.check_password_hash(user.password, password)

    if not is_user:
      return jsonify({"error": "Invalid username and/or password."});

    login_user(user)
    return jsonify({"success": "You are now logged in"})

@app.route("/register", methods=["POST"])
def register():
  if current_user.is_authenticated:
    return jsonify({"error": "You are already authenticated."})

  if request.method == "POST":
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]

    # check if the user exists
    user_exists = session.query(User).filter_by(username=username).first()
    if user_exists:
      return jsonify({"error": "Username is taken."})

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
    user = User(username=username, password=hashed_password, email=email)
    session.add(user)
    session.commit()
    return jsonify({"success": "User created successfully."})

@app.route("/logout")
def logout():
  logout_user()
  return jsonify({"success": "You have been logged out successfully."})


@app.route("/github/")
def github_login():
  url = url_for('github_authorize', _external=True)
  return oauth.github.authorize_redirect(url)

@app.route("/github/callback")
def github_authorize():
  token = oauth.github.authorize_access_token()
  resp = oauth.github.get("https://api.github.com/user")
  profile = resp.json()

  # user might exist. if so, skip entire process, login user
  user_exist = session.query(User).filter_by(githubId=profile['id']).first()
  if user_exist:
    login_user(user_exist)
    return jsonify({'success': True})

  if profile['email']:
    user = session.query(User).filter_by(email=profile['email']).first()
    if user:
      user.githubId = profile['id']
    else:
      user = User(username=profile['login'],email=profile['email'],githubId=profile['id'])

    session.add(user)
    session.commit()
  else:
    user = session.query(User).filter_by(username=profile['login']).first()
    if user:
      user.githubId = profile['id']
    else:
      user = User(username=profile['login'],email=profile['email'],githubId=profile['id'])

    session.add(user)
    session.commit()

  return jsonify({'success': True})



