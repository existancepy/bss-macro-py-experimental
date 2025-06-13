import subprocess
import plistlib

def is_full_keyboard_access_enabled():
    try:
        result = subprocess.run(
            ["defaults", "read", "com.apple.universalaccess", "KeyboardAccessEnabled"],
            capture_output=True,
            text=True
        )
        value = result.stdout.strip()
        return value == "1"  # 1 = Full Keyboard Access is enabled
    except Exception as e:
        print("Error reading Full Keyboard Access:", e)
        return False

enabled = is_full_keyboard_access_enabled()
print("Full Keyboard Access is", "enabled" if enabled else "disabled")
