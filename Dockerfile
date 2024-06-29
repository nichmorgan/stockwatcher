# Use the official Python 3.12 image as the base image
FROM python:3.12

# Set the working directory inside the container
WORKDIR /app

# Copy the poetry.lock and pyproject.toml files to the working directory
COPY poetry.lock pyproject.toml /app/

# Install Poetry
RUN pip install poetry

# Install project dependencies
RUN poetry install --no-dev

# Copy the rest of the application code to the working directory
COPY ./src /app

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Start the FastAPI application in production mode
CMD ["poetry", "run", "fastapi", "run", "main.py"]