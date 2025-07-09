# Mergington High School Activities

A comprehensive web application that allows students to view and sign up for extracurricular activities, with full teacher management capabilities.

## Features

### For Students
- View all available extracurricular activities with detailed information
- Search and filter activities by name and description
- Filter activities by category (Sports, Arts, Academic, Community, Technology)
- Filter activities by day of the week (including weekend activities)
- See real-time enrollment numbers and capacity indicators
- View detailed schedules with day and time information
- Browse weekend activities (Saturday and Sunday options available)

### For Teachers  
- Secure teacher login and session management
- Register students for activities with email verification
- Remove students from activities with confirmation dialogs
- View real-time participant lists for each activity
- Manage activity enrollments with capacity awareness
- Access to all activities regardless of day or time restrictions

### For School Administrators
- Easy activity management through structured issue requests
- Automated change processing via Copilot coding agent
- Comprehensive issue templates for common tasks

## Making Changes and Requests

Teachers and staff can easily request changes to the system using our **issue template forms**. No coding knowledge required!

### 📋 Available Request Types

- **🏫 Add New Activity** - Request new extracurricular activities
- **✏️ Modify Activity** - Change existing activity details
- **🎨 UI Enhancement** - Improve visual design and user experience  
- **🚀 New Feature** - Request new functionality
- **🐛 Bug Report** - Report issues or problems
- **📚 Documentation** - Update help text and instructions
- **❓ Other Requests** - For anything else

### 🚀 Quick Start for Teachers

1. Go to the [Issues page](../../issues/new/choose)
2. Select the appropriate template for your request
3. Fill out the form completely
4. Submit the issue
5. A Copilot coding agent will automatically handle your request!

**Expected response times:** Most requests are handled within hours during business hours.

## Current Activities

The system currently supports these activities:

### Weekday Activities
- **Chess Club** - Mondays and Fridays, 3:15 PM - 4:45 PM
- **Programming Class** - Tuesdays and Thursdays, 7:00 AM - 8:00 AM  
- **Morning Fitness** - Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM
- **Soccer Team** - Tuesdays and Thursdays, 3:30 PM - 5:30 PM
- **Basketball Team** - Wednesdays and Fridays, 3:15 PM - 5:00 PM
- **Art Club** - Thursdays, 3:15 PM - 5:00 PM
- **Drama Club** - Mondays and Wednesdays, 3:30 PM - 5:30 PM
- **Math Club** - Tuesdays, 7:15 AM - 8:00 AM
- **Debate Team** - Fridays, 3:30 PM - 5:30 PM
- **Manga Maniacs** - Tuesdays, 7:00 PM - 8:30 PM

### Weekend Activities
- **Weekend Robotics Workshop** - Saturdays, 10:00 AM - 2:00 PM
- **Science Olympiad** - Saturdays, 1:00 PM - 4:00 PM  
- **Sunday Chess Tournament** - Sundays, 2:00 PM - 5:00 PM

## Technical Features

- **Backend:** FastAPI with Python providing RESTful API endpoints
- **Database:** MongoDB with in-memory fallback for development
- **Frontend:** Vanilla JavaScript with responsive CSS and modern UI components
- **Authentication:** Secure teacher login with session validation
- **API Features:** 
  - Activity filtering by day and time
  - Real-time participant management
  - Teacher-verified student registration/unregistration
  - Comprehensive activity search and categorization
- **UI Enhancements:**
  - Interactive search and filter system
  - Activity capacity indicators with visual progress bars
  - Category-based filtering (Sports, Arts, Academic, Community, Technology)
  - Day-based filtering including weekend support
  - Responsive design for desktop and mobile devices

## Development Guide

For detailed setup and development instructions, please refer to our [Development Guide](../docs/how-to-develop.md).
