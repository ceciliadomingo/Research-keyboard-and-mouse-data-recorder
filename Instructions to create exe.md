# How to convert py file to exe
1.- Make sure py file works 
* runs
* opens popup
* start recording
* move mouse and press some keys
* wait one minute
* press stop recording and close window
* check that directory now has RECORDER files:
  * One or more images (1 per minute)
  * Mouse log
  * Keys log
  * Cursor log
  * Screen resolution log

2.- Install pyinstaller library</br>
3.- Run on terminal: pyinstaller --onefile "yourfile.py"</br>
4.- Exe will be created inside a "dist" folder</br>
5.- Check it works
