from MidiMessage import MidiMsg
import Logging


class DisplayInfo(object):
	"""Helper for the midi values dat drive the display of the SoftStep board"""

	# Static Constants
	PositionCCs = [50, 51, 52, 53]

	CharacterLookup = {
		"-": 12,
		" ": 18,
		"$": 36,
		"#": 37,

		"@": 40,
		"%": 41,
		"&": 42,
		"*": 43,

		"0": 48,
		"1": 49,
		"2": 50,
		"3": 51,
		"4": 52,
		"5": 53,
		"6": 54,
		"7": 55,
		"8": 56,
		"9": 57,

		"|": 58,
		"/": 59,
		"(": 60,
		"=": 61,
		")": 62,
		"?": 63,
		",": 64,

		'A': 65,
		"B": 66,
		"C": 67,
		"D": 68,
		"E": 69,
		"F": 70,
		"G": 71,
		"H": 72,
		"I": 73,
		"J": 74,
		"K": 75,
		"L": 76,
		"M": 77,
		"N": 78,
		"O": 79,
		"P": 80,
		"Q": 81,
		"R": 82,
		"S": 83,
		"T": 84,
		"U": 85,
		"V": 86,
		"W": 87,
		"X": 88,
		"Y": 89,
		"Z": 90,

		"[": 91,
		":": 92,
		"]": 93,
		"^": 94,
		"_": 95,
		"'": 96,

		'a': 97,
		"b": 98,
		"c": 99,
		"d": 100,
		"e": 101,
		"f": 102,
		"g": 103,
		"h": 104,
		"i": 105,
		"j": 106,
		"k": 107,
		"l": 108,
		"m": 109,
		"n": 110,
		"o": 111,
		"p": 112,
		"q": 113,
		"r": 114,
		"s": 115,
		"t": 116,
		"u": 117,
		"v": 118,
		"w": 119,
		"x": 120,
		"y": 121,
		"z": 122
	}

	@staticmethod
	def text_to_midi(text):
		# Logging.logline(str("display <- %s" % text))
		output = []

		end_pos = len(text)
		if end_pos > 4:
			end_pos = 4
		elif end_pos < 4:
			while end_pos < 4:
				text += " "
				end_pos = len(text)
		for index in range(0, end_pos):
			msg = MidiMsg(
				int(MidiMsg.Types.CC),
				10,
				int(DisplayInfo.PositionCCs[index]),
				int(DisplayInfo.CharacterLookup[text[index]]),
			)
			output.append(msg)
		return output


class DisplayControl(object):
	"""Helper for the midi values dat drive the display of the SoftStep board"""