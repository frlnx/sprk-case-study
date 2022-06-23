FROM python:3.9
COPY . /opt/app/acceptance_tests
WORKDIR /opt/app/acceptance_tests
RUN ["pip3", "install", "--no-cache-dir", "-U", "-r", "requirements.txt"]
CMD ["pytest"]