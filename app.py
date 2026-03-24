from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "API funcionando 🚀"

if __name__ == "__main__":
    app.run()
git init
git add .
git commit -m "backend pronto"
git branch -M main
git remote add origin https://github.com/vakiutialexandre/amg-backend.git
git push -u origin main
