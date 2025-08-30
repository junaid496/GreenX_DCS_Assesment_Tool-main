FROM node:18-alpine

# Working dir
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install --legacy-peer-deps

# Copy rest of the code
COPY . .

# Build React app
RUN npm run build

# Install serve globally to serve production build
RUN npm install -g serve

# Expose port
EXPOSE 3000

# Serve production build
CMD ["serve", "-s", "build", "-l", "3000"]


