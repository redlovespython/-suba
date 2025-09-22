"""
'suba Setup - Installer for Simple Utility for Broadcasting AIMP
Automated setup wizard for 'suba
"""

import os
import sys
import json
import subprocess
import webbrowser
import time

CONFIG_FILE = "suba_config.json"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 52)
    print(" " * 10 + "'suba SETUP WIZARD")
    print(" " * 4 + "Simple Utility for Broadcasting AIMP")
    print(" " * 18 + "made by red.py")
    print("=" * 52)
    print()

def check_python_packages():
    """Check and install required Python packages"""
    print("[PACKAGES] Checking required packages...")
    
    packages = {
        'pypresence': 'pypresence==4.3.0'
    }
    
    for package, install_name in packages.items():
        try:
            __import__(package)
            print(f"  [OK] {package} is installed")
        except ImportError:
            print(f"  [INSTALLING] {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", install_name], 
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"  [OK] {package} installed successfully")
    
    print()

def setup_discord_app():
    """Guide user through Discord app setup"""
    print("[DISCORD] Application Setup")
    print("-" * 52)
    print()
    print("I'll help you create a Discord application for 'suba")
    print()
    
    input("Press Enter to open Discord Developer Portal...")
    webbrowser.open("https://discord.com/developers/applications")
    
    print()
    print("SETUP STEPS:")
    print()
    print("1. Click 'New Application' (top right)")
    print("2. IMPORTANT: Name it 'suba' (this will show in Discord)")
    print("3. Click 'Create'")
    print()
    print("4. Go to 'Rich Presence' -> 'Art Assets' in sidebar")
    print("5. Click 'Add Image(s)' and upload:")
    print("   - A LARGE image (512x512 or bigger)")
    print("   - A SMALL image (at least 32x32)")
    print()
    print("6. Name your images EXACTLY as shown:")
    print("   - Name the large image: album")
    print("   - Name the small image: clover")
    print("7. Wait for images to save (can take a minute)")
    print("8. Click 'Save Changes'")
    print()
    print("9. Go back to 'General Information' in sidebar")
    print("10. Copy your APPLICATION ID")
    print()
    print("-" * 52)
    print()
    
    # Get the Application ID
    while True:
        app_id = input("Paste your Application ID: ").strip()
        if app_id and app_id.isdigit() and len(app_id) >= 17:
            break
        print("[ERROR] Invalid Application ID. Try again.")
    
    print()
    
    # Get image asset names with better defaults
    print("Enter your image names (or press Enter for defaults):")
    print()
    
    large_image = input("Large image name [default: album]: ").strip()
    if not large_image:
        large_image = "album"
    
    small_image = input("Small image name [default: clover]: ").strip()
    if not small_image:
        small_image = "clover"
    
    large_text = input("Large image hover text [default: AIMP]: ").strip()
    if not large_text:
        large_text = "AIMP"
    
    print()
    show_artist = input("Show artist in title? (y/n) [default: y]: ").strip().lower()
    show_artist = show_artist != 'n'
    
    return {
        'discord_app_id': app_id,
        'large_image_key': large_image,
        'small_image_key': small_image,
        'large_image_text': large_text,
        'show_artist_in_title': show_artist
    }

def save_config(config):
    """Save configuration to file"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"[OK] Configuration saved to {CONFIG_FILE}")

def create_batch_files():
    """Create convenient batch files for starting 'suba"""
    
    # Create start_suba.bat
    start_bat = f'''@echo off
title 'suba - Simple Utility for Broadcasting AIMP
python "{os.path.abspath('suba.py')}"
pause
'''
    
    with open('start_suba.bat', 'w') as f:
        f.write(start_bat)
    
    # Create suba_hidden.vbs (runs without console window)
    vbs_content = '''Set objShell = CreateObject("Wscript.Shell")
objShell.Run "python suba.py", 0, False
'''
    
    with open('suba_hidden.vbs', 'w') as f:
        f.write(vbs_content)
    
    print("[OK] Created start_suba.bat (shows console)")
    print("[OK] Created suba_hidden.vbs (runs in background)")

def check_aimp():
    """Check if AIMP is installed"""
    print()
    print("[AIMP] Configuration Check")
    print("-" * 52)
    print()
    print("Make sure AIMP is installed and running.")
    print()
    print("[INFO] No plugins required!")
    print("      'suba uses AIMP's built-in Remote API")
    print("      It works with any AIMP version out of the box")
    print()
    input("Press Enter to continue...")

def create_autostart_option():
    """Offer to add 'suba to Windows startup"""
    print()
    print("[AUTOSTART] Windows Startup (Optional)")
    print("-" * 52)
    print()
    response = input("Start 'suba automatically with Windows? (y/n): ").strip().lower()
    
    if response == 'y':
        startup_folder = os.path.expandvars(r'%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup')
        
        # Create a batch file that starts 'suba hidden
        startup_bat = f'''@echo off
cd /d "{os.getcwd()}"
start "" wscript.exe suba_hidden.vbs
exit
'''
        startup_bat_path = os.path.join(startup_folder, 'start_suba.bat')
        
        with open(startup_bat_path, 'w') as f:
            f.write(startup_bat)
        
        print(f"[OK] Added 'suba to Windows startup")
        print(f"     Location: {startup_bat_path}")
        print("     (Delete this file to disable auto-start)")

def main():
    print_header()
    
    print("Welcome to 'suba Setup")
    print("This wizard will configure everything for you")
    print()
    input("Press Enter to begin...")
    
    print_header()
    
    # Step 1: Install packages
    print("[STEP 1/4] Installing Requirements")
    print("-" * 52)
    check_python_packages()
    
    # Step 2: Discord setup
    print("[STEP 2/4] Discord Application")
    print("-" * 52)
    config = setup_discord_app()
    
    print_header()
    
    # Step 3: Save config
    print("[STEP 3/4] Saving Configuration")
    print("-" * 52)
    save_config(config)
    create_batch_files()
    
    print()
    
    # Step 4: AIMP setup
    print("[STEP 4/4] AIMP Configuration")
    print("-" * 52)
    check_aimp()
    
    # Optional: Autostart
    create_autostart_option()
    
    # Done
    print()
    print("=" * 52)
    print("              SETUP COMPLETE")
    print("=" * 52)
    print()
    print("You can now run 'suba using:")
    print("  start_suba.bat     (shows console)")
    print("  suba_hidden.vbs    (runs in background)")
    print()
    print("Make sure Discord and AIMP are running first")
    print()
    
    test = input("Test 'suba now? (y/n): ").strip().lower()
    if test == 'y':
        print()
        print("Starting 'suba...")
        time.sleep(2)
        import suba
        suba.main()
    else:
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[CANCELLED] Setup cancelled")
    except Exception as e:
        print(f"\n[ERROR] Setup failed: {e}")
        input("\nPress Enter to exit...")