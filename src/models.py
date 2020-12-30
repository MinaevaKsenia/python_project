from utils.database import db


class BaseModel:
    """ Базовая модель для работы с БД """

    # Название таблицы в БД
    table_name = None

    def __init__(self):
        self._connection = db.connection

    @property
    def connection(self):
        return self._connection

    def get_list_some_fields(self, received_fields_name, field_name, value):
        """ Возвращает список записей с некоторыми полями из таблицы по значению поля field_name"""

        params = ', '.join(received_fields_name)
        query = f"""
            SELECT {params} FROM {self.table_name} WHERE {field_name} = ?
        """
        values = (value, )
        result = self.connection.execute(query, values).fetchall()
        return [dict(row) for row in result] if result is not None else None

    def get_list_by_field(self, field_name, value):
        """ Возвращает список записей из таблицы по значению поля field_name"""

        query = f"""
            SELECT * FROM {self.table_name} WHERE {field_name} = ?
        """
        values = (value, )
        result = self.connection.execute(query, values).fetchall()
        return [dict(row) for row in result] if result is not None else None

    def get_by_id(self, id: int):
        """ Возвращает запись по её ID """
        query = f"""
            SELECT * FROM {self.table_name} WHERE id = ?
        """
        values = (id,)
        result = self.connection.execute(query, values).fetchone()
        return dict(result) if result is not None else None

    def get_by_field(self, field_name, value):
        """Возвращает запись по значению поля field_name"""
        query = f"""
            SELECT * FROM {self.table_name} WHERE {field_name} = ?
        """
        values = (value,)
        result = self.connection.execute(query, values).fetchone()
        return dict(result) if result is not None else None

    def create(self, attributes: dict):
        """ Создаёт запись в таблице """

        # Выбираем все поля из словаря
        field_names = attributes.keys()
        # Выбираем все значения из словаря
        # Сразу преобразуем в tuple для записи
        field_values = tuple(attributes.values())
        # Создаём шаблон со всеми названиями полей для SQL запроса
        keys_placeholder = ','.join(field_names)
        # Создаём шаблон ?,?,? по кол-ву значений полей для SQL запроса
        values_placeholder = ('?,' * len(field_values)).rstrip(',')
        query = f"""
            INSERT INTO {self.table_name} ({keys_placeholder}) 
            VALUES ({values_placeholder})
        """
        cursor = self.connection.execute(query, field_values)
        self.connection.commit()
        # Возвращаем ID последней добавленой записи
        return cursor.lastrowid

    def update(self, id, attributes: dict):
        """ Изменяет запись в таблице """
        fields = (''.join([k + ' = ?, ' for k, v in attributes.items()])).rstrip(', ')
        attributes['id'] = id
        values = tuple(attributes.values())
        query = f"""
            UPDATE {self.table_name} SET {fields} 
            WHERE id = ?
        """
        cursor = self.connection.execute(query, values)
        self.connection.commit()

    def delete(self, id: int):
        """ Удаляет запись в таблице """
        query = f"""
            DELETE FROM {self.table_name} WHERE id = ?
        """
        values = (id, )
        cursor = self.connection.execute(query, values)
        self.connection.commit()

    def get_total(self, received_fields_name, user_id):
        query = '''WITH T AS (
             SELECT id, summ as s
             FROM transactions
             WHERE type = 1 AND user_id = ?
             UNION 
             SELECT id, -summ as s
             FROM transactions
             WHERE type = 2 AND user_id = ?)
             SELECT count(*) as count, CAST(sum(s) AS FLOAT) as total
             FROM T'''
        values = (user_id, user_id, )
        cursor = self.connection.execute(query, values).fetchone()
        params = ', '.join(received_fields_name)
        query = f"""
            SELECT {params} FROM {self.table_name} WHERE user_id = ? ORDER BY date_time
        """
        values = (user_id, )
        result = self.connection.execute(query, values).fetchall()
        return {'data': [dict(row) for row in result] if result is not None else None, 'count': cursor['count'], 'total': cursor['total']}



class UserModel(BaseModel):
    table_name = 'users'

class CategoryModel(BaseModel):
    table_name = 'categories'

class TransactionModel(BaseModel):
    table_name = 'transactions'