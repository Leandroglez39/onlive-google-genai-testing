"""
Google Gemini AI Service

Production-ready service for interacting with Google's Gemini AI model.
Provides both single request and chat conversation capabilities.
"""

import logging
from typing import Any, Dict, List, Optional, Union
from contextlib import contextmanager

from google.genai import types, Client
from google.oauth2 import service_account

from app.config.settings import settings
from app.utils.secrets import get_secret_and_set_env_var
from app.config.logging_config import get_logger

logger = get_logger(__name__)


class GoogleGeminiService:
    """
    Service class for Google Gemini AI interactions.
    
    Handles authentication, client management, and provides methods for
    both single requests and chat conversations with proper error handling.
    """
    
    def __init__(self, model_name: str = "gemini-2.0-flash-001"):
        """
        Initialize the Google Gemini service.
        
        Args:
            model_name: The name of the Gemini model to use
        """
        self.model_name = model_name
        self._client: Optional[Client] = None
        self._setup_authentication()
    
    def _setup_authentication(self) -> None:
        """Set up Google Cloud authentication using secret manager."""
        try:
            secret_name = f"onlive/{settings.APP_ENV}/google_application_credentials"
            get_secret_and_set_env_var(secret_name)
            logger.info("Google Cloud authentication configured successfully")
        except Exception as e:
            logger.error(f"Failed to setup Google Cloud authentication: {e}")
            raise
    
    @property
    def client(self) -> Client:
        """
        Lazy initialization of the Google GenAI client.
        
        Returns:
            Initialized Google GenAI client
        """
        if self._client is None:
            try:
                self._client = Client(vertexai=True)
                logger.info("Google GenAI client initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Google GenAI client: {e}")
                raise
        return self._client
    
    @staticmethod
    def get_current_weather(location: str) -> str:
        """
        Mock weather function for demonstration purposes.
        
        Args:
            location: The city and state, e.g. San Francisco, CA
            
        Returns:
            Mock weather status
        """
        logger.debug(f"Weather requested for location: {location}")
        # In production, this would call a real weather API
        return "sunny"
    
    def generate_content(
        self, 
        contents: str, 
        tools: Optional[List[Any]] = None,
        **kwargs
    ) -> types.GenerateContentResponse:
        """
        Generate content using the Gemini model.
        
        Args:
            contents: The input text/prompt
            tools: Optional list of tools/functions to make available
            **kwargs: Additional configuration parameters
            
        Returns:
            Response from the Gemini model
            
        Raises:
            Exception: If content generation fails
        """
        try:
            config_params = {}
            if tools:
                config_params['tools'] = tools
            config_params.update(kwargs)
            
            config = types.GenerateContentConfig(**config_params) if config_params else None
            
            logger.info(f"Generating content with model: {self.model_name}")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=config,
            )
            
            logger.info("Content generated successfully")
            return response
            
        except Exception as e:
            logger.error(f"Failed to generate content: {e}")
            raise
    
    @contextmanager
    def create_chat(self, tools: Optional[List[Any]] = None, **kwargs):
        """
        Context manager for chat conversations.
        
        Args:
            tools: Optional list of tools/functions to make available
            **kwargs: Additional configuration parameters
            
        Yields:
            Chat session object
        """
        chat = None
        try:
            config_params = {}
            if tools:
                config_params['tools'] = tools
            config_params.update(kwargs)
            
            config = types.GenerateContentConfig(**config_params) if config_params else None
            
            logger.info(f"Creating chat session with model: {self.model_name}")
            chat = self.client.chats.create(
                model=self.model_name,
                config=config
            )
            
            yield chat
            
        except Exception as e:
            logger.error(f"Chat session error: {e}")
            raise
        finally:
            if chat:
                logger.info("Chat session completed")


def main():
    """
    Main function to demonstrate the Google Gemini service.
    This function shows both single content generation and chat functionality.
    """
    try:
        # Initialize the service
        gemini_service = GoogleGeminiService()
        
        # Example 1: Single content generation
        logger.info("Starting single content generation example")
        response = gemini_service.generate_content(
            contents="What is the weather like in Boston?",
            tools=[gemini_service.get_current_weather]
        )
        
        print("=" * 50)
        print("SINGLE REQUEST RESPONSE:")
        print("=" * 50)
        print(f"Response text: {response.text}")
        print("\nFull response details:")
        import pprint
        pprint.pprint(response.model_dump(exclude_none=True), indent=2, compact=False, sort_dicts=False)
        
        # Example 2: Chat conversation
        logger.info("Starting chat conversation example")
        with gemini_service.create_chat(tools=[gemini_service.get_current_weather]) as chat:
            response = chat.send_message("What is the weather like in Boston?")
            
            print("\n" + "=" * 50)
            print("CHAT RESPONSE:")
            print("=" * 50)
            print(f"Response text: {response.text}")
            print("\nFull response details:")
            pprint.pprint(response.model_dump(exclude_none=True), indent=2, compact=False, sort_dicts=False)
            
            print("\n" + "=" * 50)
            print("CHAT HISTORY:")
            print("=" * 50)
            history = chat.get_history()
            for i, entry in enumerate(history, 1):
                print(f"Entry {i}: {entry.model_dump(exclude_none=True)}")
        
        logger.info("Demo completed successfully")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        raise


if __name__ == "__main__":
    main()