from marshmallow import ValidationError


class DataHandlerMixin:
    """Класс-миксин для обработки данных"""

    @staticmethod
    def _request_data_handler(json_data, serializer):
        """
        Метод для проверки и обработки данных запроса
        :param json_data: данные запроса
        :param serializer: сериализатор для обработки данных
        :return: если данные валидны, то возвращает сериализованные данные (dict),
        в противном случае - сообщение об ошибке и статус-код
        """
        if not json_data:
            return {'message': 'no input data provided'}, 400
        try:
            data = serializer.load(json_data)
            _ = None
            return data, _
        except ValidationError as err:
            return err.messages, 400

    @staticmethod
    def _check_data(permission_key=None, user_=None, **kwargs):
        """
        Метод для проверки наличия объекта(объектов) и прав доступа
        :param permission_key: ключ для идентификации объекта,
        к которому нужно проверить права доступа,
        если не указан, значит проверка пропускается
        :param user_: пользователь, запрашивающий доступ,
        если проверка прав доступа не требуется, то не указывается
        :param kwargs: проверяемые объекты (ключ=объект)
        :return: В случае успешной проверки возвращает None,
        в противном случае - сообщение об ошибке и статус-код
        """
        for key in kwargs:
            query_obj = kwargs[key]
            if not query_obj:
                return {'message': f'{key} not found'}, 404
        if permission_key:
            assert user_
            if not kwargs[permission_key].author_id == user_.id:
                return {'message': f'you cannot edit this {permission_key}'}, 403
