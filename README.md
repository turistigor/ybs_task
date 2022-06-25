Yandex backend school вторая задача встепительного экзамена. Сервис сравнения цен.

Развернуть приложение на удаленном сервере:
    необходимо установить:
        - docker
        - docker-compose
    в директорию развертывания скачать https://github.com/turistigor/ybs_task/blob/main/docker-compose.yml
    выполнить команды:
        docker pull igorturist/ybs_task:0.1.0
        docker-compose up db&  # необходимо дождаться сообщения: "database ready to accept connections"
        docker-compose up migration
        docker-compose up web

Обновить и перезапустить приложение:
    docker-compose down
    docker pull igorturist/ybs_task:0.1.0
    docker-compose up db&  # необходимо дождаться сообщения: "database ready to accept connections"
    docker-compose up migration
    docker-compose up web

 Тесты:
    Протестровать со своей машины приложение, развернуте на удаленом сервере:
        скачать файл в любую удобную директорию https://github.com/turistigor/ybs_task/blob/main/docker-compose.yml
        docker pull igorturist/ybs_task:0.1.0
        docker compose up test_remote

    Запустить тесты на удаленном сервере, где развенуто приложение:
        cd <app_dir>
        docker-compose up web&
        docker compose up test