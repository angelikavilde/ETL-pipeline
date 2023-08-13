FROM python

COPY requirements.txt .
COPY extract.py .
COPY transform.py .
COPY clean_data.py .
COPY load.py .
COPY run_ETL.sh .

RUN mkdir data

RUN pip install -r requirements.txt

CMD bash run_ETL.sh
