import Live
import time
from MidiMessage import MidiMsg
from SoftStepLEDs import LEDInfo
from SoftStepDisplay import DisplayInfo


class DisplayControl(object):

	class TextElement(object):

		CONFIG_DISPLAY_POSITIONS = 4
		# all in ms
		TIMING_DEFAULT_DISPLAY_DURATION = 300
		TIMING_SCROLL_START_DISPLAY_DURATION = 300
		TIMING_SCROLL_END_DISPLAY_DURATION = 350
		TIMING_SCROLL_SPEED_DELAY = 50

		def __init__(self):
			self.__text = ""
			self.__text_offset_index = 0
			self.__display_start_time_in_ms = time.time() * 1000
			self.__animate = False
			self.__done = False
			self.__display_duration = self.TIMING_DEFAULT_DISPLAY_DURATION

		def set_text(self, text):
			self.__text = text
			self.__display_start_time_in_ms = time.time() * 1000
			self.__text_offset_index = 0
			self.__done = False
			self.__animate = len(self.__text) > self.CONFIG_DISPLAY_POSITIONS
			if self.__animate:
				self.__display_duration = self.TIMING_SCROLL_START_DISPLAY_DURATION
			else:
				self.__display_duration = self.TIMING_DEFAULT_DISPLAY_DURATION

		def has_content_to_display(self):
			return False if (len(self.__text) == 0 or self.__done is True) else True

		def get_display_text(self):
			delta = (time.time() * 1000) - self.__display_start_time_in_ms
			#print str("Wait Time: %f" % delta)
			if self.__animate and delta > self.__display_duration:
				self.__text_offset_index = int((delta-self.TIMING_SCROLL_START_DISPLAY_DURATION) / self.TIMING_SCROLL_SPEED_DELAY)
				if self.__text_offset_index > len(self.__text) - self.CONFIG_DISPLAY_POSITIONS:
					self.__text_offset_index = len(self.__text) - self.CONFIG_DISPLAY_POSITIONS
					self.__animate = False
					self.__display_start_time_in_ms = time.time() * 1000
					self.__display_duration = self.TIMING_SCROLL_END_DISPLAY_DURATION
			elif self.__animate is False and delta > self.__display_duration:
				self.__done = True
			#print str("> from %s (%i) => %s\x1b[K" % (self.__text, self.__text_offset_index, self.__text[self.__text_offset_index:self.__text_offset_index+self.CONFIG_DISPLAY_POSITIONS]))
			return self.__text[self.__text_offset_index:self.__text_offset_index+self.CONFIG_DISPLAY_POSITIONS]

	def __init__(self, c_instance):
		self.__c_instance = c_instance
		self.__text0 = self.TextElement()
		self.__text1 = self.TextElement()
		self.__last_display_content = "nOnE"

	def set_text_layer0(self, text0):
		self.__text0.set_text(text0)

	def set_text_layer1(self, text1):
		self.__text1.set_text(text1)

	def is_midi_out_msg_required(self, new_text):
		return True #self.__last_display_content != new_text

	def update_text_display(self, text):
		midi_messages = DisplayInfo.text_to_midi(text)
		for msg in midi_messages:
			self.__c_instance.send_midi(msg.as_bytes)

	def update_tick(self):
		if self.__text1.has_content_to_display():
			text = self.__text1.get_display_text()
			if self.is_midi_out_msg_required(text):
				self.update_text_display(text)
				self.__last_display_content = text
				#print str("Send Midi: True  ")
			#else:
				#print str("Send Midi: False")
			#print "\x1b[4A"
		elif self.__text0.has_content_to_display():
			text = self.__text0.get_display_text()
			if self.is_midi_out_msg_required(text):
				self.update_text_display(text)
				self.__last_display_content = text
				#print str("Send Midi: True  ")
			#else:
				#print str("Send Midi: False")
			#print "\x1b[4A"

"""
if __name__ == "__main__":
	disp = DisplayControl()
	disp.set_text_layer1("What's up dudes?")
	disp.set_text_layer0("OK")

	print "\x1b[2J"
	while True:
		disp.update_tick()
		time.sleep(0.025)
"""