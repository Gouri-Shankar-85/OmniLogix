# Base ubuntu image
FROM ubuntu:24.04

# Use bash shell
SHELL ["/bin/bash", "-c"]

# Build arguments
ARG USERNAME=omnilogix
ARG USER_UID=1000
ARG USER_GID=${USER_UID}

# Locale + Timezone configuration
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    locales \
    tzdata && \
    locale-gen en_US en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 && \
    ln -fs /usr/share/zoneinfo/Asia/Kolkata /etc/localtime && \
    echo "Asia/Kolkata" > /etc/timezone && \
    rm -rf /var/lib/apt/lists/*

# Environment variables
ENV LANG=en_US.UTF-8
ENV LANGUAGE=en_US:en
ENV LC_ALL=en_US.UTF-8

# Python
ENV PYTHONUNBUFFERED=1

# Prevent pip cache bloat
ENV PIP_NO_CACHE_DIR=1

# Essential development packages
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    sudo \
    git \
    curl \
    wget \
    vim \
    nano \
    bash-completion \
    software-properties-common \
    ca-certificates \
    gnupg \
    lsb-release \
    build-essential \
    cmake \
    gdb \
    pkg-config \
    unzip \
    zip \
    tar \
    rsync \
    net-tools \
    iputils-ping \
    usbutils \
    mesa-utils \
    python3 \
    python3-pip \
    python3-venv \
    python3-dev \
    python3-setuptools && \
    rm -rf /var/lib/apt/lists/*

# ROS 2 Jazzy repository setup
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    curl \
    software-properties-common && \
    add-apt-repository universe && \
    export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}') && \
    curl -L -o /tmp/ros2-apt-source.deb \
    "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb" && \
    dpkg -i /tmp/ros2-apt-source.deb && \
    rm /tmp/ros2-apt-source.deb

# ROS 2 Jazzy installation
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    ros-jazzy-desktop \
    ros-dev-tools \
    python3-colcon-common-extensions \
    ros-jazzy-joint-state-publisher \
    ros-jazzy-joint-state-publisher-gui \
    ros-jazzy-xacro \
    ros-jazzy-ros2-control \
    ros-jazzy-ros2-controllers \
    ros-jazzy-controller-manager \
    ros-jazzy-gz-ros2-control && \
    rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN if getent passwd ${USER_UID} > /dev/null 2>&1; then \
        userdel --remove $(getent passwd ${USER_UID} | cut -d: -f1); \
    fi && \
    if getent group ${USER_GID} > /dev/null 2>&1; then \
        groupdel $(getent group ${USER_GID} | cut -d: -f1); \
    fi && \
    groupadd --gid ${USER_GID} ${USERNAME} && \
    useradd \
        --uid ${USER_UID} \
        --gid ${USER_GID} \
        --create-home \
        --shell /bin/bash \
        ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

# Switch to non-root user
USER ${USERNAME}

# User home directory
WORKDIR /home/${USERNAME}

# ROS environment setup
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# Shell configuration
RUN echo 'source /usr/share/bash-completion/bash_completion' >> ~/.bashrc && \
    echo 'export TERM=xterm-256color' >> ~/.bashrc && \
    echo 'alias ll="ls -alF"' >> ~/.bashrc && \
    echo 'alias la="ls -A"' >> ~/.bashrc && \
    echo 'alias l="ls -CF"' >> ~/.bashrc

# Default container startup
CMD ["sleep", "infinity"]