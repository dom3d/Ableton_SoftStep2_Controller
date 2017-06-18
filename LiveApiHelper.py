import Live


class QuickApi(object):

	def __init__(self, c_instance):
		self.__c_live_instance = c_instance
		self.tracks = Tracks(c_instance)
		self.scenes = Scene(c_instance)
		self.session_view = SessionView(c_instance)
		self.song = Song(c_instance)
		self.app = App(c_instance)
		self.clip_slots = ClipSlots(c_instance)


class Tracks(object):

	def __init__(self, c_instance):
		self.__c_instance = c_instance

	def is_master_selected(self):
		return not cmp(self.__c_instance.song().view.selected_track, self.__c_instance.song().master_track)

	def is_selected_recordable(self):
		if self.__c_instance.song().view.selected_track in self.__c_instance.song().visible_tracks:
			return True
		else:
			return False

	def get_clip_and_master_tracks(self):
		return list(self.__c_instance.song().visible_tracks) + [self.__c_instance.song().master_track]

	def get_all_tracks(self):
		return list(self.__c_instance.song().visible_tracks)\
			+ list(self.__c_instance.song().return_tracks)\
			+ [self.__c_instance.song().master_track]

	def get_selected_index(self):
		return list(self.get_all_tracks()).index(self.__c_instance.song().view.selected_track)

	def toggle_arming(self):
		track = self.__c_instance.song().view.selected_track
		if track.can_be_armed:
			track.arm = not track.arm
		return track.arm

	def disarm_all(self):
		for track in self.__c_instance.song().visible_tracks:
			track.arm = False

	def exclusive_arm(self):
		track = self.__c_instance.song().view.selected_track
		if track.can_be_armed:
			target_state = not track.arm
			self.disarm_all()
			track.arm = target_state
			return target_state
		else:
			return False

	def is_selected_armed(self):
		if self.__c_instance.song().view.selected_track in self.__c_instance.song().visible_tracks:
			return self.__c_instance.song().view.selected_track.arm
		else:
			return False

	def stop_selected(self):
		self.__c_instance.song().view.selected_track.stop_all_clips()

	def set_monitoring_to_auto(self):
		track = self.__c_instance.song().view.selected_track
		if track.current_monitoring_state != Live.Track.Track.monitoring_states.AUTO:
			track.current_monitoring_state = Live.Track.Track.monitoring_states.AUTO


class Scene(object):

	def __init__(self, c_instance):
		self.__c_instance = c_instance

	def get_selected_index(self):
		return list(self.__c_instance.song().scenes).index(self.__c_instance.song().view.selected_scene)

	def fire_selected(self):
		scene = self.__c_instance.song().view.selected_scene
		if scene:
			scene.fire()
			return True
		else:
			return False


class ClipSlots(object):

	def __init__(self, c_instance):
		self.__c_instance = c_instance

	def fire(self):
		clip_slot = self.__c_instance.song().view.highlighted_clip_slot
		if clip_slot:
			clip_slot.fire()
			return True
		else:
			return False

	def fire_legato(self):
		clip_slot = self.__c_instance.song().view.highlighted_clip_slot
		if clip_slot:
			clip_slot.fire(force_legato=True, launch_quantization=Live.Song.Quantization.q_no_q)
			return True
		else:
			return False

	def fire_or_stop(self):
		clip_slot = self.__c_instance.song().view.highlighted_clip_slot
		if clip_slot:
			if clip_slot.is_playing:
				clip_slot.stop()
				return False
			else:
				clip_slot.fire()
				return True

	def stop(self):
		clip_slot = self.__c_instance.song().view.highlighted_clip_slot
		clip_slot.stop()

	def is_selected_of_recordable_track(self):
		if self.__c_instance.song().view.selected_track in self.__c_instance.song().visible_tracks:
			return True
		else:
			return False

	def is_selected_recording(self):
		if self.is_selected_of_recordable_track():
			return self.__c_instance.song().view.highlighted_clip_slot.is_recording
		else:
			return False

	def is_selected_playing(self):
		if self.is_selected_of_recordable_track():
			return self.__c_instance.song().view.highlighted_clip_slot.is_playing
		else:
			return False

	def is_selected_triggered(self):
		if self.is_selected_of_recordable_track():
			return self.__c_instance.song().view.highlighted_clip_slot.is_triggered
		else:
			return False

	def is_selected_triggered_for_recording(self):
		# todo detect overdub mode
		if self.is_selected_of_recordable_track():
			return self.__c_instance.song().view.highlighted_clip_slot.is_triggered and not self.__c_instance.song().view.highlighted_clip_slot.has_clip
		else:
			return False

	def is_selected_triggered_for_playing(self):
		# todo detectr overdub mode
		if self.is_selected_of_recordable_track():
			return self.__c_instance.song().view.highlighted_clip_slot.is_triggered and self.__c_instance.song().view.highlighted_clip_slot.has_clip
		else:
			# todo handle master track, scene triggering
			return False

	def get_most_left_playing_clip(self):
		for track in self.__c_instance.song().visible_tracks:
			for clip_slot in track.clip_slots:
				if clip_slot.is_playing:
					return clip_slot.clip
		return None

	def get_most_left_playing_pos(self):
		clip = self.get_most_left_playing_clip()
		# todo clip position, but better to use listeners


class SessionView(object):

	def __init__(self, c_instance):
		self.__c_instance = c_instance
		self.__app = Live.Application.get_application()

	def go_left(self):
		self.__app.view.scroll_view(Live.Application.Application.View.NavDirection.left, 'Session', True)

	def go_right(self):
		self.__app.view.scroll_view(Live.Application.Application.View.NavDirection.right, 'Session', True)

	def go_up(self):
		self.__app.view.scroll_view(Live.Application.Application.View.NavDirection.up, 'Session', True)

	def go_down(self):
		self.__app.view.scroll_view(Live.Application.Application.View.NavDirection.down, 'Session', True)


class Song(object):

	def __init__(self, c_instance):
		self.__c_instance = c_instance

	def undo(self):
		__song = self.__c_instance.song()
		if __song.can_undo:
			__song.undo()

	def undo_or_redo_if_possible(self):
		__song = self.__c_instance.song()
		if __song.can_redo:
			__song.redo()
			return False
		else:
			__song.undo()
			return True

	def stop_all_clips(self):
		self.__c_instance.song().stop_all_clips()

	def stop(self):
		self.__c_instance.song().stop_playing()

	def tap_tempo(self):
		self.__c_instance.song().tap_tempo()
		return self.__c_instance.song().tempo

	def is_playing(self):
		return self.__c_instance.song().is_playing

	@property
	def beat_index(self):
		return self.__c_instance.song().get_current_beats_song_time().beats

class App(object):

	def __init__(self, c_instance):
		self.__c_instance = c_instance

	def get_live_app(self):
		return Live.Application.get_application()

	def show_status_message(self, text_line):
		self.__c_instance.show_message(text_line)


# Live.Song.Song.trigger_session_record()
# .master_track.mixer_device.crossfader.value
