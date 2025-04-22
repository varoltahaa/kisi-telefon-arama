from flask import Flask, render_template, request
import urllib.parse
import requests

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

def check_profile_links(usernames):
    platforms = ['instagram', 'twitter', 'github', 'facebook']
    results = []

    for user in usernames:
        for platform in platforms:
            url = f"https://{platform}.com/{user}"
            try:
                r = requests.get(url, timeout=3)
                results.append({
                    'url': url,
                    'exists': r.status_code == 200
                })
            except:
                results.append({
                    'url': url,
                    'exists': False
                })
    return results

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
    validated_profiles = check_profile_links(usernames)

    return render_template('results.html', name=name, phone=phone, queries=google_queries, profiles=validated_profiles)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
