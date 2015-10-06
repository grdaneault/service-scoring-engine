from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'eJw9zkELgjAYgOG_Et_Zg8q6CB6CmRR831gMZLsIlaalBVNRJ_73wkPH9_LwLpCXtugqiHo7FB7k9R2iBXZXiIAU'

if __name__ == '__main__':
    app.run()