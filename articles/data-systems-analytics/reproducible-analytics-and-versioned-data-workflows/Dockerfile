FROM python:3.12-slim

WORKDIR /work
COPY . /work

RUN python --version

CMD ["python", "python/reproducible_workflow.py", "--group-by", "system"]
