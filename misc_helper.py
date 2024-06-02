import os
import dotenv

def load_firebase_credentials(env_file):
    # Load the environment variables from the .env file
    dotenv.load_dotenv(dotenv_path=env_file)
    # Recreate the Firebase credentials from the environment variables
    credentials = {}
    credentials['type'] = os.getenv('fc_type')[1:-1]
    credentials['project_id'] = os.getenv('fc_project_id')[1:-1]
    credentials['private_key_id'] = os.getenv('fc_private_key_id')[1:-1]
    credentials['private_key'] = os.getenv('fc_private_key').replace('\\n', '\n')[1:-1]
    credentials['client_email'] = os.getenv('fc_client_email')[1:-1]
    credentials['client_id'] = os.getenv('fc_client_id')[1:-1]
    credentials['auth_uri'] = os.getenv('fc_auth_uri')[1:-1]
    credentials['token_uri'] = os.getenv('fc_token_uri')[1:-1]
    credentials['auth_provider_x509_cert_url'] = os.getenv('fc_auth_provider_x509_cert_url')[1:-1]
    credentials['client_x509_cert_url'] = os.getenv('fc_client_x509_cert_url')[1:-1]
    credentials['universe_domain'] = os.getenv('fc_universe_domain')[1:-1]
    return credentials

def parse_datetime(string):
  # Split the string by delimiters
  parts = string.split("T")
  date = parts[0]
  time = parts[1].split(".")[0]  # Get only time part before milliseconds

  # Combine date and time with separator
  return f"{date} {time}"