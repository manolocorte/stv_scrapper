FROM python:3.10 as base
    WORKDIR /code 
    COPY ./* /code 

FROM base as requirements
    WORKDIR /code 
    COPY  ../requirements.txt .
    RUN pip3 install -r requirements.txt

FROM requirements as execution
    ENTRYPOINT ["bash"] 