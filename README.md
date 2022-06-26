# Сервис сравнения цен

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

**Для запуска тестов выполнить команды:**
1. развернуть приложение
2. выполнить команду:
```
docker compose up test
```
