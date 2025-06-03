import requests

PROXY_URL = "http://proxy:8000/login"

def test_login(username, password):
    params = {'username': username, 'password': password}
    response = requests.get(PROXY_URL, params=params)
    print(f"[{username} | {password}] → {response.status_code} | {response.text.strip()}")

def main():
    print("Testing normal login:")
    test_login("admin", "adminpass")
    
    print("\nTesting SQL injection:")
    test_login("admin' OR 1=1 --", "anything")

if __name__ == "__main__":
    main()
