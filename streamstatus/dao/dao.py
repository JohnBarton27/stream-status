from abc import ABC, abstractmethod
import sqlite3 as sl


class Dao(ABC):

    db_name = 'stream_status.db'

    @abstractmethod
    def get_by_id(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def create(self, obj):
        pass

    @staticmethod
    @abstractmethod
    def get_obj_from_result(result):
        pass

    @classmethod
    def get_objs_from_result(cls, results: list):
        return [cls.get_obj_from_result(result) for result in results]

    @staticmethod
    def get_db_conn():
        return sl.connect(Dao.db_name)

    def _get_results(self, query: str, parameters: tuple):
        conn = self.__class__.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute(query, parameters)

            return cursor.fetchall()

    def _update_database(self, query: str, parameters: tuple):
        conn = self.__class__.get_db_conn()

        with conn:
            conn.row_factory = sl.Row
            cursor = conn.cursor()
            cursor.execute(query, parameters)
            conn.commit()
