# Сервис сравнения цен

## Развернуть и обновить

**Как развернуть приложение на сервере:**
1. установить:
    - docker
    - docker-compose
2. скопировать файл https://disk.yandex.ru/d/Hk_xBGLwUdHhcA в директорию развертывания
3. создать в директории развертывания файл .env с переменными окружениями в формате *name*=*value*:
    - POSTGRES_DB=*<database_name>*
    - POSTGRES_USER=*<database_user_name>*
    - POSTGRES_PASSWORD=*<database_user_password>*
    - DB_HOST=*<database_addres>* - контейнер ("db"), IP("127.0.0.1") или доменное имя(localhost), по умолчанию подразумевается значение "db".
    - WEB_HOST=*<tested_application_addres>* - контейнер с протоколом ("http://web"), IP или доменное имя; для проверки локально развернутого приложения используйте "http://web"
4. выполнить команды:
```
docker pull igorturist/ybs_task:latest
docker-compose up web
```

**Для обновления приложения выполнить команды:**
```
docker-compose down
docker pull igorturist/ybs_task:latest
docker-compose up web
```

## Разработка

**Для запуска тестов выполнить команды:**
1. развернуть приложение
2. выполнить команду:
```
docker compose up test
```
**Полезные команды:**
- local_clean удалить собранный python package
- local_sdist собрать python package
- local_install локально уствить python package
- docker_build собрать контейнер
- docker_clean удалить безымянные образы
- docker_rebuild docker_clean + docker_clean
- docker_run запустить контейнер на 80 порту
- docker_rerun docker_rebuild + docker_run
- docker_upload пересобрать и выложить контейнер на https://hub.docker.com/

**Реализация:**
- База данных: PostgreSQL
- Web-фреймворк: Django 4.0.5
- Связь Web-фреймворка и базы даных: psycopg2-binary 2.9.3
- Тесты: Django Tests
- Дополнительные библиотеки:
    - requests 2.28.0
    - django-bulk-update-or-create 0.3.0
