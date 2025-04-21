# import cv2
# import pyautogui as pag
# # Assuming templateMatch uses cv2.matchTemplate
# from modules.screen.imageSearch import templateMatch 
# from modules.screen.screenshot import mssScreenshotNP
# from modules.misc.imageManipulation import pillowToCv2
# # Removed getScreenData as it wasn't used
# import numpy as np
import time
# from PIL import Image
# from concurrent.futures import ThreadPoolExecutor

# class HasteCompensationOptimized():
#     mw, mh = pag.size() 
#     BUFF_REGION = (0, 30, int(mw / 1.8), 70)

#     def __init__(self, isRetina, baseMoveSpeed):
#         self.isRetina = isRetina
#         self.baseMoveSpeed = baseMoveSpeed
        
#         # Determine the correct buff region based on screen size (if needed)
#         # For simplicity, using the class variable directly for now.
#         # You might adjust self.buff_region here if it depends on isRetina or other factors.
#         self.buff_region = HasteCompensationOptimized.BUFF_REGION

#         # --- Optimization 2: Preload and Preprocess Templates ---
#         self.hasteStacks = []
#         for i in range(10):
#             # Load, resize, and convert to grayscale ONCE during initialization
#             img = self._load_and_prepare_template(f"./images/buffs/haste{i+1}.png")
#             self.hasteStacks.append(img)
#         # Store as (index, template) pairs, reversed order is already handled
#         self.hasteStacks = list(enumerate(self.hasteStacks))[::-1] 

#         self.bearMorphs = []
#         for i in range(5):
#             # Prepare bear morph templates
#             img = self._load_and_prepare_template(f"./images/buffs/bearmorph{i+1}-retina.png")
#             self.bearMorphs.append(img)

#         # Prepare haste+ template
#         self.hastePlus = self._load_and_prepare_template(f"./images/buffs/haste+.png")

#         self.prevHaste = 0
#         self.prevHaste368 = 0 # Tracking previous haste for 3/6/8 ambiguity
#         self.hasteEnds = 0
#         self.prevHasteEnds = 0 # Value used during compensation period

#     def _load_and_prepare_template(self, path):
#         """Loads, resizes, converts to CV2 format, and converts to grayscale."""
#         try:
#             img = Image.open(path)
#             # Get original size
#             width, height = img.size
#             # Adjust scaling based on Retina display
#             scaling = 1 if self.isRetina else 2
#             # Resize image
#             new_width = max(1, int(width / scaling)) # Ensure width is at least 1
#             new_height = max(1, int(height / scaling)) # Ensure height is at least 1
#             img = img.resize((new_width, new_height))
#             # Convert to cv2 format (ensure it returns BGR)
#             cv2_img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#             # --- Optimization 3: Convert Templates to Grayscale ---
#             # Template matching is often faster on grayscale images
#             gray_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
#             return gray_img
#         except FileNotFoundError:
#             print(f"Warning: Template image not found at {path}")
#             return None # Handle missing files gracefully
#         except Exception as e:
#             print(f"Error processing template {path}: {e}")
#             return None

#     # --- Optimization 5: Refine thresholdMatch (if possible) ---
#     # Assuming templateMatch is a wrapper around cv2.matchTemplate
#     # If you have control over templateMatch, ensure it's efficient.
#     # Using TM_CCOEFF_NORMED is common.
#     def _thresholdMatch(self, target_template, screen_grayscale, threshold=0.7):
#         """Performs template matching on grayscale images."""
#         if target_template is None: # Skip if template failed to load
#              return (False, 0.0)
             
#         # Ensure screen_grayscale is also grayscale and uint8
#         # screen_grayscale should already be prepared before calling this
        
#         # Assuming templateMatch directly uses or wraps cv2.matchTemplate
#         # and expects grayscale images now.
#         # res = templateMatch(target_template, screen_grayscale) 
        
#         # --- Direct cv2.matchTemplate example (if templateMatch is simple) ---
#         # Use TM_CCOEFF_NORMED for normalized correlation coefficient matching
#         res = cv2.matchTemplate(screen_grayscale, target_template, cv2.TM_CCOEFF_NORMED)
#         min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#         # For TM_CCOEFF_NORMED, the best match is the max_val
#         # print(f"Matching {target_template.shape} against {screen_grayscale.shape}: MaxVal={match_value:.2f}") # Debug

#         # _, val, _, loc = res # Original line assumes templateMatch returns this tuple
#         # Using max_val from cv2.minMaxLoc directly:
#         return (max_val > threshold, max_val)


#     def getHaste(self):
#         st = time.perf_counter() # Keep for timing checks


#         screen_cv2 = cv2.cvtColor(mssScreenshotNP(self.buff_region[0], self.buff_region[1], 
#                                    self.buff_region[2], self.buff_region[3]), cv2.COLOR_RGBA2BGR)

#         # --- Optimization 4: Convert Screenshot to Grayscale Once ---
#         screen_grayscale = cv2.cvtColor(screen_cv2, cv2.COLOR_BGR2GRAY)

#         bestHaste = 0
#         bestHasteMaxVal = 0

#         # Match haste stacks (templates are already grayscale)
#         def match_haste(args):
#             i, template = args
#             res, val = self._thresholdMatch(template, screen_grayscale, 0.7)
#             return (i, res, val)
        
#         with ThreadPoolExecutor(max_workers=6) as executor:
#             args = [(i, template) for i, template in self.hasteStacks]
#             results = executor.map(match_haste, args)

#         for haste, res, val in results:
#             if res and val > bestHasteMaxVal:
#                 bestHaste = haste+1
#                 bestHasteMaxVal = val

#         # Ambiguity resolution for 3, 6, 8
#         if bestHaste in [3, 6, 8]:
#             # This logic seems complex and potentially error-prone.
#             # Consider if higher thresholds or different template images
#             # could distinguish these better.
#             if self.prevHaste368 == 2: 
#                 bestHaste = 3 # Confirmed 3
#             elif self.prevHaste368 == 5: 
#                 bestHaste = 6 # Confirmed 6
#             else: bestHaste = 8 # Default to 8 if ambiguity detected without clear precursor?
#         else:
#             self.prevHaste368 = bestHaste # Update tracker state


#         hasteOut = bestHaste

#         #failed to detect haste, but the haste is still there (~7.5 secs remaining)
#         if not hasteOut:
#             currTime = time.time()
#             if currTime > self.hasteEnds and self.prevHaste: #there is no ongoing hasteEnds
#                 self.prevHasteEnds = self.prevHaste #value to set for the time compensation
#                 #decrease the countdown for retina (detection is more accurate)
#                 if self.isRetina:
#                     self.hasteEnds = currTime + (0 if hasteOut == 1 else 2)
#                 else:
#                     self.hasteEnds = currTime + (4 if hasteOut == 1 else 7)
#             #there is a hasteEnd ongoing
#             if currTime < self.hasteEnds:
#                 hasteOut = self.prevHasteEnds

#         self.prevHaste = bestHaste

#         print(hasteOut)

#         # Match bear morph (using any() for efficiency)
#         bearMorph = 0 # Default to 0
#         def match_bear(template):
#             return self._thresholdMatch(template, screen_grayscale, 0.75)[0]
#         with ThreadPoolExecutor(max_workers=4) as executor:
#             results = executor.map(match_bear, self.bearMorphs)
            
#         if any(results):
#             bearMorph = 4
#             print("bear")

#         # Match haste+
#         haste_plus_threshold = 0.75
#         if self._thresholdMatch(self.hastePlus, screen_grayscale, haste_plus_threshold)[0]:
#             hasteOut += 10
#             print("hastePlus active") # Debug

#         # Calculate final speed
#         # print(f"Haste stacks: {hasteOut}, Bear: {bearMorph}") # Debug
#         final_speed = (self.baseMoveSpeed + bearMorph) * (1 + (0.1 * hasteOut))

#         # print(f"Calculation time: {time.perf_counter() - st:.4f}s") # Debug timing
#         return final_speed


from modules.submacros.hasteCompensation import HasteCompensationOptimized, HasteCompensation
h = HasteCompensationOptimized(True, 29)

time.sleep(2)
st = time.time()
print(h.getHaste())
print(time.time()-st)

hc = HasteCompensation(True, 29)
st = time.time()
print(hc.getHaste())
print(time.time()-st)

