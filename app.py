from seagull_settings import app
import os
app.secret_key = os.getenv("SECRET_KEY")
import routes

if not os.path.exists(os.getenv("UPLOAD_PATH")):
  os.mkdir(os.getenv("UPLOAD_PATH"))
