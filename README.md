# Raceclock
raceclock.py is a small GUI based python script that makes a full screen raceclock/stopwatch. I built it so I could use a 32" TV screen at my cross country meets to serve as my raceclock. I run it on a cheap raspberry pi computer that I tape to the back of the TV, but should run on any windows/linux/mac box you have lying around. When the raceclock is stopped, the digit entry area can be edited so you can start/restart the clock from whatever time you wish (e.g., 00:00, 01:00, 0:2:20).

The size and positions of the clock and buttons can be customized using the following key-presses. After exiting raceclock, the settings are saved in raceclock.cfg file so that next time you open raceclock, things look the same as when you last used it.
* Shift-Up and Shift-Down increase and decrease the size of the clock digits.
* Shift-Left and Shift-Right increase and decrease the size of the buttons (Start, Stop, Reset, and Exit buttons)
* Alt-Left, Alt-Right, Alt-Up, and Alt-Down position the location of the clock on the screen.
* Shift-Left, Shift-Right, Shift-Up, and Shift-Down position the location of the buttons on the screen.
 
After you start the clock, simply click anywhere in the clock display background to toggle the visibility of the buttons. This allows you to have a unencumbered view of the clock digits.

Also after you start the clock, the color of the digits can changed by pressing the "." and "," keys to cycle through the list of supported colors (forward and backwards through the list) until you find a color to your liking.

Again, once you exit raceclock, it will save your settings in raceclock.cfg (located in your current folder/directory).
