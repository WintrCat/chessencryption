import requests

def upgrade_to_bot_account(api_token: str):
    # Define the API endpoint for upgrading the account
    url = "https://lichess.org/api/bot/account/upgrade"

    # Set the headers, including the authorization token
    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    # Make a POST request to the Lichess API to upgrade the account
    response = requests.post(url, headers=headers)

    # Check the response status
    if response.status_code == 200:
        print("The bot account was successfully upgraded.")
    elif response.status_code == 400:
        print("The upgrade of the bot account failed. Account might have already played games.")
    else:
        print(f"Failed to upgrade account. Status code: {response.status_code}, Response: {response.text}")

# Example usage
api_token = "lip_kQvkVcLnW78Np9Fuz3xF"  # Replace this with your actual API token
upgrade_to_bot_account(api_token)
