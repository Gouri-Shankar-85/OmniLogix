# Micro XRCE DDS Agent
FROM ros_core

SHELL ["/bin/bash", "-c"]

USER root

# Dependencies
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    cmake \
    build-essential \
    git && \
    rm -rf /var/lib/apt/lists/*

# Clone Agent
WORKDIR /opt

RUN git clone -b v2.4.3 https://github.com/eProsima/Micro-XRCE-DDS-Agent.git

# Build Agent
WORKDIR /opt/Micro-XRCE-DDS-Agent

RUN mkdir build && \
    cd build && \
    cmake .. && \
    make -j$(nproc) && \
    make install && \
    ldconfig

USER omnilogix

# Default Startup
CMD ["MicroXRCEAgent", "udp4", "-p", "8888"]