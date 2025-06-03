import os
import json
from app.config.logging_config import get_logger
from app.config.secret_manager import AWSSecretManager
from app.config.settings import settings
logger = get_logger(__name__)

def get_secret_and_set_env_var(secret_name: str, env_var_name: str = "GOOGLE_APPLICATION_CREDENTIALS"):
    """
    Fetches a secret from AWS Secrets Manager and sets it as an environment variable.

    Args:
        secret_name (str): The name of the secret in AWS Secrets Manager.
        env_var_name (str): The name of the environment variable to set.
    """
    

    secret_manager = AWSSecretManager()
    try:
        secret = secret_manager.get_secret(secret_name)
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        
    # Save the json to a file
    with open("app/config/service-account.json", "w") as f:
        json.dump(secret, f)

    os.environ[env_var_name] = "app/config/service-account.json"
    
    #CHECK IF THE ENV VAR IS SET
    if os.getenv(env_var_name):
        logger.info(f"Environment variable '{env_var_name}' set successfully.")
    else:
        logger.error(f"Failed to set environment variable '{env_var_name}'.")


if __name__ == "__main__":
    get_secret_and_set_env_var()