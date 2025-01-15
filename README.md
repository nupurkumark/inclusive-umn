# Inclusive UMN Dashboard

The Inclusive UMN Dashboard is a prototype web application designed to catalog and display physical accessibility barriers across the University of Minnesota (UMN) campus. The goal is to create a user-friendly, accessible platform for the UMN community to identify and report accessibility issues in campus facilities.

## Features
- **Interactive Dashboard**: Displays a table of accessibility barriers with filters based on building selection
- **Building Search**: Search for barriers by building via dropdown
- **Add New Issues**: Users can submit new accessibility barriers, specifying the building, type of issue, and description.
- **Database Integration**: Uses SQLite for data storage and retrieval, pre-populated with data from a CSV file

## Technologies Used
- **Python**: Core programming language
- **Dash**: Creating the interactive dashboard
- **SQLite**: Database creation
- **Pandas**: Data manipulation and CSV parsing 
- **HTML/CSS**: Styling UI

## Installation

### Prerequisites
- Python 3.7 or higher
- Python dependencies: Pandas, Dash, and SQLite
    ```bash
    pip install dash pandas sqlite3
    ```

### Setup Instructions
1. Clone this repository

2. Run the application:
    ```bash
    python app.py
    ```

3. Open the application in your web browser at `http://127.0.0.1:8050`.

## Project Limitations
- The current prototype focuses on physical barriers affecting mobility, visual, and auditory disabilities
- The application is designed to be accessed via a desktop browser and is not fully optimized for mobile devices

---

We hope this dashboard serves as a meaningful step toward improving accessibility on campus!

