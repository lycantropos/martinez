ARG PYTHON_IMAGE
ARG PYTHON_IMAGE_VERSION

FROM ${PYTHON_IMAGE}:${PYTHON_IMAGE_VERSION}

RUN python -m pip install --upgrade pip setuptools

WORKDIR /opt/martinez

COPY requirements.txt .
RUN python -m pip install --force-reinstall -r requirements.txt

COPY requirements-tests.txt .
RUN python -m pip install --force-reinstall -r requirements-tests.txt

COPY README.md .
COPY pytest.ini .
COPY setup.py .
COPY src src/
COPY martinez martinez/
COPY tests/ tests/

RUN python -m pip install -e .
