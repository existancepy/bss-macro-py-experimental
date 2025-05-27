
#!/bin/sh
read -p "Enter file name: " filename
cd "$(dirname "$0")"
cd ..
if [ -d bin ]; then
   source ./bin/activate
fi
cd src
python3 $filename
