import os
import re
import requests
from flask import Flask, request, Response

app = Flask(__name__)

VULNERABLE_APP_URL = "http://vulnerable_app:5000"

def sqli_filter(query_string):
    patterns = [r"(?i)(\bor\b|\band\b).*?=.*?", r"['\"]\s*--", r"union\b", r"1=1"]
    for pattern in patterns:
        if re.search(pattern, query_string):
            return True
    return False

def xss_filter(value):
    pattern = re.compile(r'(<script.*?>.*?</script.*?>|on\w+=|javascript:|<img.*?onerror=|<svg.*?onload=)', re.IGNORECASE)
    return bool(pattern.search(value))

@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    target_url = f"{VULNERABLE_APP_URL}/{path}"

    # --- Check GET parameters for XSS or SQLi ---
    query_string = request.query_string.decode()

    if os.getenv("ENABLE_SQLI_FILTER", "0") == "1" and sqli_filter(query_string):
        return Response("Blocked by SQLi filter", status=403)

    if os.getenv("ENABLE_XSS_FILTER", "0") == "1" and xss_filter(query_string):
        return Response("Blocked by XSS filter", status=403)

    # --- Check POST form data for XSS ---
    if request.method == "POST" and os.getenv("ENABLE_XSS_FILTER", "0") == "1":
        for key, value in request.form.items():
            if xss_filter(value):
                return Response("Blocked by XSS filter (POST body)", status=403)

    # Forward the request to the vulnerable app
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
