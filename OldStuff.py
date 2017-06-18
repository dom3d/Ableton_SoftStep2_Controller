"""
   def __move_clip_selection_up(self):
        index = self.get_selected_scene_index()
        if index > 0:
            index -= 1
            self.song().view.selected_scene = self.song().scenes[index]
        #elif index == 0:

    def __move_clip_selection_down(self):
        index = self.get_selected_scene_index()
        if index < len(self.song().scenes) - 1:
            index += 1
            self.song().view.selected_scene = self.song().scenes[index]
            index2 = list(self.song().tracks).index(self.song().view.selected_track)
            self.__c_instance.show_message("track %s" % index2)

    def __move_clip_selection_left(self):
        selected_track = self.song().view.selected_track
        all_tracks = self.get_all_navigateable_tacks()
        if selected_track != all_tracks[0]:
            index = list(all_tracks).index(selected_track)
            self.song().view.selected_track = all_tracks[index - 1]

    def __move_clip_selection_right(self):
        selected_track = self.song().view.selected_track
        all_tracks = self.get_all_navigateable_tacks()
        if selected_track != all_tracks[-1]:
            index = list(all_tracks).index(selected_track)
            self.song().view.selected_track = all_tracks[index + 1]
        self.update_clip_highlight()

    def __move_clip_selection_left_old(self):
        if self.is_master_track_selected():
            self.__c_instance.show_message("is master track")
            self.song().view.selected_track = self.song().tracks[len(self.song().tracks) - 1]
            self.__c_instance.show_message("selected was master")
        else:
            index = list(self.song().tracks).index(self.song().view.selected_track)
            if index > 0:
                index -= 1
                self.song().view.selected_track = self.song().tracks[index]

    def __move_clip_selection_right_old(self):
        if self.is_master_track_selected():
            self.__c_instance.show_message("is already master")
            pass
        else:
            index = list(self.song().tracks).index(self.song().view.selected_track)
            if index < len(self.song().tracks) - 1:
                index += 1
                self.song().view.selected_track = self.song().tracks[index]
            else:
                self.__c_instance.show_message("selecting master track ...")
                self.song().view.selected_track = self.song().master_track
                self.__c_instance.show_message("selected is now master")

"""