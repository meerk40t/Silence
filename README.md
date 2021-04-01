# Silence
Silence is a hybrid K40Whisperer/MeerK40t/April-Fools-Joke

The name is a pun as to silence some criticism, and a more extreme form of whisperer.

![silence](https://user-images.githubusercontent.com/3302478/113282245-84c4ac80-929b-11eb-87c0-2375071b6a76.png)

# Devices
This is intended to work with either windows or libusb drivers for either Lhystudios boards or Moshiboards (no rastering).

# Goal
The goal of this project is to be be a very intricate joke and to implement most of K40 Whisperer with a different frontend and backend. This should include a lot of the advanced features of MeerK40t but shoved into the K40Whisperer box. With notable amounts of simplification therein.

This project should be finished by April 1st for release on that date.

# Future

This project is abandon-ware. No future releases will be made other than basic bug fixes, and things that should have been implemented but missed the release date. If anybody wants the project they can have it.

# Simplifications

The coordinate system is the same as that of K40 Whisperer. We are relative to the unlocked laser head starting and returning to the place we started, with forced auto-origin moves.

The elements backend code is Whisperer-esque. There are 4 boxes. Raster, Engrave, Cut, Gcode/CutCode and the boxes can be sent as one off commands triggered by a button. There is no classifications or anything fancy. Push the button get those laser commands.

# Kernel
This project relies on the MeerK40t Kernel and contains many of the advanced features of MeerK40t. These are merely ignored and little direct access is given to those features given in the GUI. If you're adventurous you can hit F12 and load up the Terminal, there you'll have access to all a lot of interesting features. For example `engrave set power 500` will set the engrave power to half.

# License
There is no K40 Whisperer code in this (yet), but the GUI is clearly recreated from K40Whisperer as well as the Whisperer manual being used for popup help. So this code has to be GPL3. Perfectly copying something even without the underlying code would violate copyright and as such needs permission, that permission is granted via GPL3. Most everything else is likely to be part of MeerK40t's MIT licensed code.

---

* Thanks to Scorch.
* Thanks to Dext Moss (originally had this idea, though it didn't go anywhere).
* Thanks to Joe Lane, he makes a lot of this stuff possible.

“Silence is a source of Great Strength.” ― Lao Tzu

April Fools.

