# What is this?
If you are looking for a different approach to interact with **Ableton** or if you are using the **SoftStep2 foot midi controller**, this might be interesting for you. This is a project of 2015, so it might be outdated in one way or another.

This is a custom SoftStep2 foot-based midi controller integration for Ableton that I wrote in 2015. It has quite some advanced features to sync Softstep2 with Ableton or make Softstep2 behave differently depending the context.

I didn't use the standard high level Controller APIs from Ableton to create this controller as I wanted a better understanding and more control. So if you are looking into writing your own controller in Python or if you are using the SoftStep2, please have a look as if this is not outdated it may save you some Googling time. Good luck and have fun.

# How to install
todo :(

# What does it solve?
* It's a Softstep 2 controller that you can install and use (you may want to adjust it though - so being OK to modify Python would be good. No need to be an expert for that)
* It's a custom Python API to interact with the Controller or with Ableton

## Advanced SoftStep2 controller for SessionView

The key file is **DomsSoftStep2Controller.py**. The controller is updated in real time from within Ableton and not just when something changes - this allows to do some advanced things such as having LEDs blink by used BPM or scroll text over the display.


## Custom Ableton Low-Level API (Python)

### API for Controlling SoftStep2 from within Ableton

* API to make it easier to set the text of the Softstep2 **Display** including Midi messages that are/were not in the SoftStep2 documentation
* Softstep2 Controller code / API itself allows to
	* display the select clip position in the session view 
	* 
* * Advanced control over the display 
	* Set the text
	* Make the text scroll to show messages that are longer than the display can show at a time
	* Set a short info-text messages as interlude which will revert back to the previous text automatically. Good for quick feedback to the user that a command was received while the display itself is otherwise used to show some current state
* API to the the **LEDs**
	* On or Off or FastFlash or Slow Flash
	* Green or Red
	* Setable for all 10 keys

### Mapping
This is the hardcoded MIDI mapping. If you want to adjust it, go to the **def receive_midi** code block in the file **DomsSoftStep2Controller.py** file or check at the top of the file.

**MIDI messages** that the midi controller device has to send to Ableton
* CC  21: Toggle Exclusive Arming
* CC  22: Toggle Clip Arming
* CC  60: Session View Navigation: Up ( Value > 93) / DOWN (Value < 34)
* CC  61: Session View Navigation: LEFT (Value < 34) / RIGHT  ( Value > 90)
* CC  80: Tap Temp
* CC 110: Fire/Record selected master
* CC 118: Undo / Redo toggle
* CC 120: Stop Stop Clips
* CC 121: Stop All Clips
* CC 122: Stop Song

**LEDs**
* Green Slow Flash: Selected is triggered for playing
* Green: selected is playing
* Red Slow Flash: Selected is triggered for recording
* Red: selected is recording

**Text Display**
* Position in the Session View of the Selected Clip (column_row aka tracks_scenes)
* "M_" if it's a master
* beat with prefix for
	* "R" recording
	* "P" playing


### Ableton Live API Helper
A different API to read or modify Ableton's session view * made it easier for me to understand Ableton under the hood and write a controller the way I approached it. Here's roughly what can be done with it (haven't used it for a while so might be obselete or not fully working anymore):

* Tracks
	(is master selected, is selected recordable, get selected index, disarm all, exlusive arming, stop selected, set monitoring to auto)
* Clips (slots)
	(fire, fire legato, fire or stop (toggle), stop, is selected a recordable track, is selected recording, is selected playing, is selected triggered for playing / recording,  get most lef playing clip, get most left playing pos)
* Scene
	(get selected, fire selected)
* Session View 
	(go left, go right, go_up, go_down)
* Song
	(undo, undo or redo if possible, stop all clips, stop, tap_tempo, is_playing, beat_index)
* App
	( get live app, show status message)

### Custom MidiMsg helper to hide required byte manipulation when working with Midi
* Easier Compositoin / Decomposition for
	type, channel, data 1 and data 2
* is_cc 
* types are
	Note Off, Note On, Aftertouch, Controller Change, CC, Program Change, Pitch Wheel

### Custom logging to disk solution
It can be hard to debug when things go wrong during during startup such a compilation error etc. This writes a custom log file to make it a lot easier. Check the files:
* Logging.py
* __init__.py
* settings.py (to enable / disable it. It's on atm and you may want to disable it here)





