import mlflow
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def setup_mlflow():
    MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI")
    MLFLOW_TRACKING_USERNAME = os.getenv("MLFLOW_USERNAME")
    MLFLOW_TRACKING_TOKEN = os.getenv("MLFLOW_TOKEN")

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    os.environ["MLFLOW_TRACKING_USERNAME"] = MLFLOW_TRACKING_USERNAME
    os.environ["MLFLOW_TRACKING_PASSWORD"] = MLFLOW_TRACKING_TOKEN
