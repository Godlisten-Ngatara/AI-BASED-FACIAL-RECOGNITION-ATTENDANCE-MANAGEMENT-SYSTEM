import requests
def send_api_request(target, payload, headers):
    try:
        response = requests.post(target, headers=headers, json=payload, verify=False)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        # print(f"API Response: {response.json()}")  # Debugging
        return response.json()  # Return parsed JSON response
    except requests.exceptions.RequestException as e:
        print(f"API Request failed: {e}")
        return ({"error": "API request failed", "details": str(e)})