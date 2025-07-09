"""
In-memory database mock for development when MongoDB is not available
"""

from argon2 import PasswordHasher
import copy

# In-memory data storage
activities_data = {}
teachers_data = {}

class MockCollection:
    def __init__(self, data_store):
        self.data = data_store
    
    def count_documents(self, query):
        if not query:
            return len(self.data)
        # Simple implementation for empty query
        return len(self.data)
    
    def insert_one(self, document):
        doc_id = document.get('_id')
        if doc_id:
            self.data[doc_id] = {k: v for k, v in document.items() if k != '_id'}
        return type('Result', (), {'inserted_id': doc_id})()
    
    def find_one(self, query):
        if '_id' in query:
            doc_id = query['_id']
            if doc_id in self.data:
                result = copy.deepcopy(self.data[doc_id])
                result['_id'] = doc_id
                return result
        return None
    
    def find(self, query=None):
        if query is None:
            query = {}
        
        results = []
        for doc_id, doc_data in self.data.items():
            # Simple query matching
            match = True
            
            # Handle day filtering
            if "schedule_details.days" in query:
                day_filter = query["schedule_details.days"]
                if "$in" in day_filter:
                    target_day = day_filter["$in"][0]
                    if "schedule_details" not in doc_data or "days" not in doc_data["schedule_details"]:
                        match = False
                    elif target_day not in doc_data["schedule_details"]["days"]:
                        match = False
            
            # Handle time filtering
            if "schedule_details.start_time" in query:
                time_filter = query["schedule_details.start_time"]
                if "$gte" in time_filter:
                    target_time = time_filter["$gte"]
                    if "schedule_details" not in doc_data or "start_time" not in doc_data["schedule_details"]:
                        match = False
                    elif doc_data["schedule_details"]["start_time"] < target_time:
                        match = False
            
            if "schedule_details.end_time" in query:
                time_filter = query["schedule_details.end_time"]
                if "$lte" in time_filter:
                    target_time = time_filter["$lte"]
                    if "schedule_details" not in doc_data or "end_time" not in doc_data["schedule_details"]:
                        match = False
                    elif doc_data["schedule_details"]["end_time"] > target_time:
                        match = False
            
            # Handle difficulty filtering
            if "difficulty" in query:
                difficulty_filter = query["difficulty"]
                if difficulty_filter is None:
                    # Looking for activities without difficulty
                    if "difficulty" in doc_data:
                        match = False
                else:
                    # Looking for specific difficulty
                    if "difficulty" not in doc_data or doc_data["difficulty"] != difficulty_filter:
                        match = False
            
            if match:
                result = copy.deepcopy(doc_data)
                result['_id'] = doc_id
                results.append(result)
        
        return results
    
    def update_one(self, query, update):
        if '_id' in query:
            doc_id = query['_id']
            if doc_id in self.data:
                if '$push' in update:
                    for field, value in update['$push'].items():
                        if field not in self.data[doc_id]:
                            self.data[doc_id][field] = []
                        self.data[doc_id][field].append(value)
                elif '$pull' in update:
                    for field, value in update['$pull'].items():
                        if field in self.data[doc_id] and isinstance(self.data[doc_id][field], list):
                            self.data[doc_id][field] = [x for x in self.data[doc_id][field] if x != value]
                return type('Result', (), {'modified_count': 1})()
        return type('Result', (), {'modified_count': 0})()
    
    def aggregate(self, pipeline):
        # Simple implementation for getting unique days
        if len(pipeline) >= 2 and "$unwind" in pipeline[0] and "$group" in pipeline[1]:
            days = set()
            for doc_data in self.data.values():
                if "schedule_details" in doc_data and "days" in doc_data["schedule_details"]:
                    for day in doc_data["schedule_details"]["days"]:
                        days.add(day)
            return [{"_id": day} for day in sorted(days)]
        return []

# Create mock collections
activities_collection = MockCollection(activities_data)
teachers_collection = MockCollection(teachers_data)

# Methods
def hash_password(password):
    """Hash password using Argon2"""
    ph = PasswordHasher()
    return ph.hash(password)

def init_database():
    """Initialize database if empty"""
    
    # Initialize activities if empty
    if activities_collection.count_documents({}) == 0:
        for name, details in initial_activities.items():
            activities_collection.insert_one({"_id": name, **details})
            
    # Initialize teacher accounts if empty
    if teachers_collection.count_documents({}) == 0:
        for teacher in initial_teachers:
            teachers_collection.insert_one({"_id": teacher["username"], **teacher})

# Initial database data
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
        "difficulty": "Beginner"
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"],
        "difficulty": "Intermediate"
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"],
        "difficulty": "Advanced"
    },
    "Manga Maniacs": {
        "description": "Explore the fantastic stories of the most interesting characters from Japanese Manga (graphic novels).",
        "schedule": "Tuesdays, 7:00 PM - 8:30 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:30"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "email": "mrodriguez@mergington.edu"
    },
    {
        "username": "jchen",
        "display_name": "Mr. Chen",
        "password": hash_password("science456"),
        "email": "jchen@mergington.edu"
    },
    {
        "username": "sthompson",
        "display_name": "Coach Thompson",
        "password": hash_password("sports789"),
        "email": "sthompson@mergington.edu"
    }
]