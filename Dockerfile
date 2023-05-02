FROM python@sha256:60469fac3d4c1c4781465b18f1a89d8dd2a01af9bb799d17836b972fcc463da9

WORKDIR /usr/src/app
RUN pip install requests xlsxwriter
COPY . .

ENTRYPOINT [ "python", "./cloudsploit-dedupe-csv.py" ]