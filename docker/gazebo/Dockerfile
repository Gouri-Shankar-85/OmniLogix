# Gazebo Harmonic Simulation Environment
FROM ros_core

# Use Bash Shell
SHELL ["/bin/bash", "-c"]

# Switch to Root User for Installation
USER root

# Install Required Tools
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    curl \
    lsb-release \
    gnupg && \
    rm -rf /var/lib/apt/lists/*

# Add Gazebo Harmonic Repository
RUN curl https://packages.osrfoundation.org/gazebo.gpg \
    --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] https://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

# Install Gazebo Harmonic
RUN apt update && \
    DEBIAN_FRONTEND=noninteractive apt install -y \
    gz-harmonic \
    ros-jazzy-ros-gz \
    mesa-utils \
    gstreamer1.0-tools \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev && \
    rm -rf /var/lib/apt/lists/*

# Gazebo Environment Setup
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc

# Add User To GPU Groups
RUN usermod -aG render,video omnilogix

# Switch Back to Non-Root User
USER omnilogix

# Default Startup
CMD ["sleep", "infinity"]