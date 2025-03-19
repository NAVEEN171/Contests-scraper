# db_connection.py
import pymongo
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_connection():
    """
    Creates and returns a connection to the MongoDB database.
    Uses environment variables for credentials.
    """
    try:
        # Get credentials from environment variables for security
        db_mongo_url = os.environ.get("MONGODB_URL")
        
        # If environment variables aren't found, raise error
        if not db_mongo_url :
            raise ValueError("Database credentials not found in environment variables")
        
        # Format the connection string
        connection_string = db_mongo_url
        
        # Create a connection using MongoClient
        client = MongoClient(connection_string)
        
        # Test the connection
        client.admin.command('ping')
        print("Successfully connected to MongoDB!")
        
        # Get the database
        db = client.get_database()
        return db
    
    except pymongo.errors.ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise

# Connection singleton
_db_connection = None

def get_db():
    """
    Returns a singleton database connection.
    """
    global _db_connection
    if _db_connection is None:
        _db_connection = get_database_connection()
    return _db_connection


    