import os
import requests
from flask import Flask, request, Response

# Import SQLi and XSS filter configuration and detection logic
from filters.sqli_filter import is_enabled as sqli_enabled, detect_attack as detect_sqli
from filters.xss_filter import is_enabled as xss_enabled, detect_attack as detect_xss

# Initialize Flask app
app = Flask(__name__)

# Base URL of the vulnerable backend app
VULNERABLE_APP_URL = "http://vulnerable_app:5000"

# Proxy route that forwards requests to the backend after filtering
@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    target_url = f"{VULNERABLE_APP_URL}/{path}"  # Construct full target URL

    # --- SQL Injection check on GET parameters ---
    if sqli_enabled() and detect_sqli(request.args):
        return Response("Blocked by SQLi filter", status=403)

    # --- XSS check on GET parameters ---
    if xss_enabled():
        for value in request.args.values():
            if detect_xss(value):
                return Response("Blocked by XSS filter", status=403)

    # --- XSS check on POST form data ---
    if request.method == "POST" and xss_enabled():
        for value in request.form.values():
            if detect_xss(value):
                return Response("Blocked by XSS filter (POST body)", status=403)

    # --- Forward request to the vulnerable backend app ---
    resp = requests.request(
        method=request.method,
        url=target_url,
        params=request.args,
        data=request.form,
        headers={key: value for key, value in request.headers if key.lower() != 'host'},  # Filter out 'Host' header
    )

    # Return the backend response to the client
    return Response(resp.content, resp.status_code)

# Start the proxy server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

