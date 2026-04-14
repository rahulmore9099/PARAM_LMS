# Smart LMS - Deployment Guide

## 🚀 Production Deployment

This guide covers deploying Smart LMS to production environments.

## Prerequisites

- Python 3.8+
- PostgreSQL 12+
- Redis 6+
- Nginx
- Domain name with SSL certificate
- AWS account (for S3 storage - optional)

## Step 1: Server Setup

### Update System
```bash
sudo apt update
sudo apt upgrade -y
```

### Install Dependencies
```bash
sudo apt install python3-pip python3-venv postgresql postgresql-contrib nginx redis-server -y
```

### Install PostgreSQL
```bash
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

## Step 2: Database Setup

### Create Database
```bash
sudo -u postgres psql

CREATE DATABASE smart_lms_db;
CREATE USER smart_lms_user WITH PASSWORD 'your_secure_password';
ALTER ROLE smart_lms_user SET client_encoding TO 'utf8';
ALTER ROLE smart_lms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE smart_lms_user SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE smart_lms_db TO smart_lms_user;
\q
```

## Step 3: Application Setup

### Create Application Directory
```bash
sudo mkdir -p /var/www/smart_lms
sudo chown $USER:$USER /var/www/smart_lms
cd /var/www/smart_lms
```

### Clone Repository
```bash
git clone <your-repository-url> .
```

### Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
pip install gunicorn
```

### Configure Environment
```bash
cp .env.example .env
nano .env
```

Update `.env` with production values:
```env
SECRET_KEY=your-very-secure-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_NAME=smart_lms_db
DB_USER=smart_lms_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# AWS S3 (Optional)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1
```

### Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Set Permissions
```bash
sudo chown -R www-data:www-data /var/www/smart_lms
sudo chmod -R 755 /var/www/smart_lms
```

## Step 4: Gunicorn Setup

### Create Gunicorn Socket
```bash
sudo nano /etc/systemd/system/gunicorn.socket
```

Add:
```ini
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

### Create Gunicorn Service
```bash
sudo nano /etc/systemd/system/gunicorn.service
```

Add:
```ini
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/smart_lms
ExecStart=/var/www/smart_lms/venv/bin/gunicorn \
          --access-logfile - \
          --workers 3 \
          --bind unix:/run/gunicorn.sock \
          smart_lms.wsgi:application

[Install]
WantedBy=multi-user.target
```

### Start Gunicorn
```bash
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
```

## Step 5: Nginx Configuration

### Create Nginx Config
```bash
sudo nano /etc/nginx/sites-available/smart_lms
```

Add:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 100M;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        alias /var/www/smart_lms/staticfiles/;
    }

    location /media/ {
        alias /var/www/smart_lms/media/;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

### Enable Site
```bash
sudo ln -s /etc/nginx/sites-available/smart_lms /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## Step 6: SSL Certificate (Let's Encrypt)

### Install Certbot
```bash
sudo apt install certbot python3-certbot-nginx -y
```

### Obtain Certificate
```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Auto-Renewal
```bash
sudo systemctl status certbot.timer
```

## Step 7: Redis Configuration

### Start Redis
```bash
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### Test Redis
```bash
redis-cli ping
# Should return: PONG
```

## Step 8: Daphne for WebSockets (Optional)

### Install Daphne
```bash
pip install daphne
```

### Create Daphne Service
```bash
sudo nano /etc/systemd/system/daphne.service
```

Add:
```ini
[Unit]
Description=daphne daemon
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/smart_lms
ExecStart=/var/www/smart_lms/venv/bin/daphne \
          -b 0.0.0.0 \
          -p 8001 \
          smart_lms.asgi:application

[Install]
WantedBy=multi-user.target
```

### Start Daphne
```bash
sudo systemctl start daphne
sudo systemctl enable daphne
```

### Update Nginx for WebSockets
Add to Nginx config:
```nginx
location /ws/ {
    proxy_pass http://localhost:8001;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_redirect off;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Host $server_name;
}
```

## Step 9: Monitoring & Logging

### Setup Log Directory
```bash
sudo mkdir -p /var/log/smart_lms
sudo chown www-data:www-data /var/log/smart_lms
```

### Configure Django Logging
Add to `settings.py`:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/smart_lms/django.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
```

## Step 10: Backup Strategy

### Database Backup Script
```bash
sudo nano /usr/local/bin/backup_smart_lms.sh
```

Add:
```bash
#!/bin/bash
BACKUP_DIR="/var/backups/smart_lms"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U smart_lms_user smart_lms_db > $BACKUP_DIR/db_$DATE.sql

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/smart_lms/media/

# Keep only last 7 days
find $BACKUP_DIR -type f -mtime +7 -delete
```

### Make Executable
```bash
sudo chmod +x /usr/local/bin/backup_smart_lms.sh
```

### Setup Cron Job
```bash
sudo crontab -e
```

Add:
```
0 2 * * * /usr/local/bin/backup_smart_lms.sh
```

## Step 11: Security Hardening

### Firewall Setup
```bash
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

### Fail2Ban
```bash
sudo apt install fail2ban -y
sudo systemctl start fail2ban
sudo systemctl enable fail2ban
```

### Django Security Settings
Ensure in `settings.py`:
```python
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

## Step 12: Performance Optimization

### Enable Gzip in Nginx
Add to Nginx config:
```nginx
gzip on;
gzip_vary on;
gzip_min_length 1024;
gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;
```

### Database Optimization
```sql
-- Create indexes
CREATE INDEX idx_student_user ON students(user_id);
CREATE INDEX idx_student_batch ON students(batch_id);
CREATE INDEX idx_attendance_date ON attendance(date);
```

## Step 13: Maintenance

### Update Application
```bash
cd /var/www/smart_lms
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
sudo systemctl restart daphne
```

### View Logs
```bash
# Gunicorn logs
sudo journalctl -u gunicorn

# Nginx logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/nginx/access.log

# Django logs
sudo tail -f /var/log/smart_lms/django.log
```

## Troubleshooting

### Gunicorn Not Starting
```bash
sudo systemctl status gunicorn
sudo journalctl -u gunicorn -n 50
```

### Static Files Not Loading
```bash
python manage.py collectstatic --noinput
sudo systemctl restart nginx
```

### Database Connection Issues
```bash
sudo -u postgres psql
\l  # List databases
\du # List users
```

### Permission Issues
```bash
sudo chown -R www-data:www-data /var/www/smart_lms
sudo chmod -R 755 /var/www/smart_lms
```

## Monitoring Tools

### Install Monitoring
```bash
# Install htop
sudo apt install htop

# Install PostgreSQL monitoring
sudo apt install postgresql-contrib
```

### Check System Resources
```bash
htop
df -h
free -m
```

## Scaling Considerations

### Horizontal Scaling
- Use load balancer (Nginx/HAProxy)
- Multiple application servers
- Shared database server
- Centralized Redis server
- Shared file storage (S3)

### Vertical Scaling
- Increase server resources
- Optimize database queries
- Enable caching (Redis/Memcached)
- Use CDN for static files

## Production Checklist

- [ ] DEBUG = False
- [ ] Strong SECRET_KEY
- [ ] PostgreSQL configured
- [ ] Redis configured
- [ ] SSL certificate installed
- [ ] Firewall configured
- [ ] Backup system setup
- [ ] Monitoring enabled
- [ ] Logs configured
- [ ] Email configured
- [ ] Static files collected
- [ ] Media files secured
- [ ] Database optimized
- [ ] Security headers set
- [ ] Error pages customized

## Support

For deployment issues:
- Check logs first
- Review Django documentation
- Check Nginx/Gunicorn docs
- Contact support team

---

**Deployment completed! Your Smart LMS is now live! 🎉**
