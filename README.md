# RAAI Module Camera calibration
The camera calibration module creates a matrix.csv file based on chessboard recognition, which can be used to correct 
distorted images taken with the camera

## how to use
To create the matrix u should first edit the config file, change the chessboard size and the square size according to 
the picture you are using. Then start the module and hold the image in the camera from various angles. After that
you need to press the key "q" to create the matrix and exit the program. The file creation can take a while, that depends
on the amount of chessboard patterns that where recognised. The amount will be displayed in the top right corner of the
camera stream picture. After the program recognises a chessboard pattern it will pause for 2 seconds for you to readjust 
the picture
