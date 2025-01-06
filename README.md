# RAAI Module: Camera Calibration  

This module generates a `matrix.csv` file based on chessboard pattern recognition, which can be used to correct lens distortion in images captured by the camera.  

---

## Features  
- Automatically recognizes chessboard patterns from a live camera feed.  
- Generates a calibration matrix (`matrix.csv`) for distortion correction.  
- Displays the number of recognized patterns in real-time.  

---

## How to Use  

1. **Edit the Configuration File**  
   - Open the configuration file.  
   - Set the following parameters according to your chessboard image:  
     - **Chessboard size** (number of inner corners in rows and columns).  
     - **Square size** (length of a square in the chessboard, in real-world units).  

2. **Run the Module**  
   - Start the program.  
   - Hold the chessboard image in front of the camera at various angles.  
   - Ensure the chessboard pattern is fully visible in the camera frame.  

3. **Pattern Recognition**  
   - The program will recognize chessboard patterns and display the count in the top-right corner of the live camera stream.  
   - After recognizing a pattern, the program will pause for **2 seconds** to let you readjust the image.  

4. **Generate the Calibration Matrix**  
   - When you are satisfied with the number of recognized patterns, press the **"q" key** to finalize the process and generate the `matrix.csv` file.  
   - Note: The file creation may take some time, depending on the number of recognized chessboard patterns.  
