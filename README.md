# Vulnerable Proxy Project

## Overview
This project demonstrates a vulnerable web application protected by a **dynamic proxy filter system**. It is designed for security testing and learning about web attacks and defenses.

- **vulnerable_app/**: The intentionally vulnerable web app (Flask)
- **proxy/**: The proxy that filters attacks using **dynamically discovered filters**
- **attacker/**: **Dynamic attack system** that automatically discovers and runs all attack modules

---

## System Architecture

```
[Attacker] → [Proxy] → [Vulnerable App]
   (8000)     (8000)      (5000)
```

The system consists of three main components:

1. A vulnerable Flask application with SQL injection and XSS vulnerabilities
2. A **dynamic proxy server** that automatically discovers and applies security filters
3. A **dynamic attacker system** that automatically discovers and runs all attack modules

---

## Project Structure

```
.
├── docker-compose.yml
├── vulnerable_app/
│   ├── Dockerfile
│   └── app.py
├── proxy/
│   ├── Dockerfile
│   ├── proxy.py
│   └── filters/
│       ├── __init__.py          # Dynamic filter manager
│       ├── sqli_filter.py       # SQL injection filter
│       ├── xss_filter.py        # XSS filter
│       └── template_filter.py   # Template for new filters
└── attacker/
    ├── Dockerfile
    ├── attack_manager.py        # Dynamic attack manager
    └── attacks/
        ├── __init__.py
        ├── sqli_attack.py       # SQL injection attacks
        ├── xss_attack.py        # XSS attacks
        └── template_attack.py   # Template for new attacks
```

---

## How the Dynamic System Works

### **Dynamic Attack Discovery**
- Any Python file in `attacker/attacks/` with a `name` and `run_attack()` function is automatically discovered
- No need to modify main code to add new attacks!
- The `attack_manager.py` scans the directory and runs all valid attack modules

### **Dynamic Filter Discovery**
- Any Python file in `proxy/filters/` with `is_enabled()` and `detect_attack()` functions is automatically discovered
- No need to modify main code to add new filters!
- The `filter_manager` scans the directory and applies all enabled filters

---

## Components

### Vulnerable Application
- Runs on port 5000
- Simple Flask application with SQLite database
- Contains two vulnerable endpoints:
  1. **Login endpoint** (SQL Injection vulnerable):
     ```python
     @app.route("/login")
     def login():
         # Vulnerable because it uses string concatenation
         query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
     ```
  2. **Comment endpoint** (XSS vulnerable):
     ```python
     @app.route("/comment", methods=["GET", "POST"])
     def comment():
         # Vulnerable because it displays user input without sanitization
         return "<h1>Comments</h1>" + "<br>".join(comments)
     ```

### Dynamic Proxy Server
- Runs on port 8000
- Acts as a reverse proxy to the vulnerable application
- **Automatically discovers and applies all filters** in the `filters/` directory
- Each filter can be enabled/disabled independently via environment variables
- Uses a **modular filter system** that requires no code changes to add new filters

### Dynamic Attacker System
- **Automatically discovers and runs all attacks** in the `attacks/` directory
- Each attack module is self-contained and follows a standard interface
- Provides comprehensive testing of both normal and malicious requests
- Requires no code changes to add new attack types

---

## Building and Running

1. Clone the repository:
```bash
git clone https://github.com/memahdii/vuln-proxy-project.git
cd vuln-proxy-project
```

2. Build and run the containers:
```bash
docker compose up --build -d
```

3. View attack results:
```bash
docker compose logs attacker
```

---

## How It Works

### Request Flow

1. **Normal Login**:
```
Attacker → Proxy → Vulnerable App
[admin | adminpass] → [Check: No SQLi] → [Execute Query] → [Login Successful]
```

2. **SQL Injection Attempt**:
```
Attacker → Proxy → Blocked
[admin' OR 1=1 -- | anything] → [Check: SQLi Detected] → [403 Forbidden]
```

3. **Normal Comment**:
```
Attacker → Proxy → Vulnerable App
[Hello, this is a normal comment.] → [Check: No XSS] → [Display Comment]
```

4. **XSS Attempt**:
```
Attacker → Proxy → Blocked
[<script>alert('XSS')</script>] → [Check: XSS Detected] → [403 Forbidden]
```

---

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

**Mitigation**: The dynamic SQLi filter uses regex patterns to detect real SQL injection attempts while allowing legitimate usernames like "Igor".

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

**Mitigation**: The dynamic XSS filter detects and blocks malicious HTML/JavaScript patterns.

---

## Configuration

Filters can be enabled/disabled using environment variables in `docker-compose.yml`:

```yaml
proxy:
  environment:
    - ENABLE_SQLI_FILTER=1  # 1 to enable, 0 to disable
    - ENABLE_XSS_FILTER=1   # 1 to enable, 0 to disable
```

---

## How to Add a New Attack

1. **Copy the template:**
   ```bash
   cp attacker/attacks/template_attack.py attacker/attacks/my_new_attack.py
   ```

2. **Edit `my_new_attack.py`:**
   - Change the `name`, `description`, and `category`
   - Implement your test cases in the `test_cases` list
   - Add your attack logic in the `run_attack()` function

3. **Example:**
   ```python
   name = "Command Injection Attack"
   description = "Tests command injection vulnerabilities"
   category = "Injection"

   def run_attack(target_url: str = "http://proxy:8000/command", **kwargs):
       test_cases = [
           {"name": "Basic Command Injection", "payload": "; ls -la"}
       ]
       # ... rest of logic
   ```

4. **Rebuild and run:**
   ```bash
   docker compose build attacker
   docker compose up attacker
   ```

**The attack will be automatically discovered and run!**

---

## How to Add a New Filter

1. **Copy the template:**
   ```bash
   cp proxy/filters/template_filter.py proxy/filters/command_injection_filter.py
   ```

2. **Edit `command_injection_filter.py`:**
   - Change the `is_enabled()` function to use a relevant environment variable
   - Add your detection regex patterns in `detect_attack()`

3. **Example:**
   ```python
   def is_enabled():
       return os.environ.get("ENABLE_COMMAND_INJECTION_FILTER", "1") == "1"

   def detect_attack(request_data):
       patterns = [
           r'[;&|`]',  # Command separators
           r'\b(cat|ls|pwd|whoami|id)\b',  # Common commands
       ]
       # ... detection logic
   ```

4. **Rebuild and run:**
   ```bash
   docker compose build proxy
   docker compose up proxy
   ```

**The filter will be automatically discovered and applied!**

---

## Usage

### Start the System
```bash
docker compose up --build -d
```

### Run All Attacks
```bash
docker compose logs attacker
```

### Change Filter Settings
Edit the environment variables in `docker-compose.yml` for the proxy service:
```yaml
environment:
  - ENABLE_SQLI_FILTER=0  # Disable SQLi filter
  - ENABLE_XSS_FILTER=1   # Enable XSS filter
```

Then restart:
```bash
docker compose down
docker compose up -d
```

### Test Specific Scenarios
```bash
# Test normal login (should work)
curl "http://localhost:8000/login?username=igor&password=igorpass"

# Test SQLi attack (should be blocked if filter enabled)
curl "http://localhost:8000/login?username=admin'%20OR%20'1'='1&password=anything"
```

---

## Expected Output

When running the project, you should see:

1. **Attack discovery:**
   ```
   ✓ Discovered attack: SQL Injection Attack
   ✓ Discovered attack: Cross-Site Scripting Attack
   Found 2 attacks: sqli_attack, xss_attack
   ```

2. **Filter discovery:**
   ```
   ✓ Discovered filter: sqli_filter
   ✓ Discovered filter: xss_filter
   ```

3. **Attack results:**
   ```
   Normal Login: ALLOWED (200)
   SQLi Attack: BLOCKED (403)
   Normal Comment: ALLOWED (200)
   XSS Attack: BLOCKED (403)
   ```

---

## Key Benefits of the Dynamic System

✅ **No false positives**: Legitimate usernames like "Igor" are allowed  
✅ **Easy extensibility**: Add new attacks/filters by just adding files  
✅ **Zero code changes**: No need to modify main application code  
✅ **Runtime configuration**: Enable/disable filters via environment variables  
✅ **Automatic discovery**: New components are found and used automatically  
✅ **Standardized interfaces**: All attacks/filters follow the same pattern  

---

## Security Note

- This project is for educational purposes only
- The vulnerable app is intentionally insecure
- Do not deploy in production environments
- Use only in controlled testing environments

---

## Credits

- Inspired by real-world web security testing scenarios
- Dynamic discovery pattern for extensibility
- Demonstrates modern software architecture principles
