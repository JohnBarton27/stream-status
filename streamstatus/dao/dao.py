from abc import ABC, abstractmethod
import sqlite3 as sl


class Dao(ABC):

    db_name = 'stream_status.db'

    @abstractmethod
    def get_by_id(self, obj_id):
        pass

    @abstractmethod
    def create(self, obj):
        pass

    @staticmethod
    @abstractmethod
    def get_obj_from_result(result):
        pass

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
