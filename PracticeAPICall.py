import requests

# Client id and secret used for authentication
client_id = 'rXGxqKihBJyWiwA01RVirnkrZkXEtmJg'
client_secret = 'Cljv4n0WkEcg6IqF'

# URL to get the access token
token_url = 'https://api.digikey.com/v1/oauth2/token'

# Function to get access token
def get_access_token(client_id, client_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
    }
    data = {
        'client_id': client_id,
        'client_secret': client_secret,
        #Taken from documentation standard entry to be given to parameter
        'grant_type': 'client_credentials'
    }
    #Post command used to make request to authentication server
    response = requests.post(token_url, headers=headers, data=data)
    response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    token_info = response.json()
    return token_info['access_token']

# URL to make the API call taken from documentation (needs to be updated using information from )
api_url = 'https://api.digikey.com/products/v4/search/P5555-ND/productdetails'

# Function to make an API call. 
def make_api_call(api_url, access_token):
    #Headers used for REST APIs allowing addititional information to be sent in GET request
    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-DIGIKEY-Client-Id': client_id,
        'X-DIGIKEY-Locale-Site': 'US',
        'X-DIGIKEY-Locale-Language': 'en',
        'X-DIGIKEY-Locale-Currency': 'USD',
        'X-DIGIKEY-Customer-Id': '0',
    }
    response = requests.get(api_url, headers=headers)
    #HTTP error if the HTTP request returned an unsuccessful status code
    response.raise_for_status()
    return response.json()

# Main function to orchestrate the API call
def main():
    # Calling access token function to get an access token for future operations
    access_token = get_access_token(client_id, client_secret)
    print(f'Access Token: {access_token}')

    # Calling make api call function to retrieve information from api on product information
    api_response = make_api_call(api_url, access_token)
    print('API Response:', api_response)

main()