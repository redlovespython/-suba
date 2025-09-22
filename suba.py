"""
'suba - Simple Utility for Broadcasting AIMP
Minimal Discord Rich Presence for AIMP
made by red.py

No plugins required - uses AIMP's built-in Remote API
"""

import time
import sys
import os
import json
import struct
import ctypes
import ctypes.wintypes
from pypresence import Presence
from datetime import datetime

CONFIG_FILE = "suba_config.json"
VERSION = "1.0.0"

# AIMP Remote API Constants
WM_AIMP_COMMAND = 0x0400 + 0x75
WM_AIMP_NOTIFY = 0x0400 + 0x76
WM_AIMP_PROPERTY = 0x0400 + 0x77

AIMP_REMOTE_CLASS = "AIMP2_RemoteInfo"
AIMP_REMOTE_MAPFILE_SIZE = 2048

# Property IDs
AIMP_RA_PROPERTY_VERSION = 0x10
AIMP_RA_PROPERTY_PLAYER_POSITION = 0x20
AIMP_RA_PROPERTY_PLAYER_DURATION = 0x30
AIMP_RA_PROPERTY_PLAYER_STATE = 0x40
AIMP_RA_PROPERTY_VOLUME = 0x50

# Commands
AIMP_RA_CMD_PLAY = 15
AIMP_RA_CMD_PAUSE = 16
AIMP_RA_CMD_STOP = 17
AIMP_RA_CMD_NEXT = 18
AIMP_RA_CMD_PREV = 19

class AIMPRemoteAPI:
    def __init__(self):
        self.hwnd = None
        
    def find_aimp(self):
        """Find AIMP window"""
        try:
            # Find AIMP main window by class name
            FindWindow = ctypes.windll.user32.FindWindowW
            
            # Try different AIMP window classes
            window_classes = [
                "TAIMPMainForm",  # AIMP 4/5 main window
                "AIMP2_RemoteInfo",
                "AIMP3_RemoteInfo", 
                "AIMP4_RemoteInfo"
            ]
            
            for class_name in window_classes:
                self.hwnd = FindWindow(class_name, None)
                if self.hwnd:
                    return True
                    
            # If not found by class, find by window title containing AIMP
            EnumWindows = ctypes.windll.user32.EnumWindows
            EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
            
            def enum_callback(hwnd, windows):
                if ctypes.windll.user32.IsWindowVisible(hwnd):
                    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
                    if length > 0:
                        buff = ctypes.create_unicode_buffer(length + 1)
                        ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
                        if "AIMP" in buff.value:
                            self.hwnd = hwnd
                            return False
                return True
            
            EnumWindows(EnumWindowsProc(enum_callback), 0)
            return self.hwnd != 0
        except:
            return False
    
    def connect(self):
        """Connect to AIMP"""
        return self.find_aimp()
    
    def get_window_title(self):
        """Get AIMP window title which contains track info"""
        if not self.hwnd:
            return None
            
        try:
            length = ctypes.windll.user32.GetWindowTextLengthW(self.hwnd)
            if length > 0:
                buff = ctypes.create_unicode_buffer(length + 1)
                ctypes.windll.user32.GetWindowTextW(self.hwnd, buff, length + 1)
                return buff.value
        except:
            pass
        return None
    
    def get_track_info(self):
        """Parse track info from window title"""
        title = self.get_window_title()
        if not title:
            return None
        
        # Remove "AIMP" from the end if present
        if " - AIMP" in title:
            title = title.replace(" - AIMP", "")
        
        # Common patterns:
        # "Artist - Title"
        # "Title"
        # "Artist - Album - Title"
        
        parts = title.split(" - ")
        
        if len(parts) >= 2:
            # Assume first part is artist, last part is title
            artist = parts[0].strip()
            track_title = parts[-1].strip()
        else:
            # Just the title
            track_title = title.strip()
            artist = "Unknown Artist"
        
        return {
            'artist': artist,
            'album': "Unknown Album",
            'title': track_title,
            'duration': 0
        }
    
    def get_player_state(self):
        """Check if AIMP is playing (simplified)"""
        # If we can find the window and it has a title with track info, assume playing
        title = self.get_window_title()
        if title and title != "AIMP":
            return 2  # Playing
        return 0  # Stopped
    
    def get_player_position(self):
        """Get current position (not available through window title)"""
        return 0
    
    def close(self):
        """Close connections"""
        pass

class Suba:
    def __init__(self):
        self.rpc = None
        self.aimp = None
        self.config = None
        self.running = False
        self.last_state = None
        
    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(CONFIG_FILE):
            print("[ERROR] Config file not found. Run suba_setup.py first.")
            input("\nPress Enter to exit...")
            sys.exit(1)
        
        try:
            with open(CONFIG_FILE, 'r') as f:
                self.config = json.load(f)
            return True
        except Exception as e:
            print(f"[ERROR] Failed to load config: {e}")
            return False
    
    def connect_discord(self):
        """Connect to Discord RPC"""
        try:
            print("[INFO] Connecting to Discord...")
            self.rpc = Presence(self.config['discord_app_id'])
            self.rpc.connect()
            print("[OK] Connected to Discord")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to connect to Discord: {e}")
            print("       Make sure Discord is running")
            return False
    
    def connect_aimp(self):
        """Connect to AIMP via Remote API"""
        try:
            print("[INFO] Connecting to AIMP...")
            self.aimp = AIMPRemoteAPI()
            if self.aimp.connect():
                print("[OK] Connected to AIMP")
                return True
            else:
                print("[ERROR] Could not connect to AIMP")
                print("       Make sure AIMP is running")
                return False
        except Exception as e:
            print(f"[ERROR] Failed to connect to AIMP: {e}")
            return False
    
    def get_track_info(self):
        """Get current track information from AIMP"""
        try:
            state = self.aimp.get_player_state()
            if state == 0:  # Stopped
                return None
            
            # Get track metadata
            track_data = self.aimp.get_track_info()
            if not track_data:
                # If we can't read track data, just show generic info
                return {
                    'title': "Playing Music",
                    'duration': 0,
                    'position': 0,
                    'state': state,
                    'raw_title': "Music",
                    'raw_artist': "AIMP"
                }
            
            # Get timing info
            position = self.aimp.get_player_position()
            
            # Debug output
            if self.config.get('debug', False):
                print(f"[DEBUG] Track: {track_data['title']}")
                print(f"[DEBUG] Artist: {track_data['artist']}")
                print(f"[DEBUG] State: {state}")
            
            # Combine title and artist if configured
            if self.config.get('show_artist_in_title', True) and track_data['artist'] != "Unknown Artist":
                display_title = f"{track_data['title']} - {track_data['artist']}"
            else:
                display_title = track_data['title']
            
            return {
                'title': display_title,
                'duration': track_data['duration'],
                'position': position,
                'state': state,
                'raw_title': track_data['title'],
                'raw_artist': track_data['artist']
            }
        except Exception as e:
            return None
    
    def update_presence(self):
        """Update Discord Rich Presence"""
        try:
            info = self.get_track_info()
            
            # Clear presence if nothing is playing
            if not info:
                if self.last_state is not None:
                    self.rpc.clear()
                    print("[STATUS] Playback stopped - presence cleared")
                    self.last_state = None
                return
            
            # Check if we need to update
            if (self.last_state and 
                self.last_state['title'] == info['title'] and 
                self.last_state['state'] == info['state']):
                return
            
            # Build presence data
            presence = {
                'details': info['title'],
                'state': 'Listening on AIMP',
                'large_image': self.config['large_image_key'],
                'large_text': self.config.get('large_image_text', 'AIMP'),
                'small_image': self.config['small_image_key'],
                'small_text': 'made by red.py'
            }
            
            # Note: Progress bar not available with window title method
            
            # Update Discord
            self.rpc.update(**presence)
            
            # Show what's playing
            status = "[PLAYING]" if info['state'] == 2 else "[PAUSED]"
            print(f"{status} {info['raw_title']} - {info['raw_artist']}")
            
            self.last_state = info
            
        except Exception as e:
            print(f"[WARNING] Error updating presence: {e}")
    
    def run(self):
        """Main loop"""
        print("\n" + "="*50)
        print("    'suba - Simple Utility for Broadcasting AIMP")
        print("                  made by red.py")
        print("="*50 + "\n")
        
        # Load config
        if not self.load_config():
            input("\nPress Enter to exit...")
            return
        
        # Connect to AIMP
        if not self.connect_aimp():
            print("\n[INFO] No plugins required!")
            print("[INFO] 'suba uses AIMP's built-in Remote API")
            input("\nPress Enter to exit...")
            return
        
        # Connect to Discord
        if not self.connect_discord():
            input("\nPress Enter to exit...")
            return
        
        print("\n[OK] 'suba is running. Minimize this window.")
        print("     Press Ctrl+C to stop\n")
        
        self.running = True
        
        try:
            while self.running:
                self.update_presence()
                time.sleep(3)  # Update every 3 seconds
        except KeyboardInterrupt:
            print("\n\n[INFO] Stopping 'suba...")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up connections"""
        self.running = False
        if self.rpc:
            try:
                self.rpc.clear()
                self.rpc.close()
                print("[OK] Discord presence cleared")
            except:
                pass
        if self.aimp:
            self.aimp.close()
        print("[OK] 'suba stopped")

def main():
    try:
        suba = Suba()
        suba.run()
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()