# Set the base image to Python 3.11
FROM python:3.11

# Set the working directory in the container
WORKDIR /HeadhunterBot

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the Python dependencies and requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire bot's code into the container
COPY . .

# Set environment variables for the HeadhunterBot log files and the database
ENV LOG_PATH=Logs/
ENV DB_PATH=HeadhunterBot.db

# Start the bot when the container starts
CMD ["python", "run.py"]
