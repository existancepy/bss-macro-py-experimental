# Required: pip install pyobjc-core pyobjc-framework-avfoundation
import sys
import objc

# Attempt to import the AVFoundation framework binding
try:
    import AVFoundation
except ImportError:
    print("ERROR: Failed to import the 'AVFoundation' module.")
    print("Please ensure PyObjC AVFoundation bindings are installed:")
    print("pip install pyobjc-framework-avfoundation")
    if __name__ == "__main__":
        sys.exit(1)
    else:
        # Allow calling code to handle the import error
        raise ImportError("AVFoundation module not found. PyObjC installation required.")

def can_record_screen_avfoundation():
    """
    Checks screen recording permission using AVFoundation's authorization status API.
    This is the recommended method on modern macOS (approx. 10.15+ for Screen).

    Returns:
        bool | str | None:
            - True: Permission is explicitly granted ('authorized').
            - False: Permission is explicitly denied ('denied').
            - 'notdetermined': Permission has not been requested yet for this app.
            - 'restricted': Permission is restricted (e.g., by parental controls or MDM).
            - None: An error occurred (e.g., not on macOS, AVFoundation issue, unsupported OS).
    """
    if sys.platform != 'darwin':
        print("Error: This check is only compatible with macOS.")
        return None

    try:
        # Check the authorization status directly using the class method
        # AVMediaTypeScreen requires macOS 10.15 Catalina or later.
        media_type = AVFoundation.AVMediaTypeVideo
        print(dir(AVFoundation.AVCaptureDevice))
        status = AVFoundation.AVCaptureDevice.authorizationStatus(forMediaType=media_type)

        # --- Process the Status ---
        if status == AVFoundation.AVAuthorizationStatusAuthorized:
            print("AVFoundation check: Screen Recording permission is Authorized.")
            return True
        elif status == AVFoundation.AVAuthorizationStatusDenied:
            print("AVFoundation check: Screen Recording permission is Denied.")
            return False
        elif status == AVFoundation.AVAuthorizationStatusNotDetermined:
            print("AVFoundation check: Screen Recording permission is Not Determined.")
            print("(The system should prompt the user on the first capture attempt.)")
            # Return a distinct value to indicate this state
            return "notdetermined"
        elif status == AVFoundation.AVAuthorizationStatusRestricted:
            print("AVFoundation check: Screen Recording permission is Restricted.")
            print("(Cannot be granted by the user, e.g., due to parental controls or MDM profile.)")
            # Return a distinct value to indicate this state
            return "restricted"
        else:
            # Should not happen with standard constants, but good practice to check
            print(f"AVFoundation check: Received unknown authorization status code ({status}).")
            return None # Indicate an unexpected state or error

    except AttributeError as e:
        # This likely means AVMediaTypeScreen constant or authorizationStatus method
        # is not available (e.g., older macOS version before 10.15, or PyObjC issue)
        print(f"Error: Failed to use AVFoundation API ({e}).")
        print("This method typically requires macOS 10.15 (Catalina) or later for screen recording checks.")
        print("Ensure PyObjC AVFoundation bindings are installed and compatible.")
        return None
    except Exception as e:
        # Catch any other unexpected errors during the API call
        print(f"An unexpected error occurred during the AVFoundation check: {e}")
        return None

# --- Example Usage ---
if __name__ == "__main__":
    print("Attempting to check screen recording permission using AVFoundation...")
    # Make the call within a function/block to handle potential early exit/raise on import failure
    permission_status_result = None
    try:
        permission_status_result = can_record_screen_avfoundation()
    except ImportError as e:
        print(e)
        # Error message already printed within the import block

    print("-" * 20)

    # Interpret the result
    if permission_status_result is True:
        print("Result: Screen Recording Permission is GRANTED (Authorized).")
    elif permission_status_result is False:
        print("Result: Screen Recording Permission is DENIED.")
    elif permission_status_result == "notdetermined":
        print("Result: Screen Recording Permission is NOT DETERMINED.")
        print("The user hasn't been asked yet for this application.")
    elif permission_status_result == "restricted":
        print("Result: Screen Recording Permission is RESTRICTED.")
        print("Granting permission is disallowed by system policy.")
    else:
        # This covers None return value (errors)
        print("Result: Could not reliably determine Screen Recording Permission status.")
        print("Check previous error messages for details (macOS version, PyObjC install).")

    # Reminder for testing procedure
    print("\n--- Testing Reminder ---")
    print("1. Go to System Settings > Privacy & Security > Screen Recording.")
    print("2. Find the app running this script (e.g., Terminal, Python, VSCode).")
    print("3. Toggle the permission OFF (Denied) or ON (Authorized).")
    print("4. Rerun the script to see if the status matches.")
    print("5. If 'Not Determined', an actual capture attempt by an app might be needed to trigger the prompt.")
