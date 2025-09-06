FROM public.ecr.aws/lambda/python:3.11


COPY scripts/entry.sh /entry.sh

COPY requirements.txt .

COPY src/ ${LAMBDA_TASK_ROOT}/

RUN pip install -r requirements.txt

RUN chmod +x /entry.sh 
# Set as local for local testing or empty value for default handler
ARG lambda_handler_env

ARG build

LABEL build=$build\
      image="lambda-core"


ENV PYTHONPATH="${PYTHONPATH}:${LAMBDA_TASK_ROOT}"

ENV lambda_handler=$lambda_handler_env

ENTRYPOINT /entry.sh $lambda_handler 