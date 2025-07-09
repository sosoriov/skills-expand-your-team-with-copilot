"""
Database configuration and setup for Mergington High School API
"""

try:
    from pymongo import MongoClient
    from argon2 import PasswordHasher

    # Try to connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=1000)
    client.server_info()  # This will raise an exception if MongoDB is not available
    db = client['mergington_high']
    activities_collection = db['activities']
    teachers_collection = db['teachers']
    print("Connected to MongoDB")
    
    # Methods
    def hash_password(password):
        """Hash password using Argon2"""
        ph = PasswordHasher()
        return ph.hash(password)

    def init_database():
        """Initialize database if empty"""
        # This would be implemented for real MongoDB
        pass
        
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    print("Using in-memory mock database for development")
    from .mock_database import activities_collection, teachers_collection, hash_password, init_database
