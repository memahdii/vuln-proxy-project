import requests

URL = "http://proxy:8000/comment"

def test_comment(text):
    response = requests.post(URL, data={"text": text})
    status = response.status_code
    print(f"[{text}] → {status} | {'Accepted' if status == 200 else 'Blocked'}")
    return status == 200

def verify_xss(payload):
    response = requests.get(URL)
    if payload in response.text:
        print(f"💥 XSS test failed: Payload reflected in response!")
    else:
        print(f"✅ XSS test passed: Payload filtered or not reflected.")

def main():
    print("🧪 Testing normal comment:")
    normal_comment = "Hello, this is a normal comment."
    test_comment(normal_comment)

    print("\n🧪 Testing XSS injection:")
    xss_payload = "<script>alert('XSS')</script>"
    if test_comment(xss_payload):
        verify_xss(xss_payload)
    else:
        print("❌ XSS payload blocked on submission.")

if __name__ == "__main__":
    main()
