# Use the --platform flag to specify ARM64 architecture
FROM prefecthq/prefect:2.14-python3.9-kubernetes

COPY docker-requirements.txt .

RUN pip install -r docker-requirements.txt --trusted-host pypi.python.org --no-cache-dir
RUN mkdir /opt/prefect/flows

COPY parameterized_flow.py /opt/prefect/flows/parameterized_flow.py
