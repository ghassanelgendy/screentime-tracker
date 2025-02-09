# # model/category_manager.py
# import sqlite3
# from typing import Dict, List, Optional, Tuple

# class CategoryManager:
#     def __init__(self, data_manager):
#         """
#         Initialize the category manager with a reference to the data manager.
        
#         Args:
#             data_manager: Instance of DataManager for database operations
#         """
#         self.data_manager = data_manager
#         self._init_default_categories()
#         self._load_categories_cache()
#         self._init_app_category_mappings()  # Initialize app-category mappings

#     def _init_default_categories(self):
#         """Initialize default categories if they don't exist."""
#         default_categories = [
#             ('Social Media', None),
#             ('Web Browsers', None),
#             ('Creative Tools', None),
#             ('Productivity', None),
#             ('Development Tools', None),
#             ('Communication', None),
#             ('Entertainment', None),
#             ('Gaming', None),
#             ('Utilities', None),
#             ('E-commerce', None),
#             ('Education', None),
#             ('Finance', None),
#             ('Health & Fitness', None),
#             ('News & Media', None),
#             ('Photography', None)
#         ]
        
#         with self.data_manager._get_connection() as conn:
#             # Create categories table if it doesn't exist
#             conn.execute('''CREATE TABLE IF NOT EXISTS categories (
#                 category_id INTEGER PRIMARY KEY,
#                 category_name TEXT UNIQUE NOT NULL,
#                 daily_limit INTEGER
#             )''')
            
#             # Insert default categories
#             conn.executemany('''INSERT OR IGNORE INTO categories 
#                              (category_name, daily_limit) VALUES (?, ?)''',
#                           default_categories)
#             conn.commit()

#     def _load_categories_cache(self):
#         """Load categories from database into memory."""
#         with self.data_manager._get_connection() as conn:
#             cursor = conn.execute('SELECT category_name, category_id FROM categories')
#             self.categories_cache = {row[0]: row[1] for row in cursor.fetchall()}

#     def _init_app_category_mappings(self):
#         """Initialize the database with 100 app-category mappings."""
#         app_category_mappings = {
#             # Social Media
#             'Faceboollk': 'Social Media',
#             'Instagram': 'Social Media',
#             'Twitter': 'Social Media',
#             'LinkedIn': 'Social Media',
#             'Snapchat': 'Social Media',
#             'TikTok': 'Social Media',
#             'Pinterest': 'Social Media',
#             'Reddit': 'Social Media',
#             'WhatsApp': 'Social Media',
#             'Telegram': 'Social Media',

#             # Web Browsers
#             'Google Chrome': 'Web Browsers',
#             'Microsoft Edge': 'Web Browsers',
#             'Mozilla Firefox': 'Web Browsers',
#             'Safari': 'Web Browsers',
#             'Opera': 'Web Browsers',
#             'Brave': 'Web Browsers',
#             'Tor Browser': 'Web Browsers',
#             'Vivaldi': 'Web Browsers',
#             'DuckDuckGo': 'Web Browsers',
#             'UC Browser': 'Web Browsers',

#             # Creative Tools
#             'Adobe Photoshop': 'Creative Tools',
#             'Adobe Illustrator': 'Creative Tools',
#             'Adobe Premiere Pro': 'Creative Tools',
#             'Adobe After Effects': 'Creative Tools',
#             'Blender': 'Creative Tools',
#             'Autodesk Maya': 'Creative Tools',
#             'Cinema 4D': 'Creative Tools',
#             'DaVinci Resolve': 'Creative Tools',
#             'Final Cut Pro': 'Creative Tools',
#             'CorelDRAW': 'Creative Tools',

#             # Productivity
#             'Microsoft Word': 'Productivity',
#             'Microsoft Excel': 'Productivity',
#             'Microsoft PowerPoint': 'Productivity',
#             'Google Docs': 'Productivity',
#             'Google Sheets': 'Productivity',
#             'Google Slides': 'Productivity',
#             'Notion': 'Productivity',
#             'Evernote': 'Productivity',
#             'Trello': 'Productivity',
#             'Asana': 'Productivity',

#             # Development Tools
#             'Visual Studio Code': 'Development Tools',
#             'IntelliJ IDEA': 'Development Tools',
#             'PyCharm': 'Development Tools',
#             'WebStorm': 'Development Tools',
#             'Android Studio': 'Development Tools',
#             'Xcode': 'Development Tools',
#             'Eclipse': 'Development Tools',
#             'NetBeans': 'Development Tools',
#             'Atom': 'Development Tools',
#             'Sublime Text': 'Development Tools',

#             # Communication
#             'Zoom': 'Communication',
#             'Microsoft Teams': 'Communication',
#             'Slack': 'Communication',
#             'Discord': 'Communication',
#             'Skype': 'Communication',
#             'Google Meet': 'Communication',
#             'Webex': 'Communication',
#             'Signal': 'Communication',
#             'Viber': 'Communication',
#             'Line': 'Communication',

#             # Entertainment
#             'Spotify': 'Entertainment',
#             'Apple Music': 'Entertainment',
#             'YouTube Music': 'Entertainment',
#             'Netflix': 'Entertainment',
#             'Amazon Prime Video': 'Entertainment',
#             'Disney+': 'Entertainment',
#             'Hulu': 'Entertainment',
#             'Twitch': 'Entertainment',
#             'VLC Media Player': 'Entertainment',
#             'Plex': 'Entertainment',

#             # Gaming
#             'Steam': 'Gaming',
#             'Epic Games Launcher': 'Gaming',
#             'Origin': 'Gaming',
#             'Ubisoft Connect': 'Gaming',
#             'Battle.net': 'Gaming',
#             'Riot Games Client': 'Gaming',
#             'Minecraft': 'Gaming',
#             'Roblox': 'Gaming',
#             'Fortnite': 'Gaming',
#             'League of Legends': 'Gaming',

#             # Utilities
#             '7-Zip': 'Utilities',
#             'WinRAR': 'Utilities',
#             'CCleaner': 'Utilities',
#             'Malwarebytes': 'Utilities',
#             'Norton Security': 'Utilities',
#             'Dropbox': 'Utilities',
#             'Google Drive': 'Utilities',
#             'OneDrive': 'Utilities',
#             'TeamViewer': 'Utilities',
#             'AnyDesk': 'Utilities',

#             # E-commerce
#             'Amazon': 'E-commerce',
#             'eBay': 'E-commerce',
#             'Etsy': 'E-commerce',
#             'Shopify': 'E-commerce',
#             'AliExpress': 'E-commerce',
#             'Walmart': 'E-commerce',
#             'Target': 'E-commerce',
#             'Best Buy': 'E-commerce',
#             'Newegg': 'E-commerce',
#             'Zalando': 'E-commerce'
#         }

#         with self.data_manager._get_connection() as conn:
#             for app_name, category_name in app_category_mappings.items():
#                 # Get or create the application
#                 app_id = self.data_manager.get_or_create_app(app_name, '')
                
#                 # Update the application's category
#                 conn.execute('''UPDATE application SET category_id = ?
#                              WHERE app_id = ?''',
#                           (self.categories_cache[category_name], app_id))
#             conn.commit()

#     def add_category(self, app_name: str, category_name: str) -> bool:
#         """
#         Add or update a category for an application.
        
#         Args:
#             app_name: Name of the application
#             category_name: Name of the category
            
#         Returns:
#             bool: True if successful, False otherwise
#         """
#         if category_name not in self.categories_cache:
#             return False
            
#         with self.data_manager._get_connection() as conn:
#             # Get or create the application
#             app_id = self.data_manager.get_or_create_app(app_name, '')
            
#             # Update the application's category
#             conn.execute('''UPDATE application SET category_id = ?
#                          WHERE app_id = ?''',
#                       (self.categories_cache[category_name], app_id))
#             conn.commit()
#             return True

#     def get_category(self, app_name: str) -> str:
#         """
#         Get the category for an application.
        
#         Args:
#             app_name: Name of the application
            
#         Returns:
#             str: Category name or "Uncategorized" if not found
#         """
#         with self.data_manager._get_connection() as conn:
#             cursor = conn.execute('''SELECT c.category_name 
#                                   FROM application a
#                                   JOIN categories c ON a.category_id = c.category_id
#                                   WHERE a.app_name = ?''', (app_name,))
#             result = cursor.fetchone()
#             return result[0] if result else "Uncategorized"

#     def update_categories(self, new_categories: Dict[str, str]) -> None:
#         """
#         Update multiple application categories at once.
        
#         Args:
#             new_categories: Dictionary mapping app names to category names
#         """
#         with self.data_manager._get_connection() as conn:
#             for app_name, category_name in new_categories.items():
#                 if category_name in self.categories_cache:
#                     app_id = self.data_manager.get_or_create_app(app_name, '')
#                     conn.execute('''UPDATE application SET category_id = ?
#                                  WHERE app_id = ?''',
#                               (self.categories_cache[category_name], app_id))
#             conn.commit()

#     def get_all_categories(self) -> List[Tuple[int, str, Optional[int]]]:
#         """
#         Get all available categories.
        
#         Returns:
#             List of tuples containing (category_id, category_name, daily_limit)
#         """
#         with self.data_manager._get_connection() as conn:
#             cursor = conn.execute('''SELECT category_id, category_name, daily_limit 
#                                   FROM categories''')
#             return cursor.fetchall()

#     def create_category(self, category_name: str, daily_limit: Optional[int] = None) -> bool:
#         """
#         Create a new category.
        
#         Args:
#             category_name: Name of the new category
#             daily_limit: Optional daily time limit in seconds
            
#         Returns:
#             bool: True if created successfully, False if category already exists
#         """
#         with self.data_manager._get_connection() as conn:
#             try:
#                 conn.execute('''INSERT INTO categories 
#                              (category_name, daily_limit) VALUES (?, ?)''',
#                           (category_name, daily_limit))
#                 conn.commit()
#                 self._load_categories_cache()  # Refresh cache
#                 return True
#             except sqlite3.IntegrityError:  # Category already exists
#                 return False

#     def delete_category(self, category_name: str) -> bool:
#         """
#         Delete a category.
        
#         Args:
#             category_name: Name of the category to delete
            
#         Returns:
#             bool: True if deleted successfully, False if category not found
#         """
#         if category_name not in self.categories_cache:
#             return False
            
#         with self.data_manager._get_connection() as conn:
#             conn.execute('DELETE FROM categories WHERE category_name = ?',
#                       (category_name,))
#             conn.commit()
#             self._load_categories_cache()  # Refresh cache
#             return True

#     def get_apps_in_category(self, category_name: str) -> List[str]:
#         """
#         Get all apps in a specific category.
        
#         Args:
#             category_name: Name of the category
            
#         Returns:
#             List of app names in the category
#         """
#         if category_name not in self.categories_cache:
#             return []
            
#         with self.data_manager._get_connection() as conn:
#             cursor = conn.execute('''SELECT a.app_name 
#                                   FROM application a
#                                   JOIN categories c ON a.category_id = c.category_id
#                                   WHERE c.category_name = ?''', (category_name,))
#             return [row[0] for row in cursor.fetchall()]

#     def set_daily_limit(self, category_name: str, limit_seconds: int) -> bool:
#         """
#         Set a daily time limit for a category.
        
#         Args:
#             category_name: Name of the category
#             limit_seconds: Daily limit in seconds
            
#         Returns:
#             bool: True if successful, False if category not found
#         """
#         if category_name not in self.categories_cache:
#             return False
            
#         with self.data_manager._get_connection() as conn:
#             conn.execute('''UPDATE categories SET daily_limit = ?
#                          WHERE category_name = ?''',
#                       (limit_seconds, category_name))
#             conn.commit()
#             return True

#     def get_daily_limit(self, category_name: str) -> Optional[int]:
#         """
#         Get the daily time limit for a category.
        
#         Args:
#             category_name: Name of the category
            
#         Returns:
#             Optional[int]: Daily limit in seconds, or None if not set
#         """
#         if category_name not in self.categories_cache:
#             return None
            
#         with self.data_manager._get_connection() as conn:
#             cursor = conn.execute('''SELECT daily_limit FROM categories
#                                   WHERE category_name = ?''', (category_name,))
#             result = cursor.fetchone()
#             return result[0] if result else None