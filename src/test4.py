from modules.misc.ColorProfile import DisplayColorProfile


# Direct equivalent to the original Swift code
def replicate_swift_behavior():
    """Direct replication of the original Swift code behavior"""
    profile_manager = DisplayColorProfile()
    
    # Equivalent to: ColorSyncDeviceSetCustomProfiles(DEVICE_CLASS, NSScreen.main!.cfUUID, RESET_PROFILE_DICT)
    print("Resetting display profile...")
    profile_manager.resetDisplayProfile()
    
    # Equivalent to: ColorSyncDeviceSetCustomProfiles(DEVICE_CLASS, NSScreen.main!.cfUUID, CUSTOM_PROFILE_DICT)
    print("Setting custom profile...")
    profile_manager.setCustomProfile("/System/Library/ColorSync/Profiles/sRGB Profile.icc")

a = DisplayColorProfile()
print(a.getCurrentColorProfile())
