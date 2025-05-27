import os
import re
import requests
from flask import Flask, request, Response

app = Flask(__name__)

VULNERABLE_APP_URL = "http://vulnerable_app:5000"

def sqli_filter(query_string):
    # Basic SQLi detection (simple pattern for demo purposes)
    patterns = [r"(?i)(\bor\b|\band\b).*?=.*?", r"['\"]\s*--", r"union\b", r"1=1"]
    for pattern in patterns:
        if re.search(pattern, query_string):
            return True
    return False

@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    target_url = f"{VULNERABLE_APP_URL}/{path}"
    query_string = request.query_string.decode()

    # Check for SQLi if filtering is enabled
    if os.getenv("ENABLE_SQLI_FILTER", "0") == "1":
        if sqli_filter(query_string):
            return Response("Blocked by SQLi filter", status=403)

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
