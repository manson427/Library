FROM python:3.10
WORKDIR /Library
COPY ./requirements.txt /Library/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /Library/requirements.txt
COPY ./app /Library/app
COPY ./alembic.ini /Library/alembic.ini
COPY ./settings.yml /Library/settings.yml
COPY ./main.py /Library/main.py
COPY ./test /Library/test
COPY ./pytest.ini /Library/pytest.ini