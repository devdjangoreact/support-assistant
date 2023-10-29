# Build the React app first
FROM node:16 as build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm install

COPY . ./
# RUN npm run build

# Now serve the React app with Nginx
FROM nginx:alpine

# Set the default Nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy the build folder from the build image
COPY --from=build /app/build /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
