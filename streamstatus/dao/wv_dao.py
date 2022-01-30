from streamstatus.dao.dao import Dao


class WelcomeVideoDao(Dao):

    def get_by_id(self, app_id):
        pass

    def get_all(self):
        results = self._get_results('SELECT * FROM welcome_video;', ())

        welcome_videos = WelcomeVideoDao.get_objs_from_result(results)
        return welcome_videos

    def create(self, wv):
        self._update_database('INSERT INTO welcome_video (name, length, filepath) VALUES (?, ?, ?);',
                              (wv.name, wv.length, wv.filepath))

    @staticmethod
    def get_obj_from_result(result):
        from streamstatus.video import WelcomeVideo

        wv_name = result['name']
        wv_length = int(result['length'])
        wv_filepath = result['filepath']

        return WelcomeVideo(wv_name, wv_length, filepath=wv_filepath)
