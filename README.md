# VKinder

Аналог Tinder, использующий данные из VK. Позволяет искать людей, подходящих под условия, на основании информации о пользователе из VK:

- возраст
- пол
- город
- семейное положение
- наибольшее совпадение по общим группам 

## Входные данные:

Имя пользователя или его id в ВК, для которого мы ищем пару. Если информации недостаточно, дополнительно запрашивается у пользователя.

## Выходные данные:

JSON-файл с 10 объектами, где у каждого объекта перечислены топ-3 фотографии (Популярность определяется по количеству лайков и комментариев) и ссылка на аккаунт.

Выходные данные записываются в бд PostgreSQL
