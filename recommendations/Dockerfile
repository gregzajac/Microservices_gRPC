FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get -y update
RUN python -m pip install --upgrade pip

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY recommendations/ /service/recommendations/

WORKDIR /service/recommendations
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
    --grpc_python_out=. ../protobufs/recommendations.proto

EXPOSE 50051
ENTRYPOINT ["python", "recommendations.py"]