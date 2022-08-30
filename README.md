# api_yamdb
api_yamdb


## Команда:
Михаил Выборный VM-94@yandex.ru
Андрей Пайгусов a.paigusov@yandex.ru
Алексей Радченко alexeyra@yandex.ru

## Поддерживаемые запросы
| Method | Endpoint |
| --- | --- |
| POST | /api/v1/auth/signup/ |
| POST | /api/v1/auth/token/ |
|     |     |
| GET | /api/v1/categories/ |
| POST | /api/v1/categories/ |
| DELETE | /api/v1/categories/{slug}/ |
|     |     |
| GET | /api/v1/genres/ |
| POST | /api/v1/genres/ |
| DELETE | /api/v1/genres/{slug}/ |
|     |     |
| POST | /api/v1/titles/ |
| GET | /api/v1/titles/{titles_id}/ |
| PATCH | /api/v1/titles/{titles_id}/ |
| DELETE | /api/v1/titles/{titles_id}/ |
|     |     |
| GET | /api/v1/titles/{title_id}/reviews/ |
| POST | /api/v1/titles/{title_id}/reviews/ |
| GET | /api/v1/titles/{title_id}/reviews/{review_id}/ |
| PATCH | /api/v1/titles/{title_id}/reviews/{review_id}/ |
| DELETE | /api/v1/titles/{title_id}/reviews/{review_id}/ |
|     |     |
| GET | /api/v1/titles/{title_id}/reviews/{review_id}/comments/ |
| POST | /api/v1/titles/{title_id}/reviews/{review_id}/comments/ |
| GET | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ |
| PATCH | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ |
| DELETE | /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/ |
|     |     |
| GET | /api/v1/users/ |
| POST | /api/v1/users/ |
| GET | /api/v1/users/{username}/ |
| PATCH | /api/v1/users/{username}/ |
| DELETE | /api/v1/users/{username}/ |


### POST /api/v1/auth/signup/
Получить код подтверждения на переданный email для регистрации нового пользователя
Права доступа: Доступно без токена.
Использовать имя 'me' в качестве username запрещено.
Поля email и username должны быть уникальными.

#### Формат ответа
```json
{
  "email": "string",
  "username": "string"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### POST /api/v1/auth/token/
Получение JWT-токена в обмен на username и confirmation code.

Права доступа: Доступно без токена.

#### Формат ответа
```json
{
  "token": "string"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/categories/
### GET /api/v1/categories/?search=slug

Получить список всех категорий

Права доступа: Доступно без токена

#### Формат ответа
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### POST /api/v1/categories/
Создать категорию.

Права доступа: Администратор.

Поле slug каждой категории должно быть уникальным.


#### Формат ответа
```json
{
  "name": "string",
  "slug": "string"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### DELETE /api/v1/categories/{slug}/
Удалить категорию.

Права доступа: Администратор.

#### Формат ответа
Status code 204
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/genres/
### GET /api/v1/genres/?search=slug
Получить список всех жанров.

Права доступа: Доступно без токена

#### Формат ответа
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "name": "string",
        "slug": "string"
      }
    ]
  }
]
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### POST /api/v1/genres/
Добавить жанр.

Права доступа: Администратор.

Поле slug каждого жанра должно быть уникальным.

#### Формат ответа
```json
{
  "name": "string",
  "slug": "string"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

## DELETE /api/v1/genres/{slug}/
Удалить жанр.

Права доступа: Администратор.


#### Формат ответа
Status code 204
[Вернуться к списку запросов](#поддерживаемые-запросы)

### POST /api/v1/titles/
Добавить новое произведение.

Права доступа: Администратор.

Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего).

При добавлении нового произведения требуется указать уже существующие категорию и жанр.


#### Формат ответа
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/titles/{titles_id}/
Информация о произведении

Права доступа: Доступно без токена


#### Формат ответа
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### PATCH /api/v1/titles/{titles_id}/
Обновить информацию о произведении

Права доступа: Администратор


#### Формат ответа
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "string"
    }
  ],
  "category": {
    "name": "string",
    "slug": "string"
  }
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### DELETE /api/v1/titles/{titles_id}/
Удалить произведение.

Права доступа: Администратор.


#### Формат ответа
Status code 204
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/titles/{title_id}/reviews/
Получить список всех отзывов.

Права доступа: Доступно без токена.


#### Формат ответа
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "score": 1,
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### POST /api/v1/titles/{title_id}/reviews/
Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение.

Права доступа: Аутентифицированные пользователи.


#### Формат ответа
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/titles/{title_id}/reviews/{review_id}/
Получить отзыв по id для указанного произведения.

Права доступа: Доступно без токена.


#### Формат ответа
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### PATCH /api/v1/titles/{title_id}/reviews/{review_id}/
Частично обновить отзыв по id.

Права доступа: Автор отзыва, модератор или администратор.

#### Формат ответа
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 1,
  "pub_date": "2019-08-24T14:15:22Z"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### DELETE /api/v1/titles/{title_id}/reviews/{review_id}/
Удалить отзыв по id

Права доступа: Автор отзыва, модератор или администратор.

#### Формат ответа
Status code 204
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/
Получить список всех комментариев к отзыву по id

Права доступа: Доступно без токена.

#### Формат ответа
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "id": 0,
        "text": "string",
        "author": "string",
        "pub_date": "2019-08-24T14:15:22Z"
      }
    ]
  }
]
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/
Добавить новый комментарий для отзыва.

Права доступа: Аутентифицированные пользователи.

#### Формат ответа
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Получить комментарий для отзыва по id.

Права доступа: Доступно без токена.

#### Формат ответа
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### PATCH /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Частично обновить комментарий к отзыву по id.

Права доступа: Автор комментария, модератор или администратор.

#### Формат ответа
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2019-08-24T14:15:22Z"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### DELETE /api/v1/titles/{title_id}/reviews/{review_id}/comments/{comment_id}/
Удалить комментарий к отзыву по id.

Права доступа: Автор комментария, модератор или администратор.

#### Формат ответа
Status code 204
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/users/
Получить список всех пользователей.

Права доступа: Администратор

#### Формат ответа
```json
[
  {
    "count": 0,
    "next": "string",
    "previous": "string",
    "results": [
      {
        "username": "string",
        "email": "user@example.com",
        "first_name": "string",
        "last_name": "string",
        "bio": "string",
        "role": "user"
      }
    ]
  }
]
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### POST /api/v1/users/
Добавить нового пользователя.

Права доступа: Администратор

Поля email и username должны быть уникальными.

#### Формат ответа
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### GET /api/v1/users/{username}/
Получить пользователя по username.

Права доступа: Администратор

#### Формат ответа
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### PATCH /api/v1/users/{username}/
Изменить данные пользователя по username.

Права доступа: Администратор.

Поля email и username должны быть уникальными.

#### Формат ответа
```json
{
  "username": "string",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
[Вернуться к списку запросов](#поддерживаемые-запросы)

### DELETE /api/v1/users/{username}/
Удалить пользователя по username.

Права доступа: Администратор.

#### Формат ответа
Status code 204
[Вернуться к списку запросов](#поддерживаемые-запросы)
