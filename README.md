# Bee Swarm Python Macro

Made and tested on mac, currently untested for windows/linux.



## Features

- Gathering for all fields
- Bug runs + Stump Snail
- Planters
- Wealth clock and dispenser collections
- Field Drift Compensation
- Haste Compensation
- Discord webhook
- Hourly Reports
- Disconnect check + auto reconnect
- GUI for setup


## In-Game Requirements
- Glider 
- Access to the red canon


## Social Links
- Discord: https://discord.gg/FTB8b2vB6y (Thanks to kay for setting it up)



## Installation 
Installation guide for  macro

Check your macOS version. This will determine which installation step to follow. To see your macOS version, apple logo -> about this mac

For M1/M2 Macs, I highly recommend updating your macOS version to ventura (13.0) and above. The macro is highly unlikely to work on older versions

For Intel Macs (Basically any mac that isnt M1/M2), macOS 12.0 and above is recommended. Older versions are not likely to work

### 1. Install python 3.9.5
For macOS versions 12.0 and higher:
[python 3.9](https://www.python.org/downloads/release/python-395/) (Scroll down)
*Note: The installers are found near the bottom of the webpage*

Download and run the universal installer if you are on M1/M2, else download the intel installer

![App Screenshot](https://media.discordapp.net/attachments/1081742326860349580/1081749143262875819/sadboiubasd.png?width=1866&height=962)

### 2. Installing certificates

Once python has been installed, it should automatically launch a finder window with a folder called "python 3.9"

Alternatively, you can go to applications -> python 3.9

In the folder, double click on "Install Certificates.command" and let it run 
![App Screenshot](https://media.discordapp.net/attachments/1081742326860349580/1081750296411246652/sdguosaubod.png?width=2160&height=580)

### 3. Open a new terminal


The terminal can be found in finder -> application ->  utilities -> terminal
![App Screenshot](https://media.discordapp.net/attachments/1081742326860349580/1081750377847849010/sabdauspbd.png?width=2160&height=484)

Alternatively, 

cmd + space to bring up spotlight -> search “terminal”

![App Screenshot](https://media.discordapp.net/attachments/1084366756216328213/1084367595890806794/Screenshot_2023-03-12_at_11.png?width=2160&height=298)

### 4. Installing python packages

In terminal, enter these two commands:
```bash
xcode-select --install
```
Install the xcode command line tools when prompted, else you can ignore the message if it says that command line tools are already installed

Next,
```bash
sudo xcode-select --switch /Library/Developer/CommandLineTools
```
Enter in your password

After that,
```bash
pip3 install pyautogui pillow discord-webhook discord.py pynput matplotlib pymupdf
```

After the installation is complete, run these commands one by one

#### For M1/M2 Macs
```bash
arch
```
Terminal should display "arm64"
```bash
pip3 install paddlepaddle==2.3.2

pip3 install --no-deps paddleocr==2.6.1.0
```
```bash
pip3 install attrdict beautifulsoup4 cython fire fonttools imgaug lanms-neo==1.0.2 lmdb lxml opencv-contrib-python opencv-python==4.5.5.64 openpyxl pdf2docx Polygon3 premailer pyclipper pymupdf python-docx rapidfuzz scikit-image shapely tqdm visualdl
```
#### For other Macs (intel cpu)
```bash
python3 -m pip install paddlepaddle==2.4.2 -i https://pypi.tuna.tsinghua.edu.cn/simple

pip3 install "paddleocr>=2.0.1"
```
*Note: you can ignore the error " ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts."*

Finally, enter this
```bash
pip3 install "numpy<1.24.0"
```

### 5. Installing the macro files

Install the .zip file in https://github.com/existancepy/bss-macro-py (Press the green button that says code and look for download zip)

Download it into the downloads folder, or move the zip into the downloads folder.

![App Screenshot](https://media.discordapp.net/attachments/1065032948119769121/1065033447963373690/Screen_Shot_2023-01-17_at_5.png?width=810&height=720)

Extract/Open the .zip file (double click on the .zip file installed)
## Settings
### 6. Roblox settings

In roblox, make sure your settings are as such shown in the image below. 

![App Screenshot](https://media.discordapp.net/attachments/1063607088720396318/1080320071357956136/sahudiasd.png?width=1188&height=962)

The macro only works when roblox is in full screen (takes up 100% of the screen), there should be no dock or top menu bar visible 

If the top menu bar is visible, look at the section below 

### 7. Dock and Menu Bar settings
In system preferences -> dock and menu bar,

Check "automatically hide and show the menu bar in full screen"
![App Screenshot](https://media.discordapp.net/attachments/1081742326860349580/1081755926597480559/spiahhispddsa.png?width=1306&height=962) 

### 8. Security settings

In system preferences -> security and privacy -> privacy

Check "terminal" for these categories:

- Full disk access
- Accessibility
- Screen recording
- Automation (if terminal is not there, you'll be prompted to enable it when running the macro)

*Note that on older macOS versions, some of these categories will not show up, that's to be expected*

### 9. Enable roblox's scaling (Only applicable for macs with a notch)

A notch refers to the built-in camera being attached on the screen. It is typically found on macbook pros (see image below) 
![App Screenshot](https://cdn.discordapp.com/attachments/1081742326860349580/1087240354857754694/macbook-pro-2021-notch-feature.jpeg) 

If your mac does have a notch,
- Close roblox
- In finder -> applications -> right click roblox -> get info -> enable "scale to fit below built-in camera" 

![App Screenshot](https://media.discordapp.net/attachments/1081742326860349580/1087240838230327428/Screenshot_2023-03-19_at_9.png?width=300&height=632) 

- You can now re-open roblox. Roblox should now take up the whole screen, meaning that the camera should block off a part of the app

### 10. Running the macro

 Open terminal and run the command: 
```bash
cd downloads/bss-macro-py-main
```


Run the program with the following command: 
```bash
python3 e_macro.py
```

## Exiting the macro
1. Tab out/close out of Roblox
2. Tap on terminal and press Ctrl + C

## Re-running the macro
Enter the following commands into terminal:

```bash
cd desktop/bss-macro-py-main
```

and
```bash
python3 e_macro.py
```
## Setting up the discord bot

1. Go to [discord applications](https://discord.com/developers/applications)

2. Click on “New Application” (top right)

3. Put in a name, tick the checkbox and create

4. Copy the application id (it is required later)

5. In the “settings” sidebar, click on bot -> add bot

6. Scroll down to “Privileged Gateway Intents” and check “Message Content Intent”

7. Edit and copy in the following link into a web browser:

8. https://discord.com/oauth2/authorize?client_id=<your application id from step 4>&permissions=68608&scope=bot

9. Add your bot to the server and ensure that it has permissions to view the channels you want to use it in

10. Returning back to the application page, click on reset token -> copy

11. Launch the macro and copy the token into the calibration section.

### Discord Bot commands

- Format: <prefix> <command>
- Prefix: !b
- Commands:
    1. rejoin
    2. screenshot

- *Example: !b rejoin*





## Acknowledgements

- For the enable dictation fix: https://www.dofus.com/en/forum/1151-general-problems-solutions/339448-issue-with-macos-keyboard-keys

- Natro Macro for inspiration 
