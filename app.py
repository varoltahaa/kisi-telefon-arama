from flask import Flask, render_template, request
import urllib.parse

app = Flask(__name__)

def generate_usernames(name):
    parts = name.lower().split()
    usernames = []
    if len(parts) >= 2:
        first, last = parts[0], parts[1]
        usernames = [
            f"{first}{last}", f"{first}.{last}", f"{first}_{last}",
            f"{first[0]}.{last}", f"{last}.{first}", f"{first}{last}123"
        ]
    else:
        usernames = [name.lower()]
    return usernames

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    name = request.form['name']
    phone = request.form['phone']
    encoded_name = urllib.parse.quote_plus(name)
    encoded_phone = urllib.parse.quote_plus(phone)

    google_queries = {
        "Facebook": f"https://www.google.com/search?q=site:facebook.com+%22{encoded_name}%22",
        "Instagram": f"https://www.google.com/search?q=site:instagram.com+%22{encoded_name}%22",
        "Twitter": f"https://www.google.com/search?q=site:twitter.com+%22{encoded_name}%22",
        "LinkedIn": f"https://www.google.com/search?q=site:linkedin.com+%22{encoded_name}%22",
        "Telefon Araması": f"https://www.google.com/search?q={encoded_phone}"
    }

    usernames = generate_usernames(name)
    sherlock_links = [f"https://{platform}.com/{user}" for user in usernames for platform in ['instagram', 'twitter', 'github', 'facebook']]

    return render_template('results.html', name=name, phone=phone, queries=google_queries, usernames=sherlock_links)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
