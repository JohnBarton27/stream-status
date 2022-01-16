from streamstatus.dao.dao import Dao


class WelcomeVideoDao(Dao):

    def get_by_id(self, app_id):
        pass

    def get_all(self):
        results = self._get_results('SELECT * FROM welcome_video;', ())

        welcome_videos = WelcomeVideoDao.get_objs_from_result(results)
        return welcome_videos

    def create(self, wv):
        self._update_database('INSERT INTO welcome_video (filepath, length) VALUES (?, ?);',
                              (wv.name, wv.length))

    @staticmethod
    def get_obj_from_result(result):
        from streamstatus.video import WelcomeVideo

        wv_name = result['filepath']
        wv_length = int(result['length'])

        return WelcomeVideo(wv_name, wv_length)
