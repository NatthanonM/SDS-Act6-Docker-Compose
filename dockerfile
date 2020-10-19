FROM python:3.7

COPY . /root
WORKDIR /root
RUN pip install -r requirements.txt

EXPOSE 8000
CMD (./wait-for-it.sh db:3306 --strict -- echo database is up) && \
alembic upgrade head && \
uvicorn --host=0.0.0.0 --port=8000 --reload main:app