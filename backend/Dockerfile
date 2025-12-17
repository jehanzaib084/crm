# Backend Dockerfile - Node.js/Express API
FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy application source
COPY . .

# Expose backend port
EXPOSE 8888

# Start the backend server
CMD ["node", "src/server.js"]
