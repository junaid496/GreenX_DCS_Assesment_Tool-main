FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies (legacy-peer-deps for old CRA)
RUN npm install --legacy-peer-deps

# Add missing dependencies explicitly
RUN npm install echarts --save
RUN npm install @babel/plugin-proposal-private-property-in-object --save-dev

# Copy rest of the code
COPY . .

# Optional: increase memory for buil
ENV NODE_OPTIONS=--max_old_space_size=4096

# Build React app
RUN npm run build

# Install serve globally to serve production build
RUN npm install -g serve

EXPOSE 3000

# Serve production build
CMD ["serve", "-s", "build", "-l", "3000"]




