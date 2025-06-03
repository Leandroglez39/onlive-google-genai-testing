"""Application configurations settings"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings
from dotenv import load_dotenv



class Settings(BaseSettings):
    """
    Represents the application settings.

    Attributes:
        APP_ENV (str): The application environment.       
        RABBIT_URI (str): The RabbitMQ URI.
        
    """

    APP_ENV: str = "None"   
    RABBITMQ_URI: str = "None" 
    OPENAI_API_KEY: str = "None"
    LIVEKIT_API_KEY: str = "None"
    LIVEKIT_API_SECRET: str = "None"
    LIVEKIT_URL: str = "None"
    OPENAI_API_KEY: str = "None"
    ELEVEN_API_KEY: str = "None"
    DEFAULT_AGENT_TYPE: str = "None"
    OLLAMA_HOST: str = "None"
    EMBEDDED_MODEL_PROVIDER: str = "None"
    EMBEDDED_DIMENTION: int = 1024
    OLLAMA_EMBEDDING_MODEL: str = "None"
    RABBITMQ_QUEUE_NAME: str = "onlive-ms-rag-provider"
    DEEPGRAM_API_KEY: str = "None"
    AWS_REGION: str = ""
    



    model_config = ConfigDict( 
        env_file = ".env.dev",  # Load environment variables from .env.prod
        extra="ignore",  # Ignore extra fields not defined in the model
          
    )

_ = load_dotenv(dotenv_path=".env.dev", override=True)  # Load environment variables from .env.prod
settings: Settings = Settings()
