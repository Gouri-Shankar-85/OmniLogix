# PX4 SITL Environment
FROM gazebo_sim

# Use Bash Shell
SHELL ["/bin/bash", "-c"]

USER root

# PX4 Dependencies
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    python3-pip \
    python3-jinja2 \
    python3-empy \
    python3-toml \
    python3-numpy \
    python3-yaml \
    python3-setuptools \
    ninja-build \
    exiftool \
    zip \
    default-jre && \
    rm -rf /var/lib/apt/lists/*

USER omnilogix

# Default Startup
CMD ["sleep", "infinity"]