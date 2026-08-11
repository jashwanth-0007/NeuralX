import os

from dotenv import load_dotenv
from pymongo import MongoClient


# =========================================================
# LOAD .ENV
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


ENV_FILE = os.path.join(
    BASE_DIR,
    ".env"
)


load_dotenv(
    ENV_FILE,
    override=True
)


# =========================================================
# MONGODB CONNECTION STRING
# =========================================================

MONGO_URI = os.environ.get(
    "MONGO_URI"
)


if not MONGO_URI:

    raise ValueError(
        "MONGO_URI is not set. "
        "Check the .env file."
    )


# =========================================================
# MONGODB CLIENT
# =========================================================

client = MongoClient(

    MONGO_URI,

    serverSelectionTimeoutMS=10000

)


# =========================================================
# DATABASE
# =========================================================

db = client["NeuralX"]


# =========================================================
# COLLECTIONS
# =========================================================

teams_collection = db["Teams"]

members_collection = db["team members"]