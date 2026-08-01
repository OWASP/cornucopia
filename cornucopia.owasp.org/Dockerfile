FROM node:iron-alpine3.21@sha256:957dbf2afb4f22d9e2b94b981e242cbb796965cd3d9cc02d436e2a05fa0ec300 AS builder

WORKDIR /app

# Install dependencies (lockfile copied for deterministic builds)
COPY package.json pnpm-lock.yaml ./
RUN npm install -g pnpm@v10.3.0 --save-exact
RUN pnpm install --frozen-lockfile

# Copy source data needed for SvelteKit prerendering (card YAML files)
# The workflow copies the repo-root source/ directory into the build context
COPY source /source

# Copy the frontend application code
COPY . .

# Build the application
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN pnpm run build

# Production stage
FROM nginx:alpine3.21@sha256:b471bb609adc83f73c2d95148cf1bd683408739a3c09c0afc666ea2af0037aef

# Copy the built assets from builder stage to nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]