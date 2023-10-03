FROM python:3.10.6


SHELL ["/bin/bash", "-c"]

# Переменные окружения
# Запрет на создание файлов кэша
ENV PYTHONDONTWRITEBYCODE 1 

# Сообщения с логами не буферизируются,
# а выводятся сразу в stdout
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip


# RUN apt update && apt -qy install gcc \
#     openssh-client flake8 locales vim


# Создёт пользователя dj_dev
# Выдёт права на директории /opt и /run
# 777 - сем разрешено все
RUN useradd -rms /bin/bash dj_dev && chmod 777 /opt /run

# Определяет рабочую директорию
WORKDIR /dj_dev

# Создаёт отдельную папку для работы
# chown - Меняет владельца директории
# Выдаёт права на чтение и запись
# 755 - все для владельца, остальным только чтение и выполнение
RUN mkdir /dj_dev/static && chown -R dj_dev:dj_dev /dj_dev && chmod 755 /dj_dev

# COPY - копирует локальные файлы проекта
# в директорию /dj_dev
# устанавливает владельца файлов
# Первая точка - локальная директория проекта
# Вторая точка - директория /dj_dev
COPY --chown=dj_dev:dj_dev . .

#Устанавливает зависимости из файла requirements.txt
RUN pip install -r requirements.txt

# Переходит на пользователя
USER dj_dev

# Запускает приложение
CMD ["python manage.py runserver"]