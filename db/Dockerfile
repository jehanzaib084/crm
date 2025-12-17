# MongoDB Dockerfile
FROM mongo:7.0

# Copy initialization script
COPY init-mongo.js /docker-entrypoint-initdb.d/

# Create data directory
RUN mkdir -p /data/db

# Expose MongoDB port
EXPOSE 27017

# Set default command
CMD ["mongod"]
