## The script will:

Process all FIT files in the activitiesTest folder
Store HRV data in the astremis_hrv.db database
Create analysis views
Provide HRV trend analysis

## Key features:

FIT file parsing
Data storage in SQLite database
Daily HRV summaries
Trend analysis
Recovery score calculation
Comprehensive logging


### Key changes from the previous version:

Replaced SQLAlchemy with direct SQLite3 queries
Simplified database connection handling
Hardcoded SQL queries
Direct table creation and management
Simplified error handling
Maintained all functionality but with pure SQLite implementation

## The script will still:

Process all FIT files in the activitiesTest folder
Store HRV data in the astremis_hrv.db database
Create analysis views
Provide HRV trend analysis