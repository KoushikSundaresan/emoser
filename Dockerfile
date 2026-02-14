FROM ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    python3 \
    python3-pip \
    python3-dev \
    openjdk-11-jdk \
    android-sdk \
    android-studio \
    wget \
    unzip \
    libffi-dev \
    libssl-dev \
    libjpeg-dev \
    zlib1g-dev

# Set up Android SDK environment variables
ENV ANDROID_SDK_ROOT=/usr/lib/android-sdk \
    ANDROID_HOME=/usr/lib/android-sdk \
    PATH=$PATH:/usr/lib/android-sdk/cmdline-tools/latest/bin:/usr/lib/android-sdk/platform-tools:/usr/lib/android-sdk/tools/bin

# Install Buildozer and dependencies
RUN pip install --upgrade pip && \
    pip install buildozer cython pyjnius kivy

# Set working directory
WORKDIR /app

# Copy the emoser app files
COPY . /app

# Build the APK
RUN buildozer android debug

# Output location
CMD cp bin/*.apk /output/ 2>/dev/null; echo "APK build process completed. Check /output directory."
