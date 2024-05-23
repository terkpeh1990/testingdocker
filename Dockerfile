# Use an official Python runtime as a parent image
# FROM python:3.10-slim
FROM --platform=linux/amd64 python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       libpq-dev \
       gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the container
COPY . /app/
# RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
# RUN echo "from authentication.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'lovia2020')" | python manage.py shell

# Expose port 8000 to allow outside connections
EXPOSE 4900

# Start the Django application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:4900", "erpproject.wsgi:application"]
