"""
Google Sheets Manager
Handles all interactions with Google Sheets
"""
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import config

class SheetsManager:
    def __init__(self):
        """Initialize Google Sheets connection"""
        import os
        import json
        
        self.scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        
        try:
            # Check if credentials are provided as environment variable (for deployment)
            if os.getenv('GOOGLE_CREDENTIALS'):
                creds_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
                self.creds = Credentials.from_service_account_info(
                    creds_dict,
                    scopes=self.scopes
                )
                print("🔑 Using credentials from environment variable")
            else:
                # Use credentials file (for local development)
                self.creds = Credentials.from_service_account_file(
                    'credentials.json',
                    scopes=self.scopes
                )
                print("🔑 Using credentials from file")
            
            self.client = gspread.authorize(self.creds)
            self.spreadsheet = self.client.open_by_key(config.GOOGLE_SHEETS_ID)
            self.inventory_sheet = self.spreadsheet.worksheet(config.INVENTORY_SHEET_NAME)
            self.log_sheet = self.spreadsheet.worksheet(config.LOG_SHEET_NAME)
            print("✅ Successfully connected to Google Sheets")
        except Exception as e:
            print(f"❌ Error connecting to Google Sheets: {e}")
            raise
    
    def get_item_by_id(self, item_id):
        """
        Find an item by its ID in the inventory sheet
        Returns: dict with item details or None if not found
        """
        try:
            all_items = self.inventory_sheet.get_all_records()
            
            for idx, item in enumerate(all_items, start=2):  # Start from row 2 (after header)
                if str(item.get('ItemID', '')).strip().upper() == str(item_id).strip().upper():
                    item['_row_number'] = idx
                    return item
            
            return None
        except Exception as e:
            print(f"Error fetching item: {e}")
            return None
    
    def check_availability(self, item_id):
        """
        Check if an item is available for rent
        Returns: (available: bool, quantity: int, item_details: dict)
        """
        item = self.get_item_by_id(item_id)
        
        if not item:
            return False, 0, None
        
        quantity = int(item.get('Quantity', 0))
        
        # Check active rentals for this item
        active_rentals = self.get_active_rentals_for_item(item_id)
        available_quantity = quantity - active_rentals
        
        return available_quantity > 0, available_quantity, item
    
    def get_active_rentals_for_item(self, item_id):
        """
        Count how many units of this item are currently rented
        """
        try:
            all_logs = self.log_sheet.get_all_records()
            active_count = 0
            
            for log in all_logs:
                if (str(log.get('Item ID', '')).strip().upper() == str(item_id).strip().upper() 
                    and log.get('Status', '').upper() == 'ACTIVE'):
                    active_count += 1
            
            return active_count
        except Exception as e:
            print(f"Error checking active rentals: {e}")
            return 0
    
    def log_rental(self, borrower_name, telegram_username, user_id, item_id, item_name, 
                   rental_start, expected_return, pickup_photo_url):
        """
        Log a new rental transaction
        """
        try:
            row = [
                borrower_name,
                telegram_username,
                str(user_id),  # Store user ID for reminders
                item_id,
                item_name,
                rental_start,
                expected_return,
                '',  # Actual Return Date (empty for now)
                'ACTIVE',  # Status
                pickup_photo_url,
                ''  # Return Photo (empty for now)
            ]
            
            self.log_sheet.append_row(row)
            print(f"✅ Logged rental for {item_id} by {borrower_name}")
            return True
        except Exception as e:
            print(f"Error logging rental: {e}")
            return False
    
    def get_active_rentals_by_user(self, user_id):
        """
        Get all active rentals for a specific user
        Returns: list of rental records
        """
        try:
            all_logs = self.log_sheet.get_all_records()
            user_rentals = []
            
            for idx, log in enumerate(all_logs, start=2):
                if (str(log.get('User ID', '')).strip() == str(user_id).strip() 
                    and log.get('Status', '').upper() == 'ACTIVE'):
                    log['_row_number'] = idx
                    user_rentals.append(log)
            
            return user_rentals
        except Exception as e:
            print(f"Error fetching user rentals: {e}")
            return []
    
    def complete_return(self, row_number, return_photo_url):
        """
        Mark a rental as returned
        """
        try:
            actual_return_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Update Actual Return Date
            self.log_sheet.update_cell(
                row_number, 
                config.LOG_COLUMNS['ACTUAL_RETURN'] + 1, 
                actual_return_date
            )
            
            # Update Status
            self.log_sheet.update_cell(
                row_number, 
                config.LOG_COLUMNS['STATUS'] + 1, 
                'RETURNED'
            )
            
            # Update Return Photo
            self.log_sheet.update_cell(
                row_number, 
                config.LOG_COLUMNS['RETURN_PHOTO'] + 1, 
                return_photo_url
            )
            
            print(f"✅ Marked rental at row {row_number} as returned")
            return True
        except Exception as e:
            print(f"Error completing return: {e}")
            return False
    
    def get_all_due_tomorrow(self):
        """
        Get all rentals that are due tomorrow (for reminder notifications)
        Returns: list of rentals with user info
        """
        try:
            from datetime import timedelta
            import pytz
            
            tomorrow = (datetime.now(pytz.timezone(config.TIMEZONE)) + timedelta(days=1)).date()
            
            all_logs = self.log_sheet.get_all_records()
            due_tomorrow = []
            
            for log in all_logs:
                if log.get('Status', '').upper() == 'ACTIVE':
                    expected_return = log.get('Expected Return Date', '')
                    try:
                        # Parse the expected return date
                        return_date = datetime.strptime(expected_return, '%Y-%m-%d').date()
                        
                        if return_date == tomorrow:
                            due_tomorrow.append(log)
                    except:
                        continue
            
            return due_tomorrow
        except Exception as e:
            print(f"Error fetching due tomorrow rentals: {e}")
            return []

