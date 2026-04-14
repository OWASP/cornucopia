FROM node:iron-alpine3.21@sha256:957dbf2afb4f22d9e2b94b981e242cbb796965cd3d9cc02d436e2a05fa0ec300 AS builder

# Context is now the repository root to allow copying the source folder.
WORKDIR /source
COPY source .

WORKDIR /app

# Install dependencies
# V15.2: Copy the lockfile before install so dependency resolution is deterministic
# and Docker can safely cache the dependency layer.
COPY cornucopia.owasp.org/package.json ./
COPY cornucopia.owasp.org/pnpm-lock.yaml ./
RUN npm install -g pnpm@v10.3.0 --save-exact
RUN pnpm install --frozen-lockfile

# Copy source code
COPY cornucopia.owasp.org .

# Build the application
ENV NODE_OPTIONS="--max-old-space-size=4096"
RUN pnpm run build

# Production stage
FROM nginx:alpine3.21@sha256:b471bb609adc83f73c2d95148cf1bd683408739a3c09c0afc666ea2af0037aef

# Copy the built assets from builder stage to nginx
COPY --from=builder /app/build /usr/share/nginx/html

# Copy custom Nginx configuration
COPY cornucopia.owasp.org/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

# Added a comment to push to repo webhook