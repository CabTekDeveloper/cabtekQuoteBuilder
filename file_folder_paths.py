

# Save all the paths in one file and import wherever required
QUOTING_DB_NAME = "quoting_db.db"

# Folder paths
FOLDER_PATH_QUOTE_BUILDER_DB = "\\\\MANAGER1\\SharedDatabase\\CabTek Quote Builder Database"
FOLDER_PATH_QUOTE_BUILDER_DB_BACKUP = f"{FOLDER_PATH_QUOTE_BUILDER_DB}\\Backup"

# Database paths
LIVE_QUOTING_DB_PATH = f"{FOLDER_PATH_QUOTE_BUILDER_DB}\\{QUOTING_DB_NAME}"           # For Deployment
TEST_QUOTING_DB_PATH = f"static\\test_db\\{QUOTING_DB_NAME}"           # For Deployment


