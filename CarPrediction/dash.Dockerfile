FROM python:3.9-bookworm
    RUN pip3 install ipykernel
    RUN pip3 install dash
    RUN pip3 install pandas 
    RUN pip3 install seaborn
    RUN pip3 install numpy
    CMD tail -f /dev/null
