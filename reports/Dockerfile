FROM amazon/aws-lambda-python

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY aws_lambda.py .
COPY connections.py .
COPY previous_day_report.py .

CMD [ "aws_lambda.lambda_handler" ]
