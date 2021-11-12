from streamstatus.dao.dao import Dao


class ApplicationDao(Dao):

    def get_by_id(self, app_id):
        results = self._get_results('SELECT * FROM application WHERE id=?;', (str(app_id),))

        application = ApplicationDao.get_obj_from_result(dict(results[0]))
        return application

    def get_all(self):
        results = self._get_results('SELECT * FROM application;', ())

        applications = ApplicationDao.get_objs_from_result(results)
        return applications

    def create(self, app):
        self._update_database('INSERT INTO application (hostname, port, name) VALUES (?, ?, ?);',
                              (app.hostname, app.port, app.app_name))

    @staticmethod
    def get_obj_from_result(result):
        from streamstatus.application import Application

        app_id = result['id']
        app_hostname = result['hostname']
        app_port = int(result['port'])
        app_name = result['name']

        return Application(app_hostname, app_port, app_name=app_name, db_id=app_id)
