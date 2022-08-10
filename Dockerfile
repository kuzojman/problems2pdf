FROM texlive/texlive:TL2020-historic

RUN apt-get update -y && apt-get install -y python3 python3-pip
RUN pip3 install flask
COPY . /app
WORKDIR /app
CMD ["python", "api.py"]