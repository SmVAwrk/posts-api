# Тестовое задание

### API приложения

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

Регистрация пользователя.

_Метод_ ___POST___ - `api/v1/registration`

    
    {
        "email": "string",
        "username": "string",
        "password": "string"
    }

### Post:

    Схема:
    { 
        id: int
        author_id: objectid
        title: string
        content: string
        publication_datetime: datatime
        comments: [objectid, ]
    }

Просмотр списка постов.

_Метод_ ___GET___ - `api/v1/posts`


    [{ 
        "id": "int",
        "author_id": "objectid",
        "title": "string",
        "content": "string",
        "publication_datetime": "datatime",
        "comments": []
    }]

Создание поста.

_Метод_ ___POST___ - `api/v1/posts`


    {
        "title": "string",
        "content": "string"
    }

Просмотр экземпляра поста.

_Метод_ ___GET___ - `api/v1/posts/{post_id}`


    { 
        "id": "post_id",
        "author_id": "objectid",
        "title": "string",
        "content": "string",
        "publication_datetime": "datatime",
        "comments": []
    }


Изменение экземпляра поста.

_Метод_ ___PUT___ - `api/v1/posts/{post_id}`


    {
        "title": "string",
        "content": "string"
    }

Частичное изменение экземпляра поста.

_Метод_ ___PATCH___ - `api/v1/posts/{post_id}`


    {
        "title": "string", *опционально
        "content": "string" *опционально
    }

Удаление экземпляра поста.

_Метод_ ___DELETE___ - `api/v1/posts/{post_id}`


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

Создание комментария под постом.

_Метод_ ___POST___ - `api/v1/posts/{post_id}/comments`

    {
        "title": "string",
        "content": "string"
    }


Изменение экземпляра комментария.

_Метод_ ___PUT___ - `api/v1/posts/{post_id}/comments/{comment_id}`

    {
        "title": "string",
        "content": "string"
    }

Частичное изменение экземпляра комментария.

_Метод_ ___PATCH___ - `api/v1/posts/{post_id}/comments/{comment_id}`


    {
        "title": "string", *опционально
        "content": "string" *опционально
    }

Удаление экземпляра комментария.

_Метод_ ___DELETE___ - `api/v1/posts/{post_id}/comments/{comment_id}`