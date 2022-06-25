Yandex backend school вторая задача встепительного экзамена. Сервис сравнения цен.

Как развернуть приложение на удаленном сервере:
    установить:
        - docker
        - docker-compose
    скопировать файлы:
        https://disk.yandex.ru/d/qCBmMwC0PXsYog в /etc/systems/system
        https://disk.yandex.ru/d/Hk_xBGLwUdHhcA в директорию развертывания
    выполнить команды:
        docker pull igorturist/ybs_task:0.1.0
        docker-compose up db&  # необходимо дождаться сообщения: "database ready to accept connections"
        docker-compose up migration
        docker-compose up web

Для обновления приложения выполнить команды:
    docker-compose down
    docker pull igorturist/ybs_task:0.1.0
    docker-compose up db&  # необходимо дождаться сообщения: "database ready to accept connections"
    docker-compose up migration
    docker-compose up web

Для запуска тестов выполнить команды:
    развернуть приложение
    docker-compose up web&
    docker compose up test