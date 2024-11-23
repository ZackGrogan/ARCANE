# ARCANE Deployment Guide

## Prerequisites

### System Requirements
- Python 3.10 or higher
- MongoDB 4.4 or higher
- Nginx (recommended for production)
- Gunicorn
- Linux-based OS (recommended for production)

### Required Services
1. MongoDB Atlas or self-hosted MongoDB
2. Google Cloud Platform (for Gemini API)
3. FLUX API account

## Installation Steps

### 1. System Setup
```bash
# Update system packages
sudo apt update
sudo apt upgrade

# Install required system packages
sudo apt install python3-pip python3-venv nginx mongodb
```

### 2. Application Setup
```bash
# Create application directory
mkdir /opt/arcane
cd /opt/arcane

# Clone repository
git clone https://github.com/yourusername/arcane.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn
```

### 3. Environment Configuration
Create `.env` file in the application root:
```bash
# Database
MONGODB_URI=mongodb://[username:password@]host[:port]/database

# API Keys
GEMINI_API_KEY=your_gemini_api_key
FLUX_API_KEY=your_flux_api_key

# Flask Configuration
FLASK_ENV=production
FLASK_APP=main.py
SECRET_KEY=your_secret_key

# Server Configuration
HOST=0.0.0.0
PORT=8000
```

### 4. Database Setup
1. Create MongoDB database
2. Set up user accounts
3. Configure network access
4. Initialize collections

### 5. Gunicorn Setup
Create `/etc/systemd/system/arcane.service`:
```ini
[Unit]
Description=ARCANE Gunicorn Service
After=network.target

[Service]
User=arcane
Group=www-data
WorkingDirectory=/opt/arcane
Environment="PATH=/opt/arcane/venv/bin"
ExecStart=/opt/arcane/venv/bin/gunicorn --workers 3 --bind unix:arcane.sock -m 007 main:app

[Install]
WantedBy=multi-user.target
```

### 6. Nginx Configuration
Create `/etc/nginx/sites-available/arcane`:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location / {
        include proxy_params;
        proxy_pass http://unix:/opt/arcane/arcane.sock;
    }

    location /static {
        alias /opt/arcane/static;
    }
}
```

## Deployment Steps

### 1. Initialize Application
```bash
# Create database indexes
python manage.py init_db

# Collect static files
python manage.py collect_static
```

### 2. Start Services
```bash
# Start Gunicorn service
sudo systemctl start arcane
sudo systemctl enable arcane

# Start Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

### 3. SSL Configuration (Optional)
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Obtain SSL certificate
sudo certbot --nginx -d your_domain.com
```

## Monitoring and Maintenance

### Logging
- Application logs: `/var/log/arcane/app.log`
- Nginx access logs: `/var/log/nginx/access.log`
- Nginx error logs: `/var/log/nginx/error.log`

### Backup Strategy
1. Database Backup
```bash
# Daily MongoDB backup
mongodump --uri="$MONGODB_URI" --out=/backup/$(date +%Y%m%d)
```

2. Application Backup
```bash
# Backup application files
tar -czf /backup/arcane_$(date +%Y%m%d).tar.gz /opt/arcane
```

### Monitoring Tools
1. Server Monitoring
   - CPU usage
   - Memory usage
   - Disk space
   - Network traffic

2. Application Monitoring
   - API endpoint response times
   - Error rates
   - User sessions
   - Database performance

### Update Procedure
1. Pull latest changes
```bash
cd /opt/arcane
git pull origin main
```

2. Update dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

3. Restart services
```bash
sudo systemctl restart arcane
sudo systemctl restart nginx
```

## Troubleshooting

### Common Issues

1. **Application Not Starting**
- Check Gunicorn logs: `journalctl -u arcane`
- Verify environment variables
- Check file permissions

2. **Database Connection Issues**
- Verify MongoDB service status
- Check connection string
- Verify network connectivity

3. **API Service Errors**
- Validate API keys
- Check rate limits
- Verify service status

### Health Checks
```bash
# Check Gunicorn status
sudo systemctl status arcane

# Check Nginx status
sudo systemctl status nginx

# Test MongoDB connection
mongo $MONGODB_URI --eval "db.runCommand({ping:1})"
```

## Security Considerations

### Firewall Configuration
```bash
# Allow HTTP/HTTPS
sudo ufw allow 80
sudo ufw allow 443

# Allow SSH
sudo ufw allow 22
```

### File Permissions
```bash
# Set proper ownership
sudo chown -R arcane:www-data /opt/arcane

# Set proper permissions
sudo chmod -R 750 /opt/arcane
sudo chmod -R 660 /opt/arcane/logs
```

### Security Headers
Add to Nginx configuration:
```nginx
add_header X-Frame-Options "SAMEORIGIN";
add_header X-XSS-Protection "1; mode=block";
add_header X-Content-Type-Options "nosniff";
add_header Referrer-Policy "strict-origin-when-cross-origin";
```
