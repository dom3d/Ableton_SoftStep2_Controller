import Live
from MidiMessage import MidiMsg
from LiveApiHelper import QuickApi
from SoftStepLEDs import LEDInfo
from SoftStepDisplay import DisplayInfo
from DisplayController import DisplayControl
import Logging

CC_CLIP_NAV_UP_DOWN = 60
CC_CLIP_NAV_LEFT_RIGHT = 61
CC_TAP = 80
CONTROLLER_CHANNEL = 3


class DomsSoftStep2Controller:

    __module__ = __name__
    __doc__ = 'Advanced Ableton controller for SoftStep2 by Dom'
    __name__ = "Dom's SoftStep2 Controller"

    def __init__(self, c_instance):
        # get live topics
        self.__c_instance = c_instance
        self.__c_instance.log_message("DomsSoftStep2ControllerLogginxyz::__init__")
        self.__qAPI = QuickApi(c_instance)
        self.__display_ctrl = DisplayControl(c_instance)
        self.__display_ctrl.set_text_layer0("Softstep2")
        # setup controller script properties
        # register for for callbacks
        self.song().add_is_playing_listener(self.__playing_status_changed)
        self.song().add_record_mode_listener(self.__recording_status_changed)
        self.song().add_visible_tracks_listener(self.__tracks_changed)
        self.song().add_current_song_time_listener(self.update_beat_time_display)
        # trigger initial controller hardware elements update
        self.__playing_status_changed()
        self.__recording_status_changed()
        self.__qAPI.app.show_status_message("SoftStep2 Controller loaded")

        # tmp
        self.__time_beats = -1

    def get_application(self):
        # returns a reference to the application that we are running in
        return Live.Application.get_application()

    def song(self):
        # returns a reference to the Live song instance that we do control
        return self.__c_instance.song()

    def disconnect(self):
        #Live -> Script Called right before we get disconnected from Live.
        self.song().remove_is_playing_listener(self.__playing_status_changed)
        self.song().remove_record_mode_listener(self.__recording_status_changed)
        self.song().remove_visible_tracks_listener(self.__tracks_changed)
        # todo, remove position changed listener
        # todo update remote display

    def connect_script_instances(self, instanciated_scripts):
        # Called by the Application as soon as all scripts are initialized. You can connect yourself to other running scripts here, as we do it connect the extension modules (MackieControlXTs).
        pass

    def suggest_input_port(self):
        # Live -> Script Live can ask the script for an input port name to find a suitable one.
        return str('SSCOM (Port 1)')

    def suggest_output_port(self):
        # Live -> Script Live can ask the script for an output port name to find a suitable one.
        return str('SSCOM (Port 1)')

    def suggest_map_mode(self, cc_no, channel):
        # Live -> Script Live can ask the script for a suitable mapping mode for a given CC.
        return Live.MidiMap.MapMode.absolute

    def can_lock_to_devices(self):
        return False

    def request_rebuild_midi_map(self):
        # Script -> Live When the internal MIDI controller has changed in a way that you need to rebuild the MIDI mappings, request a rebuild by calling this function This is processed as a request, to be sure that its not too often called, because  its time-critical.
        self.__c_instance.request_rebuild_midi_map()

    def send_midi(self, midi_event_bytes):
        # Script -> Live Use this function to send MIDI events through Live to the _real_ MIDI devices        that this script is assigned to.
        self.__c_instance.send_midi(midi_event_bytes)

    def refresh_state(self):
        # Live -> Script Send out MIDI to completely update the attached MIDI controller. Will be called when requested by the user, after for example having reconnected the MIDI cables...
        # reset all LEDs first
        for attr, value in LEDInfo.CCs.__dict__.iteritems():
            if not attr.startswith('__'):
                Logging.logline(str("Turning off %s %i" % (attr, value)))
                self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, value, LEDInfo.Status.Off).as_bytes)
        # now push the current state
        self.update_display()

    def update_display(self):
        # Live -> Script Aka on_timer. Called every 100 ms and should be used to update display relevant        parts of the controller
        self.update_LEDs()
        self.__display_ctrl.update_tick()

    def update_text_displayOLD(self, text):
        midi_messages = DisplayInfo.text_to_midi(text)
        for msg in midi_messages:
            self.send_midi(msg.as_bytes)

    def update_beat_time_display(self):
        if self.__qAPI.song.is_playing():
            beat = self.__qAPI.song.beat_index
            if self.__time_beats != beat:
                self.__time_beats = beat
                #self.update_text_display(str("b %i" % beat))
                tag = "b"
                if self.__qAPI.clip_slots.is_selected_recording():
                    tag = "R"
                elif self.__qAPI.clip_slots.is_selected_playing():
                    tag = "P"
                elif self.__qAPI.clip_slots.is_selected_triggered():
                    tag = "t"
                self.__display_ctrl.set_text_layer0(str("%s %i" % (tag, beat)))
                self.__display_ctrl.update_tick()

    def update_clip_playback_display_info(self):
        pass

    def display_show_session_view_pos(self):
        x = self.__qAPI.tracks.get_selected_index() + 1
        y = self.__qAPI.scenes.get_selected_index() + 1
        if self.__qAPI.tracks.is_master_selected():
            text = str("M_%i" % y)
        else:
            text = str("%i_%i" % (x, y))
        #self.update_text_display(text)
        self.__display_ctrl.set_text_layer1(text)

    def update_LEDs(self):

        # armed status
        armed_status = LEDInfo.Status.Off
        if self.__qAPI.tracks.is_selected_armed():
            armed_status = LEDInfo.Status.On
        msg = MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key2_Red, armed_status)
        self.send_midi(msg.as_bytes)

        # fire key status
        green_status = LEDInfo.Status.Off
        if self.__qAPI.clip_slots.is_selected_triggered_for_playing():
            green_status = LEDInfo.Status.SlowFlash
        elif self.__qAPI.clip_slots.is_selected_playing():
            green_status = LEDInfo.Status.On
        else:
            green_status = LEDInfo.Status.Off

        red_status = LEDInfo.Status.Off
        if self.__qAPI.clip_slots.is_selected_triggered_for_recording():
            red_status = LEDInfo.Status.SlowFlash
            green_status = LEDInfo.Status.Off
        elif self.__qAPI.clip_slots.is_selected_recording():
            green_status = LEDInfo.Status.Off
            red_status = LEDInfo.Status.On
        else:
            red_status = LEDInfo.Status.Off
        # HW bug workaround: somehow keeps the light on due to display messages being send to the HW
        self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key1_Green, LEDInfo.Status.On).as_bytes)
        #self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key1_Green, LEDInfo.Status.On).as_bytes)
        # normal intended behabiour
        self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key1_Green, green_status).as_bytes)
        self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key1_Red, red_status).as_bytes)

        # turn undo / redo off
        self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key6_Red, LEDInfo.Status.Off).as_bytes)
        self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key6_Green, LEDInfo.Status.Off).as_bytes)

    def build_midi_map(self, midi_map_handle):
        # Live -> Script Build DeviceParameter Mappings, that are processed in Audio time, or forward MIDI messages explicitly to our receive_midi_functions. Which means that when you are not forwarding MIDI, nor mapping parameters, you will never get any MIDI messages at all.
        script_handle = self.__c_instance.handle()
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, CC_CLIP_NAV_UP_DOWN)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, CC_CLIP_NAV_LEFT_RIGHT)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 110)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 21)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 22)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 80)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 118)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 120)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 121)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 122)
        Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, CONTROLLER_CHANNEL, 125)
        """
        for channel in range(0, 15):
            for cc_id in range(0, 127):
                Live.MidiMap.forward_midi_cc(script_handle, midi_map_handle, channel, cc_id)
        self.__c_instance.show_message("build midi map5")
        """

    def receive_midi(self, midi_bytes):
        # Live -> Script MIDI messages are only received through this function, when explicitly forwarded in 'build_midi_map'.
        #self.__c_instance.show_message("received midi data")
        msg = MidiMsg.from_bytes(midi_bytes)
        if msg.msg_type == MidiMsg.Types.CC and msg.channel == CONTROLLER_CHANNEL:
            self.__qAPI.app.show_status_message(str("CC: %i" % msg.data1))
            if msg.data1 == 21 and msg.data2 > 0:
                armed = self.__qAPI.tracks.exclusive_arm()
                if armed:
                    #self.update_text_display("ARM")
                    self.__display_ctrl.set_text_layer1("ARM")
                else:
                    #self.update_text_display(" XX ")
                    self.__display_ctrl.set_text_layer1("disARMed")
                self.__qAPI.tracks.set_monitoring_to_auto()
            elif msg.data1 == 22 and msg.data2 > 0:
                armed = self.__qAPI.tracks.toggle_arming()
                if armed:
                    #self.update_text_display("ARM")
                    self.__display_ctrl.set_text_layer1("ARM")
                else:
                    self.display_show_session_view_pos()
                self.__qAPI.tracks.set_monitoring_to_auto()
            elif msg.data1 == CC_CLIP_NAV_LEFT_RIGHT:
                if msg.data2 > 90:
                    self.__qAPI.session_view.go_right()
                    self.display_show_session_view_pos()
                elif msg.data2 < 34:
                    self.__qAPI.session_view.go_left()
                    self.display_show_session_view_pos()
            elif msg.data1 == CC_CLIP_NAV_UP_DOWN:
                if msg.data2 > 93:
                    self.__qAPI.session_view.go_up()
                    self.display_show_session_view_pos()
                elif msg.data2 < 34:
                    self.__qAPI.session_view.go_down()
                    self.display_show_session_view_pos()
            elif msg.data1 == 110 and msg.data2 > 0:
                if self.__qAPI.tracks.is_master_selected():
                    self.__qAPI.scenes.fire_selected()
                    #self.update_text_display("FIRE")
                    #self.__display_ctrl.set_text_layer1("FIRE")
                else:
                    fired = self.__qAPI.clip_slots.fire_or_stop()
                    if fired:
                        #self.update_text_display("FIRE")
                        #self.__display_ctrl.set_text_layer1("FIRE")
                        pass
                    else:
                        #self.update_text_display("STOP")
                        #self.__display_ctrl.set_text_layer1("STOP")
                        pass
            elif msg.data1 == 80 and msg.data2 > 0:
                tempo = self.__qAPI.song.tap_tempo()
                self.__display_ctrl.set_text_layer1(str("t%i" % tempo))
            elif msg.data1 == 118 and msg.data2 > 0:
                undo = self.__qAPI.song.undo_or_redo_if_possible()
                if undo:
                    self.__display_ctrl.set_text_layer1("UNDO")
                    self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key6_Red, LEDInfo.Status.On).as_bytes)
                else:
                    self.__display_ctrl.set_text_layer1("REDO")
                    self.send_midi(MidiMsg(MidiMsg.Types.CC, 10, LEDInfo.CCs.Key6_Green, LEDInfo.Status.On).as_bytes)
            elif msg.data1 == 120 and msg.data2 > 0:
                self.__qAPI.clip_slots.stop()
                self.__display_ctrl.set_text_layer1("stop clips")
            elif msg.data1 == 121 and msg.data2 > 0:
                self.__qAPI.song.stop_all_clips()
                self.__display_ctrl.set_text_layer1("stop all clips")
            elif msg.data1 == 122 and msg.data2 > 0:
                self.__qAPI.song.stop()
                self.__display_ctrl.set_text_layer1("STOP Song")

    def __playing_status_changed(self):
        # Update the LED accordingly
        # if self.song().is_playing:
        # self.send_midi((status, note, value))
        self.update_display()
        pass

    def __recording_status_changed(self):
        #  Update the LED accordingly
        #if self.song().record_mode:
        # self.send_midi((status, note, value))
        self.update_display()
        pass

    def __tracks_changed(self):
        # self.request_rebuild_midi_map()
        pass

    # todos

    # todo: move up to track select and move back down from track selection

    # rewind
    # self.song().record_mode = not self.song().record_mode
    # self.song().is_playing = True
    # track.mute = not track.mute