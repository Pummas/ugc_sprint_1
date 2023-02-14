FROM python:3.10.10-slim as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONPATH="/opt/app:$PYTHONPATH"


COPY ./docker/entrypoint.sh ./docker/wait_for_services.py /opt/
RUN chmod +x /opt/entrypoint.sh

WORKDIR /opt/app

COPY ./requirements.txt ./requirements.dev.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements.dev.txt

COPY ./src ./

ENTRYPOINT ["/opt/entrypoint.sh"]
CMD ["python", "main.py"]
