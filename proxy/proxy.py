import os
import requests
from flask import Flask, request, Response
from filters.sqli_filter import is_enabled as sqli_enabled, detect_attack as detect_sqli
from filters.xss_filter import is_enabled as xss_enabled, detect_attack as detect_xss

app = Flask(__name__)

VULNERABLE_APP_URL = "http://vulnerable_app:5000"

@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    target_url = f"{VULNERABLE_APP_URL}/{path}"

    # --- Check SQLi (GET) ---
    if sqli_enabled() and detect_sqli(request.args):
        return Response("Blocked by SQLi filter", status=403)

    # --- Check XSS (GET) ---
    if xss_enabled():
        for value in request.args.values():
            if detect_xss(value):
                return Response("Blocked by XSS filter", status=403)

    # --- Check XSS (POST) ---
    if request.method == "POST" and xss_enabled():
        for value in request.form.values():
            if detect_xss(value):
                return Response("Blocked by XSS filter (POST body)", status=403)

    # Forward to vulnerable app
    resp = requests.request(
        method=request.method,
        url=target_url,
        params=request.args,
        data=request.form,
        headers={key: value for key, value in request.headers if key.lower() != 'host'},
    )
    return Response(resp.content, resp.status_code)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
