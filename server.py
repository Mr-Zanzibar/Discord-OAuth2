import requests
from flask import Flask, render_template, request



class OAuth2(object):
    api_endpoint  = "https://discord.com/api/v8"
    client_id     = ""      #your client id
    client_secret = ""      #your client secret
    redirect_uri  = ""      #your redirect uri

    @staticmethod
    def exchange_code(code):
        data = {
            'client_id': OAuth2.client_id,
            'client_secret': OAuth2.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': OAuth2.redirect_uri
            }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
            }

        r = requests.post(f"{OAuth2.api_endpoint}/oauth2/token", data=data, headers=headers)
        try:
            r.raise_for_status()
        except Exception:
            print(f"[err:] func(exchange_token){r.text}")
            return False

        to_return_json = {
            "access_token": r.json().get("access_token"),
            "refresh_token": r.json().get("refresh_token")
            }

        return to_return_json

    @staticmethod
    def refresh_token(refresh_token):
        data = {
            'client_id': OAuth2.client_id,
            'client_secret': OAuth2.client_secret,
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
            }
        
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
            }
        
        r = requests.post(f'{OAuth2.api_endpoint}/oauth2/token', data=data, headers=headers)
        try:
            r.raise_for_status()
        except Exception:
            print(f"[err:] func(refresh_token){r.text}")
            return False

        to_return_json = {
            "access_token": r.json().get("access_token"),
            "refresh_token": r.json().get("refresh_token")
            }

        return to_return_json

    @staticmethod
    def get_user_info(access_token):
        url = OAuth2.api_endpoint + "/users/@me"

        headers = {
            "Authorization": f"Bearer {access_token}"
            }
        
        r = requests.get(url=url, headers=headers)
        user_object = r.json()

        try:
            r.raise_for_status()
        except Exception:
            print(f"[err:] func(get_user_info)\n{r.text}")
            return False

        to_return_json = {
            "username": user_object.get("username") + "#" + user_object.get("discriminator"),
            "id": user_object.get("id"),
            "email": user_object.get("email"),
            "locale": user_object.get("locale")
            }

        return to_return_json



app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
    return render_template("404.html")



@app.route("/")
def index():
    return "Template from https://deepcrack.ml/"



@app.route("/verify")
def verify():
    return render_template("verify.html")



@app.route("/callback", methods=["GET"])
def callback():
    code = request.args.get("code")
    tokens = OAuth2.exchange_code(code)
    user_object = OAuth2.get_user_info(tokens.get("access_token"))

    to_save_data = {
        "username": user_object.get("username"),
        "id": user_object.get("id"),
        "email": user_object.get("email"),
        "locale": user_object.get("locale"),
        "refresh_token": tokens.get("refresh_token")
        }

    # save(to_save_data)

    return render_template("callback.html")



if __name__ == "__main__":
    app.run()
