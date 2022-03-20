FROM python:3.9-slim-buster

RUN apt-get update \
  && apt-get install --yes --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /stuart
RUN useradd -ms /bin/bash stuart && chown -R stuart /stuart
USER stuart

COPY --chown=stuart:stuart requirements.txt /tmp/requirements.txt
RUN pip3 install --user -r /tmp/requirements.txt
# Install python build tools
RUN pip install --upgrade pip setuptools wheel

ENV PATH="/stuart/.local/bin:${PATH}"
ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 
RUN bash -c 'mkdir -p {landing,raw}'

COPY --chown=stuart:stuart ./src challenge/
COPY --chown=stuart:stuart tests tests
COPY --chown=stuart:stuart landing landing

# # RUN Unit tests
RUN python3 -m unittest discover -s tests

# # RUN Pipeline and print to stdout
ENTRYPOINT ["python3", "./challenge/main.py"]
