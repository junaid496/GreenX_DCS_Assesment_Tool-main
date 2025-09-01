# Build stage
FROM node:19.5.0-alpine 
WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

# Increase Node.js memory limit (4GB here, adjust if needed)
RUN NODE_OPTIONS="--max-old-space-size=4096" npm run build

RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]









