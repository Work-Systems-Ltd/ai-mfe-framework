FROM node:22-alpine AS builder

# Recreate the repo structure so relative paths work
WORKDIR /repo

# Copy common frontend and install its deps
COPY common/templates/frontend/ ./common/templates/frontend/
WORKDIR /repo/common/templates/frontend
RUN npm install

# Copy shell frontend
WORKDIR /repo/apps/shell/frontend
COPY apps/shell/frontend/package.json apps/shell/frontend/package-lock.json* ./
RUN npm install

COPY apps/shell/frontend/ ./
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /repo/apps/shell/frontend/dist /usr/share/nginx/html
COPY apps/shell/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]
