Yandex backend school вторая задача встепительного экзамена. Сервис сравнения цен.

Развернуть приложение на удаленном сервере:
    скачать файл в директорию для развертывания https://github.com/turistigor/ybs_task/blob/main/docker-compose.yml
    docker pull igorturist/ybs_task:0.1.0
    docker-compose up web

Обновить и перезапустить приложение:
    docker pull igorturist/ybs_task:0.1.0
    docker-compose down
    docker-compose up web

 Тесты:
    Запустить тесты на своей машине, приложение развернуто на удаленом сервере:
        скачать файл в любую удобную директорию https://github.com/turistigor/ybs_task/blob/main/docker-compose.yml
        docker pull igorturist/ybs_task:0.1.0
        docker compose up test_remote

    Запустить тесты на удаленном сервере, где развенуто приложение:
        cd <app_dir>
        docker-compose up web&
        docker compose up test