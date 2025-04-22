
from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    phone = request.form['phone']

    encoded_name = urllib.parse.quote_plus(name)
    encoded_phone = urllib.parse.quote_plus(phone)

    results = {
        "Google (İsim)": f"https://www.google.com/search?q={encoded_name}",
        "Google (Telefon)": f"https://www.google.com/search?q={encoded_phone}",
        "Facebook (İsim)": f"https://www.facebook.com/search/top?q={encoded_name}",
        "Instagram (Tahmini)": f"https://www.instagram.com/{name.replace(' ', '').lower()}/",
        "Twitter (X)": f"https://twitter.com/search?q={encoded_name}",
        "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={encoded_name}",
        "TrueCaller (Telefon)": f"https://www.truecaller.com/search/tr/{phone}"
    }

    return render_template('results.html', name=name, phone=phone, results=results)

if __name__ == '__main__':
    app.run(debug=True)
