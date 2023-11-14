FROM ros:noetic
# Set the working directory within the container
WORKDIR /fastapi

# Copy the application files into the container
COPY fastapi /fastapi

# Install application dependencies
RUN apt-get update 
RUN apt-get install -y python3 python3-pip 
RUN pip install uvicorn fastapi jinja2 python-multipart opencv-python 
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y 
RUN apt-get install ros-$(rosversion -d)-cv-bridge -y

# Expose the application port
EXPOSE 8080


