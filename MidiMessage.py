
class MidiMsg(object):
	# Helper to deal with midi raw data encoding and decoding
	# Static Constants
	class Types:
		NoteOff = 8
		NoteOn = 9
		Aftertouch = 10
		ControlChange = 11
		CC = 11
		ProgramChange = 12
		ChannelPressure = 13
		PitchWheel = 14

	# class behaviour
	def __init__(self, msg_type=None, channel=None, data1=None, data2=None ):
		self.msg_type = msg_type
		self.channel = channel
		self.data1 = data1
		self.data2 = data2

	@classmethod
	def from_bytes(cls, three_bytes):
		return cls(
			# high nibble
			msg_type=((three_bytes[0] & 0xF0) >> 4),
			# low nibble
			channel=(three_bytes[0] & 0x0F),
			# other two bytes
			data1=three_bytes[1], data2=three_bytes[2]
		)

	@property
	def is_cc(self):
		return self.msg_type == MidiMsg.Types.CC

	@property
	def as_bytes(self):
		# bytearray not available, must be older python version
		return (
			((self.msg_type << 4) | (self.channel & 0x0F)),
			self.data1,
			self.data2)
