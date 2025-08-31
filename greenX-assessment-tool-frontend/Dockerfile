# Build stage
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ENV NODE_OPTIONS=--max-old-space-size=2048
RUN npm run build

# Production stage
FROM node:18-alpine
WORKDIR /app
COPY --from=build /app/build ./build
RUN npm install -g serve
CMD ["serve", "-s", "build", "-l", "3000"]









