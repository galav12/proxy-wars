# Use a Python image as the base for the backend
FROM python:3.9

# Set the working directory for the backend
WORKDIR /app

# Install Flask and other dependencies
COPY ./backend/requirements.txt /app/
RUN pip install --upgrade pip && pip install --no-deps -r requirements.txt

# Copy backend source code
COPY ./backend/src /app/

# Install Node.js for the React frontend
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Set the working directory for the frontend
WORKDIR /app/frontend

# Install frontend dependencies
COPY ./frontend/package.json ./frontend/package-lock.json /app/frontend/
RUN npm install

# Copy frontend source code
COPY ./frontend/src /app/frontend/src
COPY ./frontend/public /app/frontend/public

# Expose both backend (Flask) and frontend (React) ports
EXPOSE 5000 3000

# Command to run both Flask (backend) and React (frontend) in parallel
CMD npm start & python /app/controllers/app.py