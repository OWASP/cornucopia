FROM node:iron-alpine3.21@sha256:957dbf2afb4f22d9e2b94b981e242cbb796965cd3d9cc02d436e2a05fa0ec300 AS builder

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install -g pnpm
RUN pnpm install

# Copy source code
COPY . .

# Build the application
RUN pnpm run build

# Production stage
FROM nginx:alpine3.21@sha256:b471bb609adc83f73c2d95148cf1bd683408739a3c09c0afc666ea2af0037aef

# Copy the built assets from builder stage to nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# Added a comment to push to repo webhook