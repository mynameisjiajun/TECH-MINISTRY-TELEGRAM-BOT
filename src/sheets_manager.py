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
    
    def enrich_rental_with_item_details(self, rental):
        """
        Enrich a rental record with item details from inventory
        Adds 'Item Name' and 'Location' fields
        """
        item_id = rental.get('Item ID', '').strip()
        if item_id:
            item = self.get_item_by_id(item_id)
            if item:
                rental['Item Name'] = item.get('Item Name', 'Unknown')
                rental['Location'] = item.get('Location', 'Unknown')
        return rental
    
    def check_availability(self, item_id):
        """
        Check if an item is available for rent
        Uses "Quantity Current" to determine stock availability
        Returns: (available: bool, quantity: int, item_details: dict)
        """
        item = self.get_item_by_id(item_id)
        
        if not item:
            return False, 0, None
        
        # Use "Quantity Current" for stock checking
        quantity_current = int(item.get('Quantity Current', 0))
        
        # If Quantity Current is 0, item is out of stock
        if quantity_current == 0:
            return False, 0, item
        
        # Available quantity is the Quantity Current value
        available_quantity = quantity_current
        
        return available_quantity > 0, available_quantity, item
    
    def log_rental(self, borrower_name, telegram_username, user_id, item_id, item_name, 
                   rental_start, expected_return, pickup_photo_url, quantity=1):
        """
        Log a new rental transaction and increment Loaned Out counter
        Each rental is logged as a separate row
        """
        try:
            # Get current date and time
            request_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Log the rental - NEW STRUCTURE
            row = [
                request_datetime,      # Date & Time
                borrower_name,         # Borrower Name
                telegram_username,     # Telegram Username
                str(user_id),         # User ID
                item_id,              # Item ID
                quantity,             # Quantity (from user input)
                rental_start,         # Rental Start Date
                expected_return,      # Expected Return Date
                '',                   # Actual Return Date (empty for now)
                'ACTIVE',             # Status
                pickup_photo_url,     # Pickup Photo
                ''                    # Return Photo (empty for now)
            ]
            
            self.log_sheet.append_row(row)
            
            # Increment the "Loaned Out" counter in inventory by the quantity
            item = self.get_item_by_id(item_id)
            
            if not item or '_row_number' not in item:
                return True
            
            try:
                # Get current Loaned Out value
                current_loaned_raw = item.get('Loaned Out', 0)
                
                # Convert to int, handling empty strings and None
                if current_loaned_raw == '' or current_loaned_raw is None:
                    current_loaned = 0
                else:
                    current_loaned = int(current_loaned_raw)
                
                new_loaned = current_loaned + quantity
                
                # Column index for Loaned Out
                loaned_out_col = config.INVENTORY_COLUMNS['LOANED_OUT'] + 1
                
                # Update the Loaned Out column
                self.inventory_sheet.update_cell(
                    item['_row_number'],
                    loaned_out_col,
                    new_loaned
                )
                
            except Exception as update_error:
                print(f"Error updating inventory: {update_error}")
            
            return True
        except Exception as e:
            print(f"Error logging rental: {e}")
            return False
    
    def get_active_rentals_by_user(self, user_id):
        """
        Get all active rentals for a specific user
        Returns: list of rental records with item details enriched
        """
        try:
            all_values = self.log_sheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return []
            
            headers = all_values[0]
            user_rentals = []
            
            for idx, row in enumerate(all_values[1:], start=2):
                if len(row) > config.LOG_COLUMNS['STATUS']:
                    user_id_val = str(row[config.LOG_COLUMNS['USER_ID']]).strip()
                    status_val = str(row[config.LOG_COLUMNS['STATUS']]).upper()
                    
                    if user_id_val == str(user_id).strip() and status_val == 'ACTIVE':
                        # Create dictionary from row
                        log = {
                            'Borrower Name': row[config.LOG_COLUMNS['BORROWER_NAME']] if len(row) > config.LOG_COLUMNS['BORROWER_NAME'] else '',
                            'Telegram Username': row[config.LOG_COLUMNS['TELEGRAM_USERNAME']] if len(row) > config.LOG_COLUMNS['TELEGRAM_USERNAME'] else '',
                            'User ID': row[config.LOG_COLUMNS['USER_ID']] if len(row) > config.LOG_COLUMNS['USER_ID'] else '',
                            'Item ID': row[config.LOG_COLUMNS['ITEM_ID']] if len(row) > config.LOG_COLUMNS['ITEM_ID'] else '',
                            'Quantity': int(row[config.LOG_COLUMNS['QUANTITY']]) if len(row) > config.LOG_COLUMNS['QUANTITY'] and row[config.LOG_COLUMNS['QUANTITY']] else 1,
                            'Rental Start Date': row[config.LOG_COLUMNS['RENTAL_START']] if len(row) > config.LOG_COLUMNS['RENTAL_START'] else '',
                            'Expected Return Date': row[config.LOG_COLUMNS['EXPECTED_RETURN']] if len(row) > config.LOG_COLUMNS['EXPECTED_RETURN'] else '',
                            'Status': row[config.LOG_COLUMNS['STATUS']] if len(row) > config.LOG_COLUMNS['STATUS'] else '',
                            '_row_number': idx
                        }
                        log = self.enrich_rental_with_item_details(log)
                        user_rentals.append(log)
            
            return user_rentals
        except Exception as e:
            print(f"Error fetching user rentals: {e}")
            return []
    
    def complete_return(self, row_number, return_photo_url):
        """
        Mark a rental as returned and decrement Loaned Out counter by the rented quantity
        """
        try:
            # Get the item ID and quantity from this rental row
            row_values = self.log_sheet.row_values(row_number)
            item_id = row_values[config.LOG_COLUMNS['ITEM_ID']] if len(row_values) > config.LOG_COLUMNS['ITEM_ID'] else None
            quantity = int(row_values[config.LOG_COLUMNS['QUANTITY']]) if len(row_values) > config.LOG_COLUMNS['QUANTITY'] else 1
            
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
            
            # Decrement the "Loaned Out" counter in inventory by the quantity
            if item_id:
                print(f"🔍 Looking up item {item_id} for return (Quantity: {quantity})...")
                item = self.get_item_by_id(item_id)
                if item and '_row_number' in item:
                    try:
                        current_loaned_raw = item.get('Loaned Out', 0)
                        if current_loaned_raw == '' or current_loaned_raw is None:
                            current_loaned = 0
                        else:
                            current_loaned = int(current_loaned_raw)
                        new_loaned = max(0, current_loaned - quantity)
                        
                        loaned_out_col = config.INVENTORY_COLUMNS['LOANED_OUT'] + 1
                        
                        # Update the Loaned Out column
                        self.inventory_sheet.update_cell(
                            item['_row_number'],
                            loaned_out_col,
                            new_loaned
                        )
                    except Exception as update_error:
                        print(f"Error updating inventory on return: {update_error}")
            
            return True
        except Exception as e:
            print(f"Error completing return: {e}")
            return False
    
    def get_all_due_tomorrow(self):
        """
        Get all rentals that are due tomorrow (for reminder notifications)
        Returns: list of rentals with user info and item details
        """
        try:
            from datetime import timedelta
            import pytz
            
            tomorrow = (datetime.now(pytz.timezone(config.TIMEZONE)) + timedelta(days=1)).date()
            
            all_values = self.log_sheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return []
            
            due_tomorrow = []
            
            for row in all_values[1:]:  # Skip header
                if len(row) > config.LOG_COLUMNS['STATUS']:
                    status_val = str(row[config.LOG_COLUMNS['STATUS']]).upper()
                    expected_return = row[config.LOG_COLUMNS['EXPECTED_RETURN']] if len(row) > config.LOG_COLUMNS['EXPECTED_RETURN'] else ''
                    
                    if status_val == 'ACTIVE' and expected_return:
                        try:
                            return_date = datetime.strptime(expected_return, '%Y-%m-%d').date()
                            
                            if return_date == tomorrow:
                                log = {
                                    'Borrower Name': row[config.LOG_COLUMNS['BORROWER_NAME']] if len(row) > config.LOG_COLUMNS['BORROWER_NAME'] else '',
                                    'User ID': row[config.LOG_COLUMNS['USER_ID']] if len(row) > config.LOG_COLUMNS['USER_ID'] else '',
                                    'Item ID': row[config.LOG_COLUMNS['ITEM_ID']] if len(row) > config.LOG_COLUMNS['ITEM_ID'] else '',
                                    'Quantity': int(row[config.LOG_COLUMNS['QUANTITY']]) if len(row) > config.LOG_COLUMNS['QUANTITY'] and row[config.LOG_COLUMNS['QUANTITY']] else 1,
                                    'Expected Return Date': expected_return
                                }
                                log = self.enrich_rental_with_item_details(log)
                                due_tomorrow.append(log)
                        except:
                            continue
            
            return due_tomorrow
        except Exception as e:
            print(f"Error fetching due tomorrow rentals: {e}")
            return []
    
    def get_all_active_rentals(self):
        """
        Get all active rentals (for admin)
        Returns: list of all active rental records with item details
        """
        try:
            all_values = self.log_sheet.get_all_values()
            if not all_values or len(all_values) < 2:
                return []
            
            active_rentals = []
            
            for row in all_values[1:]:  # Skip header
                if len(row) > config.LOG_COLUMNS['STATUS']:
                    status_val = str(row[config.LOG_COLUMNS['STATUS']]).upper()
                    
                    if status_val == 'ACTIVE':
                        log = {
                            'Borrower Name': row[config.LOG_COLUMNS['BORROWER_NAME']] if len(row) > config.LOG_COLUMNS['BORROWER_NAME'] else '',
                            'Telegram Username': row[config.LOG_COLUMNS['TELEGRAM_USERNAME']] if len(row) > config.LOG_COLUMNS['TELEGRAM_USERNAME'] else '',
                            'User ID': row[config.LOG_COLUMNS['USER_ID']] if len(row) > config.LOG_COLUMNS['USER_ID'] else '',
                            'Item ID': row[config.LOG_COLUMNS['ITEM_ID']] if len(row) > config.LOG_COLUMNS['ITEM_ID'] else '',
                            'Quantity': int(row[config.LOG_COLUMNS['QUANTITY']]) if len(row) > config.LOG_COLUMNS['QUANTITY'] and row[config.LOG_COLUMNS['QUANTITY']] else 1,
                            'Rental Start Date': row[config.LOG_COLUMNS['RENTAL_START']] if len(row) > config.LOG_COLUMNS['RENTAL_START'] else '',
                            'Expected Return Date': row[config.LOG_COLUMNS['EXPECTED_RETURN']] if len(row) > config.LOG_COLUMNS['EXPECTED_RETURN'] else '',
                            'Status': row[config.LOG_COLUMNS['STATUS']] if len(row) > config.LOG_COLUMNS['STATUS'] else ''
                        }
                        log = self.enrich_rental_with_item_details(log)
                        active_rentals.append(log)
            
            return active_rentals
        except Exception as e:
            print(f"Error fetching active rentals: {e}")
            return []
    
    def user_has_overdue_items(self, user_id):
        """
        Check if a user has any overdue items
        Returns: (has_overdue: bool, overdue_rental: dict or None)
        """
        try:
            rentals = self.get_active_rentals_by_user(user_id)
            today = datetime.now().date()
            
            for rental in rentals:
                expected_return = rental.get('Expected Return Date', '')
                if expected_return:
                    try:
                        return_date = datetime.strptime(expected_return, '%Y-%m-%d').date()
                        if return_date < today:
                            return True, rental
                    except:
                        continue
            
            return False, None
        except Exception as e:
            print(f"Error checking overdue items: {e}")
            return False, None

