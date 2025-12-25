"""
Test script to verify all connections are working
Run this before starting the main bot
"""
import sys
import os

def test_python_version():
    """Test if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Requires 3.8+)")
        return False

def test_dependencies():
    """Test if all required packages are installed"""
    print("\n🔍 Checking dependencies...")
    required_packages = [
        'telegram',
        'gspread',
        'oauth2client',
        'google.auth',
        'apscheduler',
        'dotenv',
        'pytz'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} (Not installed)")
            all_installed = False
    
    return all_installed

def test_env_file():
    """Test if .env file exists and has required variables"""
    print("\n🔍 Checking .env configuration...")
    
    if not os.path.exists('.env'):
        print("❌ .env file not found")
        return False
    
    print("✅ .env file exists")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    required_vars = [
        'TELEGRAM_BOT_TOKEN',
        'GOOGLE_SHEETS_ID'
    ]
    
    all_set = True
    for var in required_vars:
        value = os.getenv(var)
        if value and value != 'your_bot_token_here' and value != 'your_google_sheets_id_here':
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is not set or using default value")
            all_set = False
    
    return all_set

def test_credentials_file():
    """Test if credentials.json exists"""
    print("\n🔍 Checking Google credentials...")
    
    if os.path.exists('credentials.json'):
        print("✅ credentials.json found")
        return True
    elif os.getenv('GOOGLE_CREDENTIALS'):
        print("✅ GOOGLE_CREDENTIALS environment variable found")
        return True
    else:
        print("❌ Neither credentials.json nor GOOGLE_CREDENTIALS found")
        return False

def test_google_sheets_connection():
    """Test Google Sheets connection"""
    print("\n🔍 Testing Google Sheets connection...")
    
    try:
        from sheets_manager import SheetsManager
        sheets = SheetsManager()
        print("✅ Successfully connected to Google Sheets")
        
        # Try to read first row
        try:
            inventory = sheets.inventory_sheet.row_values(1)
            print(f"✅ Inventory sheet accessible (columns: {len(inventory)})")
        except Exception as e:
            print(f"⚠️  Warning: Could not read inventory sheet: {e}")
            return False
        
        try:
            log = sheets.log_sheet.row_values(1)
            print(f"✅ Log sheet accessible (columns: {len(log)})")
        except Exception as e:
            print(f"⚠️  Warning: Could not read log sheet: {e}")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Failed to connect to Google Sheets: {e}")
        return False

def test_telegram_token():
    """Test if Telegram bot token is valid"""
    print("\n🔍 Testing Telegram bot token...")
    
    try:
        import config
        from telegram import Bot
        import asyncio
        
        async def test_bot():
            bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
            me = await bot.get_me()
            return me
        
        me = asyncio.run(test_bot())
        print(f"✅ Bot token is valid")
        print(f"   Bot name: @{me.username}")
        print(f"   Bot ID: {me.id}")
        return True
    except Exception as e:
        print(f"❌ Failed to validate bot token: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("🧪 Church Tech Ministry Bot - Connection Test")
    print("=" * 50)
    
    results = []
    
    results.append(("Python Version", test_python_version()))
    results.append(("Dependencies", test_dependencies()))
    results.append(("Environment File", test_env_file()))
    results.append(("Google Credentials", test_credentials_file()))
    results.append(("Google Sheets", test_google_sheets_connection()))
    results.append(("Telegram Bot Token", test_telegram_token()))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the bot.")
        print("Run: python main.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above before running the bot.")
        print("Check SETUP_GUIDE.md for detailed setup instructions.")
    
    print("=" * 50)

if __name__ == '__main__':
    main()

