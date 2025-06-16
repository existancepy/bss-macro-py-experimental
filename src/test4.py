import time
import Quartz
from AppKit import NSWorkspace
from ApplicationServices import AXUIElementCreateApplication, AXUIElementCopyAttributeValue, kAXChildrenAttribute, kAXTitleAttribute, kAXRoleAttribute

def get_pid_by_app_name(app_name):
    workspace = NSWorkspace.sharedWorkspace()
    apps = workspace.runningApplications()
    for app in apps:
        if app.localizedName() == app_name:
            return app.processIdentifier()
    return None

def get_app_ax_element(pid):
    return AXUIElementCreateApplication(pid)

def get_children(element):
    try:
        children = AXUIElementCopyAttributeValue(element, kAXChildrenAttribute)
        return children or []
    except Exception:
        return []

def find_element_by_title(element, target_title):
    children = get_children(element)
    print(children)
    for child in children:
        try:
            title = AXUIElementCopyAttributeValue(child, kAXTitleAttribute)
            if title == target_title:
                return child
            found = find_element_by_title(child, target_title)
            if found:
                return found
        except Exception:
            continue
    return None

def perform_click(element):
    try:
        AXUIElementPerformAction(element, "AXPress")
        print("Clicked!")
    except Exception as e:
        print("Click failed:", e)

# --- Main logic ---
pid = get_pid_by_app_name("Brave Browser")
if not pid:
    print("Roblox not running.")
    exit()

app = get_app_ax_element(pid)
target = find_element_by_title(app, "Game Mode")  # Adjust if needed

if target:
    perform_click(target)
else:
    print("Game Mode button not found.")