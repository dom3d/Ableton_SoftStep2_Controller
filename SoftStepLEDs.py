
class LEDInfo(object):
	"""Helper for the midi values dat drive the LEDs of the SoftStep board"""

	# Static Constants
	class Status:
		Off = 0
		On = 1
		FastFlash = 2
		SlowFlash = 3

	class CCs:
		Key1_Red = 20
		Key2_Red = 21
		Key3_Red = 22
		Key4_Red = 23
		Key5_Red = 24
		Key6_Red = 25
		Key7_Red = 26
		Key8_Red = 27
		Key9_Red = 28
		Key0_Red = 29
		
		Key1_Green = 110
		Key2_Green = 111
		Key3_Green = 112
		Key4_Green = 113
		Key5_Green = 114
		Key6_Green = 115
		Key7_Green = 116
		Key8_Green = 117
		Key9_Green = 118
		Key0_Green = 119
