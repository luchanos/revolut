FROM python:3.6.2
WORKDIR /
ADD . .
ENV SERVICE_TOKEN=a1f64cd8-69b9-493c-8587-7afc041efabe
RUN pip3 install --upgrade pip
RUN pip3 install setuptools-rust
RUN pip3 install -r requirements.txt
CMD ["python", "app.py", "0.0.0.0", "6000"]
