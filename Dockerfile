# Base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project files
COPY . .

# Set environment variables for Django
ENV DJANGO_SETTINGS_MODULE=financial_data.settings
ENV PYTHONUNBUFFERED=1

# Run migrations and start the Django server
CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]