FROM python

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY data ./data/
COPY static ./static/
COPY templates ./templates/
COPY main.py .
COPY utils.py .

CMD flask run
