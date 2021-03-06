# HumanInside
Разработка проекта для хакатона

### Предустановка
Для того чтобы запустить сайт нужно склонировать репозиторий на свою машину и настроить виртуальное окружение.

#### Виртуальное окружение
Находясь внутри дирректории Django, нужно выполнить команду
```bash
$sourse virtenv/bin/activate
```

Если имеется окружение conda, то его, предварительно, нужно отключить
```bash
$conda deactivate
```
#### Скачивание библиотек
Прежде, чем перейти к запуску, необходимо скачать библиотеки, которые использовались при написании сайта. Все имена библиотек лежат в файле requirements.txt
```bash
$pip3 install requirements.txt
```

### Запуск сервера
Чтобы запустить сайт нужно выполнить скрипт
```bash
$python3 manage.py runserver
```

### Дополнительно
Скрипт с парсером имеет несколько флагов. Чтобы открыть help, нужно выполнить команду
```bash
$python3 manage.py parser -h
```
Также имеется срипт с мейком для рекомендаций. Чтобы открыть help, нужно выполнить команду
```bash
$python3 manage.py maker -h
```

Feel free to use!
