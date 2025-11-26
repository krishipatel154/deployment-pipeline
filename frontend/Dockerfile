# 1. Choose a Python Base Image
FROM node:20-alpine

# 2. Set the working directory
WORKDIR /app

# 3. Copy requirements and install dependencies
COPY package*.json .
RUN npm install

# 4. Copy the rest of your application code
COPY . .

RUN npm run build 

EXPOSE 5173

CMD ["npm", "run", "preview"]