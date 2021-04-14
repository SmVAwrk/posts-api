## API приложения для просмотра постов

(доступно по ссылке: https://api-posts-test.herokuapp.com/)

#### Данный интерфейс предоставляет следующие возможности:

1. Прохождение регистрации.
2. Аутентификация (тип Basic Auth).
3. Просмотр опубликованных постов (без аутентификации).
4. Публикация постов и комментариев к постам (только с аутентификацией).
5. Редактирование и удаление постов и комментариев (только для их авторов).

#### Стек технологий:

+ Ubuntu 20
+ Python 3.7
+ PostgreSQL 
+ Flask
+ Docker/Docker-compose

#### Установка и запуск:

1. Склонируйте репозиторий в требуемую директорию:

`git clone https://github.com/SmVAwrk/posts-api`

2. Перейдите в корневую папку.

3. Создайте образ и запустите контейнер БД в фоновом режиме:

`docker-compose up -d db`

4. Создайте образ и запустите контейнер приложения:

`docker-compose up app`

5. API доступно на localhost:8080.

#### Документация:

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
        publication_datetime: datetime
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
            "publication_datetime": "datetime",
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
        "publication_datetime": "datetime",
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
        "publication_datetime": "datetime",
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
        "publication_datetime": "datetime",
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
        "publication_datetime": "datetime",
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
        publication_datetime: datetime
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
        "publication_datetime": "datetime"
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
        "publication_datetime": "datetime"
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
        "publication_datetime": "datetime"
    }

###### Удаление экземпляра комментария.

_Метод_ ___DELETE___ - `/api/v1/posts/{post_id}/comments/{comment_id}`