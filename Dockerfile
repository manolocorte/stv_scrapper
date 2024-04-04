FROM python:3.10 as base
    WORKDIR /code 
    COPY ./src /code 

FROM base as requirements
    WORKDIR /code 
    COPY  ./src/requirements.txt .
    RUN pip3 install -r requirements.txt

FROM requirements as execution
    ENTRYPOINT ["bash"] 