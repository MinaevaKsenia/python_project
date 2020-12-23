from flask import jsonify


class Messages:
    MSG_NO_RIGHTS = {'message': 'У Вас нет прав доступа.'}
    MSG_REQ_FAILED = {'message': 'Не удалось выполнить запрос!'}
    MSG_NOT_CAT = {'message': 'Вы пока не создали ни одной категории.'}
    MSG_NOT_CAT_BY_ID = {'message': 'Категории с таким id не существует.'}
    MSG_EMPTY_FIELD = {'message':'Поле не заполнено!'}
    MSG_NOT_TR_BY_ID = {'message': 'Транзакции с таким id не существует.'}
    MSG_CAT_EXIST = {'message': 'Категория с таким именем уже существует!'}



message = Messages()

    
