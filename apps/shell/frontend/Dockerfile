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

ARG VITE_API_URL=http://localhost:8000
ARG VITE_KEYCLOAK_URL=http://localhost:8080
ARG VITE_KEYCLOAK_REALM=mfe
ARG VITE_KEYCLOAK_CLIENT_ID=mfe-shell
ARG EXAMPLE1_REMOTE_URL=http://localhost:5174

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_KEYCLOAK_URL=$VITE_KEYCLOAK_URL
ENV VITE_KEYCLOAK_REALM=$VITE_KEYCLOAK_REALM
ENV VITE_KEYCLOAK_CLIENT_ID=$VITE_KEYCLOAK_CLIENT_ID
ENV EXAMPLE1_REMOTE_URL=$EXAMPLE1_REMOTE_URL

RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=builder /repo/apps/shell/frontend/dist /usr/share/nginx/html
COPY apps/shell/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]
