FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Copy the app.py and requirements.txt
COPY app.py app.py
COPY requirements.txt requirements.txt

# Install the requirements
RUN pip3 install -r requirements.txt

# Run the script
CMD ["python3", "-u", "app.py"]
