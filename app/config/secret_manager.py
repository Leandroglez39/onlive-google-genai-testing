from typing import Dict
import boto3
import json
import logging
from botocore.exceptions import ClientError
from botocore.config import Config
from cachetools import cachedmethod, LRUCache
from app.config.settings import settings
from app.config.logging_config import get_logger

# Botocore logging level is configured in logging_config.py

logger = get_logger(__name__)

class LoggingLRUCache(LRUCache):
    def __getitem__(self, key):
        try:
            value = super().__getitem__(key)
            logger.info(f"Cache hit for key: {key}")
            return value
        except KeyError:
            logger.info(f"Cache miss for key: {key}")
            raise
class AWSSecretManager:
    """
    A class to interact with AWS Secrets Manager for retrieving secrets.
    
    Attributes:
        region_name (str): AWS region where the secret is stored.
    """
    
    def __init__(self, assumed_role: bool = False, role_config: Dict[str,str] = None):
        """
        Initializes the AWSSecretsManager client.
        
        Args:
            region_name (str): AWS region name (e.g., 'us-east-1').
            assumed_role (bool): Whether to assume a role for accessing secrets.
            role_config (Dict[str, str]): Configuration for the assumed role, including RoleArn and RoleSessionName.
        """
        self._cache = LoggingLRUCache(maxsize=128)
        self.region_name = settings.AWS_REGION  # Default region, can be overridden
        session = boto3.Session()
        
        if assumed_role and role_config:
            # Assuming a role if specified
            try:
                assumed_role_object = session.client('sts').assume_role(
                    RoleArn=role_config['RoleArn'],
                    RoleSessionName=role_config['RoleSessionName']
                )        
        
        
                config = Config(read_timeout=10,      # Tiempo de espera en segundos (puede ajustarse)
                                    connect_timeout=10,
                                    retries={"max_attempts": 3})
                
                self.client = boto3.client(service_name='secretsmanager',
                                           region_name=self.region_name,                                          
                                            aws_access_key_id=assumed_role_object['Credentials']['AccessKeyId'],
                                            aws_secret_access_key=assumed_role_object['Credentials']['SecretAccessKey'],
                                            aws_session_token=assumed_role_object['Credentials']['SessionToken'],
                                            config=config)
            except ClientError as e:
                logger.error(f"Failed to assume role: {e}")
                raise Exception(f"Error assuming role: {e}") from e
        else:
            # Use default session if not assuming a role
            config = Config(read_timeout=10,      # Tiempo de espera en segundos (puede ajustarse)
                            connect_timeout=10,
                            retries={"max_attempts": 3})
            
                # Create a Secrets Manager client
            self.client = session.client(
                service_name='secretsmanager', 
                region_name=self.region_name,              
                config=config
            )
        
    
        
    @cachedmethod(lambda self: self._cache)
    def get_secret(self, secret_name: str):
        """
        Retrieve a secret from AWS Secrets Manager.
        
        Args:
            secret_name (str): The name or ARN of the secret.
        
        Returns:
            dict or str or bytes: If the secret is a JSON string, it is parsed into a dictionary;
                                    otherwise, it returns the secret as a string or bytes.
                                    
        Raises:
            Exception: Propagates exceptions encountered when retrieving the secret.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            logger.info(f"Successfully retrieved secret: {secret_name}")
        except ClientError as e:
            logger.error(f"Failed to retrieve secret '{secret_name}': {e}")
            raise Exception(f"Error retrieving secret '{secret_name}': {e}") from e
        
        # Process secret based on its format
        if 'SecretString' in response:
            secret = response['SecretString']
            try:
                # Try to parse the secret as JSON if applicable
                return json.loads(secret)
            except json.JSONDecodeError:
                # If not a JSON string, return as is
                return secret
        elif 'SecretBinary' in response:
            return response['SecretBinary']
        else:
            logger.error("The secret does not contain 'SecretString' or 'SecretBinary'.")
            raise Exception("Invalid secret format received from AWS Secrets Manager.")

# Example usage:
if __name__ == "__main__":
    from app.config.settings import settings
 
    secret_name = f"onlive/{settings.APP_ENV}/google_application_credentials"  # Replace with your secret's name or ARN
    
    secret_manager = AWSSecretManager()
    try:
        secret = secret_manager.get_secret(secret_name)       
        # If the secret is a JSON object, you can access its keys as a dictionary.
        logger.info(f"Retrieved secret data: {secret}")
        print(secret)
    except Exception as e:
        logger.error(f"An error occurred: {e}")



