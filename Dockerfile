FROM texlive/texlive:TL2020-historic

RUN apt-get install -y texlive-lang-cyrillic 
RUN apt-get update -y && apt-get install -y python3 python3-pip
#RUN pip install -r requirements.txt
#RUN pip3 install flask requests
RUN apt-get install -y python3-flask python3-requests
COPY . /app
WORKDIR /app
CMD ["python", "api.py"]