
# 1. INITIALIZE APP
from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = "SECRET_KEY"

oauth = OAuth(app)

# 2. CONFIGURE OAUTH PROVIDER (GITHUB)
github = oauth.register(
    name='github',

    client_id='Ov23litNzTxRGwjOU9LT',

    client_secret='e82d91719e66b53e6377db71bac476d6cc194edb',

    access_token_url='https://github.com/login/oauth/access_token',

    authorize_url='https://github.com/login/oauth/authorize',

    api_base_url='https://api.github.com/',

    client_kwargs={'scope': 'user:email'},
)

auth0 = oauth.register(
    name='auth0',

    client_id='Ov23litNzTxRGwjOU9LT',

    client_secret='e82d91719e66b53e6377db71bac476d6cc194edb',

    access_token_url='https://github.com/login/oauth/access_token',

    authorize_url='https://github.com/login/oauth/authorize',

    api_base_url='https://api.github.com/',

    client_kwargs={'scope': 'openid profile email',},
)

# 3. LOGIN ROUTE
@app.route('/login')
def login():
    return github.authorize_redirect('http://localhost:5000/callback')

# 4. CALLBACK ROUTE
@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    user = github.get('user').json()

    session['user'] = user
    return redirect('/profile')

# 5. PROTECTED API
@app.route('/profile')
def profile():
    if 'user' not in session:
        return "Unauthorized Access", 401
    
    return jsonify(session['user'])

# BONUS PROTECTED API
@app.route('/api/secure-data')
def secure_data():

    if 'user' not in session:
        return jsonify({
            "error": "Unauthorized"
        }), 401

    return jsonify({
        "message": "This is protected secure data!",
        "user": session['user']['login']
    })

# 6. LOGOUT ROUTE
@app.route('/logout')
def logout():
    session.pop('user', None)
    return 'Logged out successfully'

# 7. UN APPLICATION
if __name__ == '__main__':
    app.run(debug=True)