FROM python:3.10-slim

RUN pip install pymodbus==2.5.3

COPY plc.py /plc.py

EXPOSE 502

CMD ["python", "/plc.py"]
