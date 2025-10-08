import os
import sys

def setup_vlc_path():
    """Setup VLC library path for bundled or system VLC"""
    
    # Check if running as PyInstaller bundle
    if getattr(sys, 'frozen', False):
        # Running as executable
        bundle_dir = os.path.dirname(sys.executable)
        
        # Look for bundled VLC in parent directory
        vlc_paths = [
            os.path.join(bundle_dir, '..', 'vlc'),  # Electron app structure
            os.path.join(bundle_dir, 'vlc'),        # Same directory
        ]
        
        for vlc_path in vlc_paths:
            if os.path.exists(vlc_path):
                libvlc_dll = os.path.join(vlc_path, 'libvlc.dll')
                if os.path.exists(libvlc_dll):
                    # Add VLC path to system PATH
                    os.environ['PATH'] = vlc_path + os.pathsep + os.environ.get('PATH', '')
                    # Set plugin path
                    plugins_path = os.path.join(vlc_path, 'plugins')
                    if os.path.exists(plugins_path):
                        os.environ['VLC_PLUGIN_PATH'] = plugins_path
                    print(f"VLC found and configured at: {vlc_path}")
                    return True
        
        print("Warning: Bundled VLC not found, trying system VLC")
    
    # Try system VLC paths
    system_vlc_paths = [
        r'C:\Program Files\VideoLAN\VLC',
        r'C:\Program Files (x86)\VideoLAN\VLC'
    ]
    
    for vlc_path in system_vlc_paths:
        if os.path.exists(vlc_path):
            libvlc_dll = os.path.join(vlc_path, 'libvlc.dll')
            if os.path.exists(libvlc_dll):
                os.environ['PATH'] = vlc_path + os.pathsep + os.environ.get('PATH', '')
                print(f"System VLC found at: {vlc_path}")
                return True
    
    print("Error: VLC not found in bundled or system locations")
    return False