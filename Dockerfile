FROM ubuntu:22.04

WORKDIR /workspace

COPY . .

CMD ["sleep", "infinity"]
