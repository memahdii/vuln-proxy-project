import os
import requests
from flask import Flask, request, Response
from filters import filter_manager

app = Flask(__name__)

VULNERABLE_APP_URL = "http://vulnerable_app:5000"


@app.route('/<path:path>', methods=["GET", "POST"])
def proxy(path):
    target_url = f"{VULNERABLE_APP_URL}/{path}"

    # --- Dynamic Filter Check ---
    # Prepare request data for filters
    request_data = {
        'args': request.args,
        'form': request.form,
        'method': request.method,
        'path': path
    }
    
    # Check all discovered filters
    if filter_manager.check_all_filters(request_data):
        return Response("Blocked by security filter", status=403)

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
