import re

with open('macro.py', 'r') as f:
    content = f.read()

# Match mouse.moveTo(<anything>, <anything>) including variables or expressions
pattern = r'mouse\.moveTo\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)'

# Replace with offset wrapped version
def replacer(match):
    arg1 = match.group(1)
    arg2 = match.group(2)
    return f'mouse.moveTo(self.mx+({arg1}), self.my+({arg2}))'

new_content = re.sub(pattern, replacer, content)

with open('macro 2.py', 'w') as f:
    f.write(new_content)
