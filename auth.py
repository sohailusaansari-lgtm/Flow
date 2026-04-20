import google_auth_oauthlib.flow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json",
        SCOPES
    )

    # 🔥 FORCE redirect URI (fixes your error)
    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

    auth_url, _ = flow.authorization_url(prompt="consent")

    print("\n👉 Open this URL in your browser:\n")
    print(auth_url)

    code = input("\n🔑 Paste the code here: ")

    flow.fetch_token(code=code)

    creds = flow.credentials

    with open("token.json", "w") as f:
        f.write(creds.to_json())

    print("✅ OAuth DONE")

if __name__ == "__main__":
    authenticate()