# Step 1: Build the React app
FROM node:20-alpine AS builder

# Set the API URL environment variable
ARG VITE_API_URL
ENV VITE_API_URL=$VITE_API_URL

# Set the working directory inside the container
WORKDIR /my-app

# Copy package.json and package-lock.json to the working directory
COPY package*.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Build the application
RUN npm run build


# Step 2: Serve the built app using nginx
FROM nginx:alpine

# Copy built files from the builder
COPY --from=builder /my-app/dist /usr/share/nginx/html

# Remove default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Add custom nginx config
COPY nginx.conf /etc/nginx/conf.d

# Expose port 5173
EXPOSE 5173

# Start nginx
CMD ["nginx", "-g", "daemon off;"]