FROM python:3.10-slim-buster



RUN pip install boto3 wmill windmill-api
COPY scripts/refresh-tokens.py /


CMD ["python3", "refresh-tokens.py"]