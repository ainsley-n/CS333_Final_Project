# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
# Since you mentioned you don't have a requirements.txt file, you can directly install the necessary dependencies here
RUN pip install coverage

# CMD specifies the command to run when the container starts
# Since you want to run the game when the container starts, you can specify the command to execute the game script
CMD ["python", "game.py"]

