# # 1. Choose a Python Base Image
# FROM node:20-alpine

# # 2. Set the working directory
# WORKDIR /app

# # 3. Copy requirements and install dependencies
# COPY package*.json .
# RUN npm install

# # 4. Copy the rest of your application code
# COPY . .

# RUN npm run build 

# EXPOSE 5173

# CMD ["npm", "run", "preview"]

# --- Stage 1: Build React App ---
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json .
RUN npm install

COPY . .
RUN npm run build


# --- Stage 2: Serve with NGINX ---
FROM nginx:stable-alpine

# Copy React build from Stage 1
COPY --from=build /app/dist /usr/share/nginx/html

# Copy your Nginx config
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
