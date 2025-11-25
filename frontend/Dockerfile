# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install --legacy-peer-deps

# Copy source code
COPY . .

# Build for web
RUN npm run build:web

# Production stage
FROM node:18-alpine

WORKDIR /app

# Install serve globally
RUN npm install -g serve

# Copy built files from builder
COPY --from=builder /app/web-build ./web-build

# Expose port (Railway will override with $PORT)
EXPOSE 3000

# Start command using Railway's PORT env var
CMD serve web-build -s -l ${PORT:-3000}

