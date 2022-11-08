FROM python:3.10.8-slim
WORKDIR /app
RUN apt-get update -y
RUN apt-get install -y gcc g++ make wget python-tk libgl1 libglib2.0-0
ENV PYTHONPATH "${PYTHONPATH}:/app"
COPY ./requirements.txt /app/requirements.txt
COPY . /app
RUN pip install -r requirements.txt
RUN cd darknet && make && cd ..
RUN bash get-networks.sh
RUN mkdir -p temp_dir
EXPOSE 5000
CMD ["python", "app.py"]
