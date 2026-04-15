FROM node:22-alpine AS builder

# Recreate the repo structure so relative paths work
WORKDIR /repo

# Copy common frontend
COPY common/templates/frontend/ ./common/templates/frontend/

# Copy app frontend
COPY apps/mfe-example-app-1/frontend/package.json apps/mfe-example-app-1/frontend/package-lock.json* ./apps/mfe-example-app-1/frontend/

WORKDIR /repo/apps/mfe-example-app-1/frontend
RUN npm install

COPY apps/mfe-example-app-1/frontend/ ./
RUN npm run build

FROM nginx:alpine
COPY --from=builder /repo/apps/mfe-example-app-1/frontend/dist /usr/share/nginx/html
COPY apps/mfe-example-app-1/frontend/nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 5174
CMD ["nginx", "-g", "daemon off;"]
