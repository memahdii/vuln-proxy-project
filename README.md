# Vulnerable Proxy Project

A demonstration project showcasing SQL injection and XSS vulnerabilities and their mitigation through a proxy server. This project consists of three main components:

1. A vulnerable Flask application with SQL injection and XSS vulnerabilities
2. A proxy server that can filter SQL injection and XSS attempts
3. An attacker script that demonstrates both normal and malicious requests

## Project Structure

```
.
├── docker-compose.yml
├── vulnerable_app/
│   ├── Dockerfile
│   └── app.py
├── proxy/
│   ├── Dockerfile
│   └── proxy.py
└── attacker/
    ├── Dockerfile
    ├── sqli_attack.py
    └── xss_attack.py
```

## Components

### Vulnerable Application
- Runs on port 5000
- Simple Flask application with SQLite database
- Contains a vulnerable login endpoint that is susceptible to SQL injection
- Contains a vulnerable comment system that is susceptible to XSS
- Uses string concatenation for SQL queries (intentionally vulnerable)
- Displays user comments without proper sanitization (intentionally vulnerable)

### Proxy Server
- Runs on port 8000
- Acts as a reverse proxy to the vulnerable application
- Implements SQL injection and XSS filtering
- Can be configured to enable/disable filtering for each vulnerability type

### Attacker Script
- Demonstrates both normal and malicious login attempts
- Tests the proxy's SQL injection filtering capabilities
- Tests the proxy's XSS filtering capabilities

## Building and Running

1. Clone the repository:
```bash
git clone https://github.com/memahdii/vuln-proxy-project.git
cd vuln-proxy-project
```

2. Build and run the containers:
```bash
docker-compose up --build
```

## Vulnerabilities and Mitigation

### SQL Injection Vulnerability
The vulnerable application uses string concatenation to build SQL queries:
```python
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
```

This allows SQL injection attacks like:
```
username=admin' OR 1=1 --&password=anything
```

### XSS Vulnerability
The vulnerable application has a comment system that stores and displays user input without proper sanitization:
```python
@app.route("/comment", methods=["GET", "POST"])
def comment():
    if request.method == "POST":
        text = request.form.get("text", "")
        comments.append(text)
    return "<h1>Comments</h1>" + "<br>".join(comments)
```

This allows XSS attacks like:
```html
<script>alert('XSS')</script>
```

### Mitigation
The proxy server implements filtering for both vulnerabilities:

#### SQL Injection Filter
Checks for common SQL injection patterns:
- OR/AND conditions
- Comment markers (--)
- UNION statements
- Common tautologies (1=1)

#### XSS Filter
Checks for common XSS patterns:
- `<script>` tags
- Event handlers (onload, onerror, etc.)
- JavaScript protocol handlers
- Malicious HTML attributes

## Configuration

Both filters can be enabled/disabled using environment variables in `docker-compose.yml`:

```yaml
proxy:
  environment:
    - ENABLE_SQLI_FILTER=1  # 1 to enable, 0 to disable
    - ENABLE_XSS_FILTER=1   # 1 to enable, 0 to disable
```

## Expected Output

When running the project, you should see:

1. Normal login attempt:
```
🔒 Testing normal login:
[admin | adminpass] → 200 | Login successful
```

2. SQL injection attempt:
```
💥 Testing SQL injection:
[admin' OR 1=1 -- | anything] → 403 | Blocked by SQLi filter
```

3. Normal comment:
```
🧪 Testing normal comment:
[Hello, this is a normal comment.] → 200 | Accepted
```

4. XSS attempt:
```
🧪 Testing XSS injection:
[<script>alert('XSS')</script>] → 403 | Blocked by XSS filter
```

## Security Note

This project is intentionally vulnerable and should only be used for educational purposes. Do not deploy it in production environments.
