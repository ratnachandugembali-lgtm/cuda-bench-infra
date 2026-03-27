FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    python3 \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

RUN apt-get update && apt-get install -y \
    libbenchmark-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pytest

WORKDIR /workspace

COPY . .

RUN mkdir -p build && cd build && cmake .. && make

CMD ["pytest", "tests/test_benchmarks.py", "-v"]