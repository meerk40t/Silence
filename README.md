# Silence
Silence is a hybrid K40Whisperer/MeerK40t/April-Fools-Joke

Please do not discuss this outside of `#meerk40t` prior to April 1st, 2021.

The gui is finished for the most part. Some code from MeerK40t 0.7.0 is patched in but not yet altered to work. The main guis are all completed. Some added code needs to be pushed circa 0.7.0 in order to ensure this will work.


# Goal
The goal is to implement most of K40 Whisperer with a different frontend and backend. This should include a lot of the advanced features of MeerK40t but shoved into the K40Whisperer box.

# Future
This project is abandon-ware. If we are not finished by April 1st the project will be either pushed a year or silently deleted. If released no future releases will be made other than a couple very basic bug fixes.

# Coordinate System
The coordinate system is the same as that of K40 Whisperer. We are relative to the unlocked laser head starting and returning to the place we started. With forced auto-origin moves.

# Kernel
This project relies on the MeerK40t Kernel and contains many of the advanced features of MeerK40t. These are merely ignored and no direct access is given to those features.

# Expected Features
* Drag and Drop of files
* Direct Drop of Image Files
* Reading of GCode
* Reading of RD files.
* Sending of EGV
* Generation of EGV
* Fast Start Implementation
* Replace RasterSettings with RasterWizard by default (I don't want to implement that other stuff)
* Advanced Scene interactions. Zoom/Pan/Guide
* No resize or alterations
* Require strict lhymicro-gl directionality.

#License
There is no K40 Whisperer code in this (yet), but the GUI is clearly recreated from K40Whisperer as well as the manual being used for popup help. So this code has to be GPL3. Perfectly copying something even without the underlying code would violate copyright and as such needs permission, that permission is granted via GPL3.

Anything that needs to be implemented in a useful fashion will be implemented in MeerK40t and ported over.