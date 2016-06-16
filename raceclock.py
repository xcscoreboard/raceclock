#!/usr/bin/env python

from Tkinter import *
import datetime
try:
   import cPickle as pickle
except:
   import pickle

def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    d["minutes"] = "{:>02}".format(d["minutes"])
    d["seconds"] = "{:>02}".format(d["seconds"])
    return fmt.format(**d)

class Timer():
  def __init__(self, master, Groups=False):
    self.master = master
    self.master.attributes('-fullscreen', True)
    self.master.configure(background = 'black')
    self.config = {}
    self.config['timerpadx'] = 0
    self.config['timerpady'] = 0
    self.config['buttoncol'] = 43
    self.config['buttonrow'] = 49
    self.config['timerfontsize'] = 200
    self.config['buttonfontsize'] = 32
    self.config['disabledfgcolor'] = 'green'
    try:
      self.raceclockcfg = open('raceclock.cfg', mode='r')
      self.config = pickle.load(self.raceclockcfg)
    except:
      pass
    else:
      self.raceclockcfg.close()

    self.master.bind("<Control-Right>", lambda event: self.redraw_button((0,1)))
    self.master.bind("<Control-Left>", lambda event:self.redraw_button((0,-1)))
    self.master.bind("<Control-Up>", lambda event: self.redraw_button((-1,0)))
    self.master.bind("<Control-Down>", lambda event:self.redraw_button((1,0)))
    self.master.bind("<Alt-Right>", lambda event: self.redraw_timer((0,1)))
    self.master.bind("<Alt-Left>", lambda event:self.redraw_timer((0,-1)))
    self.master.bind("<Alt-Up>", lambda event: self.redraw_timer((-1,0)))
    self.master.bind("<Alt-Down>", lambda event:self.redraw_timer((1,0)))
    self.master.bind("<Shift-Up>", self.shiftup)
    self.master.bind("<Shift-Down>", self.shiftdown)
    self.master.bind("<Shift-Right>", self.shiftright)
    self.master.bind("<Shift-Left>", self.shiftleft)
    self.master.bind(".", lambda event: self.colorchange(1))
    self.master.bind(",", lambda event: self.colorchange(-1))
    self.timer_active=False
    self.timerstr = StringVar()
    self.timerstr.set("00:00")
    self.timer = Entry(self.master, textvariable=self.timerstr, bg="grey", fg="yellow",
                 font=("Helvetica", self.config['timerfontsize']),
                 width=5, disabledbackground="black", disabledforeground=self.config['disabledfgcolor'], borderwidth=0)
    #self.buttongroup = Pmw.Group(self.master,tag_pyclass=None)
    self.buttongroup = Frame(master=self.master)
    self.start = Button(self.buttongroup, text="Start", fg="black", 
                 font=("Helvetica", self.config['buttonfontsize']), relief=RAISED)
    self.start["command"] = self.start_timer
    self.stop = Button(self.buttongroup, text="Stop", fg="black",
                 font=("Helvetica", self.config['buttonfontsize']), relief=RAISED)
    self.stop["command"] = self.stop_timer
    self.reset = Button(self.buttongroup, text="Reset", fg="black",
                 font=("Helvetica", self.config['buttonfontsize']), relief=RAISED)
    self.reset["command"] = self.reset_timer
    self.exit = Button(self.buttongroup, text="Exit", fg="black",
                 font=("Helvetica", self.config['buttonfontsize']), relief=RAISED)
    self.exit["command"] = self.Exit
    self.buttongroup.grid(row=self.config['buttonrow'], column=self.config['buttoncol'], sticky=E)
    self.start.grid(row=0, column=0, sticky=W)
    self.stop.grid(row=0, column=1, sticky=W)
    self.reset.grid(row=0, column=2, sticky=W)
    self.exit.grid(row=0, column=3, sticky=W)
    self.timer.grid(row=0, column=0, columnspan=100, rowspan=100, sticky=W+E, padx=self.config['timerpadx'], pady=self.config['timerpady'])

  def colorchange(self,upordown):
    i = COLORS.index(self.config['disabledfgcolor']) + upordown
    if i == len(COLORS):
      i = 0
    elif i < 0:
      i = len(COLORS-1)
    self.config['disabledfgcolor'] = COLORS[i]
    self.timer.config(disabledforeground=self.config['disabledfgcolor'])

  def shiftleft(self,event):
    self.config['buttonfontsize'] -= 1
    self.start.configure(font=("Helvetica", self.config['buttonfontsize']))
    self.stop.configure(font=("Helvetica", self.config['buttonfontsize']))
    self.reset.configure(font=("Helvetica", self.config['buttonfontsize']))
    self.exit.configure(font=("Helvetica", self.config['buttonfontsize']))

  def shiftright(self,event):
    self.config['buttonfontsize'] += 1
    self.start.configure(font=("Helvetica", self.config['buttonfontsize']))
    self.stop.configure(font=("Helvetica", self.config['buttonfontsize']))
    self.reset.configure(font=("Helvetica", self.config['buttonfontsize']))
    self.exit.configure(font=("Helvetica", self.config['buttonfontsize']))

  def shiftup(self,event):
    self.config['timerfontsize'] += 1
    self.timer.configure(font=("Helvetica", self.config['timerfontsize']))

  def shiftdown(self,event):
    self.config['timerfontsize'] -= 1
    self.timer.configure(font=("Helvetica", self.config['timerfontsize']))

  def redraw_timer(self, move):
    self.config['timerpadx'] += move[1] 
    if self.config['timerpadx'] < 0:
      self.config['timerpadx'] -= move[1] 
      return
    self.config['timerpady'] += move[0] 
    if self.config['timerpady'] < 0:
      self.config['timerpady'] -= move[0] 
      return
    self.timer.grid_forget()
    self.timer.grid(row=0, column=0, columnspan=100, rowspan=100, sticky=W+E, padx=self.config['timerpadx'], pady=self.config['timerpady'])

  def redraw_button(self, move):
    self.config['buttoncol'] += move[1] 
    if self.config['buttoncol'] < 0 or self.config['buttoncol'] > 99:
      self.config['buttoncol'] -= move[1] 
      return
    self.config['buttonrow'] += move[0] 
    if self.config['buttonrow']< 0 or self.config['buttonrow'] > 99:
      self.config['buttonrow'] -= move[0] 
      return
    if self.buttongroup.grid_info() != {}:
      self.buttongroup.grid_forget()
      self.buttongroup.grid(row=self.config['buttonrow'], column=self.config['buttoncol'], sticky=E)

  def toggle_buttons(self,event):
    if self.buttongroup.grid_info() =={}:
      self.buttongroup.grid(row=self.config['buttonrow'], column=self.config['buttoncol'], sticky=E)
    else:
      self.buttongroup.grid_forget()

  def start_timer(self):
    self.timer.config(state=DISABLED)
    self.timer.bind("<ButtonPress-1>", self.toggle_buttons)
    timertext = self.timerstr.get()
    try:
      deltatime = datetime.datetime.strptime(timertext, "%M:%S") - datetime.datetime.strptime("00:00", "%M:%S")
    except:
      deltatime = datetime.datetime.strptime("00:00", "%M:%S") - datetime.datetime.strptime("00:00", "%M:%S")
    self.start_time = datetime.datetime.now() - deltatime
    self.timer_active = True
    self.update_clock()
    c=True

  def stop_timer(self):
    self.timer.config(state=NORMAL)
    self.timer.unbind("<ButtonPress-1>")
    self.timer_active = False
    self.timer["bg"] = "grey"
    self.timer["fg"] = "yellow"

  def reset_timer(self):
    self.timerstr.set("00:00")

  def Exit(self):
    root.destroy()
    self.raceclockcfg = open('raceclock.cfg', mode='w')
    pickle.dump(self.config,self.raceclockcfg)
    self.raceclockcfg.close()

  def update_clock(self):
    if self.timer_active:
      self.display_time = datetime.datetime.now() - self.start_time
      if self.display_time.total_seconds() >= 3600:
        display_time_str = strfdelta(self.display_time, "{hours}:{minutes}:{seconds}")
        if self.display_time.total_seconds() < 3601.5:
          self.timer.config(width=7)
      else:
        display_time_str = strfdelta(self.display_time, "{minutes}:{seconds}")
      self.timerstr.set(display_time_str)
      self.master.after(1000, self.update_clock)

COLORS  =['green', 'snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']

if __name__ == "__main__":
  root = Tk()
  root.title ("Timer")
  timer = Timer(root)
  root.mainloop()
