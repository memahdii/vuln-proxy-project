import requests  # Imports the 'requests' library to make HTTP requests

# The endpoint for posting and getting comments
URL = "http://proxy:8000/comment"

# Function to submit a comment and print whether it's accepted or blocked
def test_comment(text):
    response = requests.post(URL, data={"text": text})  # Sends a POST request with the comment text
    status = response.status_code  # Gets the HTTP response status code
    print(f"[{text}] → {status} | {'Accepted' if status == 200 else 'Blocked'}")  # Prints result
    return status == 200  # Returns True if the comment was accepted

# Function to check if an XSS payload is reflected in the server response
def verify_xss(payload):
    response = requests.get(URL)  # Sends a GET request to retrieve comments
    if payload in response.text:  # Checks if the payload is present in the response
        print(f"XSS test failed: Payload reflected in response!")  # XSS vulnerability detected
    else:
        print(f"XSS test passed: Payload filtered or not reflected.")  # No XSS vulnerability

# Main function to run normal and XSS comment tests
def main():
    print("Testing normal comment:")
    normal_comment = "Hello, this is a normal comment."
    test_comment(normal_comment)  # Test a safe comment

    print("\nTesting XSS injection:")
    xss_payload = "<script>alert('XSS')</script>"  # Simulated XSS attack
    if test_comment(xss_payload):  # If the XSS payload was accepted
        verify_xss(xss_payload)  # Check if it's reflected (vulnerable)
    else:
        print("XSS payload blocked on submission.")  # Blocked at input level

# Entry point of the script
if __name__ == "__main__":
    main()

