# Тестовое задание

### API приложения (доступно по ссылке: https://liis-test-job.herokuapp.com/)

#### Данный интерфейс предоставляет следующие возможности:

1. Прохождение регистрации.
2. Авторизация (тип Basic Auth).
3. Просмотр опубликованных постов (без авторизации).
4. Публикация постов и комментариев к постам (только с авторизацией).
5. Редактирование и удаление постов и комментариев (только для их авторов).

### User:

    Схема:
    {
        id: int
        email: string 
        username: string 
        password: string 
    }

###### Регистрация пользователя.

_Метод_ ___POST___ - `/api/v1/registration`

Входные данные:
    
    {
        "email": "string",
        "username": "string",
        "password": "string"
    }

Выходные данные:
    
    {
        "id": "int",
        "username": "string",
        "email": "string"
    }

### Post:

    Схема:
    { 
        id: int
        author_id: objectid
        title: string
        content: string
        publication_datetime: datatime
    }

###### Просмотр списка постов.

_Метод_ ___GET___ - `/api/v1/posts`

Выходные данные:

    [
        { 
            "id": "int",
            "author_id": "objectid",
            "title": "string",
            "content": "string",
            "publication_datetime": "datatime",
            "comments": []
        },
    ]

###### Создание поста.

_Метод_ ___POST___ - `/api/v1/posts`

Входные данные:

    {
        "title": "string",
        "content": "string"
    }

Выходные данные:

    { 
        "id": "int",
        "author_id": "objectid",
        "title": "string",
        "content": "string",
        "publication_datetime": "datatime",
        "comments": []
    }

###### Просмотр экземпляра поста.

_Метод_ ___GET___ - `/api/v1/posts/{post_id}`

Выходные данные:

    { 
        "id": "post_id",
        "author_id": "objectid",
        "title": "string",
        "content": "string",
        "publication_datetime": "datatime",
        "comments": []
    }

###### Изменение экземпляра поста.

_Метод_ ___PUT___ - `/api/v1/posts/{post_id}`

Входные данные:

    {
        "title": "string",
        "content": "string"
    }

Выходные данные:

    { 
        "id": "post_id",
        "author_id": "objectid",
        "title": "string",
        "content": "string",
        "publication_datetime": "datatime",
        "comments": []
    }

###### Частичное изменение экземпляра поста.

_Метод_ ___PATCH___ - `/api/v1/posts/{post_id}`

Входные данные:

    {
        "title": "string", *опционально
        "content": "string" *опционально
    }

Выходные данные:

    { 
        "id": "post_id",
        "author_id": "objectid",
        "title": "string",
        "content": "string",
        "publication_datetime": "datatime",
        "comments": []
    }

###### Удаление экземпляра поста.

_Метод_ ___DELETE___ - `/api/v1/posts/{post_id}`


### Comment:

    Схема:
    { 
        id: int
        post_id: objectid
        author_id: objectid
        title: string
        content: string
        publication_datetime: datatime
    }

###### Создание комментария под постом.

_Метод_ ___POST___ - `/api/v1/posts/{post_id}/comments`

Входные данные:

    {
        "title": "string",
        "content": "string"
    }

Выходные данные:

    { 
        "id": "int"
        "post_id": "post_id"
        "author_id": "objectid"
        "title": "string"
        "content": "string"
        "publication_datetime": "datatime"
    }

###### Изменение экземпляра комментария.

_Метод_ ___PUT___ - `/api/v1/posts/{post_id}/comments/{comment_id}`

Входные данные:

    {
        "title": "string",
        "content": "string"
    }

Выходные данные:

    { 
        "id": "int"
        "post_id": "post_id"
        "author_id": "comment_id"
        "title": "string"
        "content": "string"
        "publication_datetime": "datatime"
    }

###### Частичное изменение экземпляра комментария.

_Метод_ ___PATCH___ - `/api/v1/posts/{post_id}/comments/{comment_id}`

Входные данные:

    {
        "title": "string", *опционально
        "content": "string" *опционально
    }

Выходные данные:

    { 
        "id": "int"
        "post_id": "post_id"
        "author_id": "comment_id"
        "title": "string"
        "content": "string"
        "publication_datetime": "datatime"
    }

###### Удаление экземпляра комментария.

_Метод_ ___DELETE___ - `/api/v1/posts/{post_id}/comments/{comment_id}`