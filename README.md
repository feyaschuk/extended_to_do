# extended_to_do
to-do list with advanced features
test
try new branch

```
localhost/api/users/ ---- POST создание пользователя и т.д. по типичным урлам джосера
```
```
localhost/api/auth/jwt/create/ ------ POST создание токена и т.д. по типичным урлам JWT
```
#### Загрузить тестовую дату ( из директории task_scheduler)
```
python manage.py load data db.json
```
```
http://127.0.0.1:8000/api/products/ ------ [GET, POST]
```
```
http://127.0.0.1:8000/api/products/<id>/ ------ [GET, PATCH, DELETE]
```
```
http://127.0.0.1:8000/api/shops/ ----------- [GET, POST]
```
```
http://127.0.0.1:8000/api/shops/<id>/ ------------- [GET, PATCH, DELETE]
```
```
http://127.0.0.1:8000/api/recipes/ ----------- [GET, POST]
```
```
http://127.0.0.1:8000/api/recipes/<id>/ ----------- [GET, PATCH, PUT, DELETE]
```
```
http://127.0.0.1:8000/api/recipes/<id>/shopping_cart/ ---------- добавление, удаление в шоплист рецепт [GET, DELETE], для авториз.пользователя
```
```
http://127.0.0.1:8000/api/products/<id>/shopping_cart/ ---------- добавление, удаление в шоплист продукт [GET, DELETE], для авториз.пользователя
```
```
http://127.0.0.1:8000/api/products/download_shopping_cart/-------------------[GET] обьединенный шоплист продукт
```
