# Silence
Silence is a hybrid K40Whisperer/MeerK40t/April-Fools-Joke

Please do not discuss this outside of `#meerk40t` prior to April 1st, 2021.

The name is a pun as to silence some criticism and an even quieter form of Whisperer.

# Progress

The gui is finished for the most part. Some code from MeerK40t 0.7.0 is patched in but not yet altered to work. The main guis are all completed. Some added code needs to be pushed circa 0.7.0 in order to ensure this will work.


# Goal
The goal is to implement most of K40 Whisperer with a different frontend and backend. This should include a lot of the advanced features of MeerK40t but shoved into the K40Whisperer box. With notable amounts of simplification therein. 

This project should be finished by April 1st for release, on that date.

# Future
This project is abandon-ware. If we are not finished by April 1st the project will be either pushed a year or silently deleted. If released no future releases will be made other than basic bug fixes. If anybody wants the project they can have it.

# Simplifications
The coordinate system is the same as that of K40 Whisperer. We are relative to the unlocked laser head starting and returning to the place we started, with forced auto-origin moves.

The elements backend code will be the Whisperer-esque. There are 4 boxes. Raster, Engrave, Cut, Gcode/CutCode and the boxes can be sent as one off commands triggered by a button. There will be no classifications or anything fancy done here.

# Kernel
This project relies on the MeerK40t Kernel and contains many of the advanced features of MeerK40t. These are merely ignored and no direct access is given to those features given in the GUI, console access may grant access to those.

This might need to include some console commands to give some access to fancier MeerK40t features, like setting dot_length and PPI values for some particular type of operation.

# Expected Features
* Drag-and-Drop of files
* Direct read of image files
* Reading of GCode
* Reading of RD files.
* Sending of EGV
* Generation of EGV
* Fast-Start Implementation
* Correct multi-threaded code.
* Replace RasterSettings with RasterWizard by default (I don't want to implement that other stuff)
* Advanced Scene interactions. Zoom/Pan/Guides PinchZoom, TouchScreen. 
* No resize or alterations
* Require strict lhymicro-gl directionality.
* OSX validation for proper functionality throughout
* Moshiboard support (raster may be speed capped vector-rasters)
* CLI support
* Some method of dealing with almost-red strokes, either warning the user or otherwise asking them what they would like done with those lines
* Native Zingl-Bresenham curve plotting.

Most all of this will just be ported in from 0.7.x and altered to fit. Some simplifications should make that easier. A different bit of core code would need to be written to fit this paradigm.


# License
There is no K40 Whisperer code in this (yet), but the GUI is clearly recreated from K40Whisperer as well as the manual being used for popup help. So this code has to be GPL3. Perfectly copying something even without the underlying code would violate copyright and as such needs permission, that permission is granted via GPL3.

Anything that needs to be implemented in a useful fashion will be implemented in MeerK40t and ported over.