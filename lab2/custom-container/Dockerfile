FROM ubuntu
RUN apt-get update
RUN apt-get -y install python3
COPY helloinwk.py /helloinwk.py
RUN ["chmod", "+x", "/helloinwk.py"]
CMD ["/helloinwk.py"]
