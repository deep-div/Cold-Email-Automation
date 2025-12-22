# Use the official NGINX Alpine-based image as the base image (small, secure, production-ready)
FROM nginx:stable-alpine

# Remove the default NGINX configuration to avoid conflicts with custom configs
RUN rm /etc/nginx/conf.d/default.conf

# Copy all environment-specific NGINX configs (dev/prod) into the image as templates
COPY nginx/config /etc/nginx/templates

# Copy the startup shell script that selects the correct config at runtime
COPY nginx/entrypoint.sh /entrypoint.sh

# Make the entrypoint script executable by the container runtime
RUN chmod +x /entrypoint.sh
RUN sed -i 's/\r$//' /entrypoint.sh 

# Declare HTTP and HTTPS ports used by NGINX
EXPOSE 80 443

# Run the shell script first to prepare config before starting NGINX
ENTRYPOINT ["/entrypoint.sh"]

# Start NGINX in the foreground so Docker can track the process
CMD ["nginx", "-g", "daemon off;"]