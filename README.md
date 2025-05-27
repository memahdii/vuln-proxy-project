<<<<<<< HEAD
# vuln-proxy-project
=======
# Vulnerable Proxy Project

A demonstration project showcasing SQL injection vulnerabilities and their mitigation through a proxy server. This project consists of three main components:

1. A vulnerable Flask application with SQL injection vulnerabilities
2. A proxy server that can filter SQL injection attempts
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
    └── sqli_attack.py
```

## Components

### Vulnerable Application
- Runs on port 5000
- Simple Flask application with SQLite database
- Contains a vulnerable login endpoint that is susceptible to SQL injection
- Uses string concatenation for SQL queries (intentionally vulnerable)

### Proxy Server
- Runs on port 8000
- Acts as a reverse proxy to the vulnerable application
- Implements SQL injection filtering
- Can be configured to enable/disable filtering

### Attacker Script
- Demonstrates both normal and malicious login attempts
- Tests the proxy's SQL injection filtering capabilities

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

### Mitigation
The proxy server implements basic SQL injection filtering by checking for common SQL injection patterns:
- OR/AND conditions
- Comment markers (--)
- UNION statements
- Common tautologies (1=1)

## Configuration

### SQL Injection Filter
The proxy's SQL injection filter can be enabled/disabled using the `ENABLE_SQLI_FILTER` environment variable in `docker-compose.yml`:

```yaml
proxy:
  environment:
    - ENABLE_SQLI_FILTER=1  # 1 to enable, 0 to disable
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

## Security Note

This project is intentionally vulnerable and should only be used for educational purposes. Do not deploy it in production environments.

## License

MIT License
>>>>>>> e89cff6 (Initial commit: Add vulnerable proxy project with documentation)
