FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY scripts/entry.sh /entry.sh

COPY src/ ${LAMBDA_TASK_ROOT}/

RUN chmod +x /entry.sh 

ARG lambda_handler_env

ARG build

LABEL build=$build\
      image="lambda-core"


ENV PYTHONPATH="${PYTHONPATH}:${LAMBDA_TASK_ROOT}"

ENV lambda_handler=$lambda_handler_env

ENTRYPOINT /entry.sh $lambda_handler 