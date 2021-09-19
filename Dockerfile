FROM python:3.6.2
WORKDIR /
ADD . .
RUN pip3 install --upgrade pip
RUN pip3 install setuptools-rust
RUN pip3 install -r requirements.txt
CMD ["python", "app.py", "0.0.0.0", "6000"]
