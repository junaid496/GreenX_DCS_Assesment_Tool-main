# Use official Node image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .
RUN npm run build
RUN npm install -g serve

# Start the React app
CMD ["serve", "-s", "build", "-l", "3000"]








