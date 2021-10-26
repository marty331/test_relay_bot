FROM python:3.8.5-slim-buster as builder
RUN apt-get update \
    && apt-get -y install build-essential libpcre3-dev libssl-dev \
    && apt-get clean
COPY requirements.txt /build/
WORKDIR /build/
RUN pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host sede-pt-ssw.pkgs.visualstudio.com
RUN pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org --trusted-host sede-pt-ssw.pkgs.visualstudio.com

FROM python:3.8.5-slim-buster as app
WORKDIR /app/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/ /usr/local/lib/
COPY *.py /app/
COPY uwsgi.ini /app/
ENTRYPOINT uwsgi --ini uwsgi.ini --http :$PORT