# QualityForce AI - Deployment Guide

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Local Development Setup](#local-development-setup)
3. [Production Deployment](#production-deployment)
4. [Configuration](#configuration)
5. [Troubleshooting](#troubleshooting)

## System Requirements

### Minimum Requirements

- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 10 GB free space
- **OS**: Linux, macOS, or Windows

### Recommended for Production

- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 50+ GB SSD
- **OS**: Linux (Ubuntu 20.04+ or CentOS 8+)

### Software Dependencies

- Python 3.9 or higher
- Node.js 18 or higher
- npm or yarn
- Git

## Local Development Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/QualityForceAI.git
cd QualityForceAI
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv venv

# On Linux/macOS
source venv/bin/activate

# On Windows
venv\Scripts\activate

# Install dependencies
pip install -r ../requirements.txt

# Create environment file
cp ../.env.example .env

# Edit .env file with your settings
nano .env  # or use your preferred editor

# Run the backend
python main.py
```

The backend will start on `http://localhost:8000`

### 3. Frontend Setup

```bash
# Open a new terminal
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will start on `http://localhost:5173`

### 4. Verify Installation

1. Open browser and navigate to `http://localhost:5173`
2. You should see the QualityForce AI dashboard
3. Navigate to the Marketplace to see available agents
4. Test API: `curl http://localhost:8000/api/health`

## Production Deployment

### Option 1: Docker Deployment (Recommended)

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports:
      - "8000:8000"
    environment:
      - HOST=0.0.0.0
      - PORT=8000
      - DEBUG=False
    volumes:
      - ./test_results:/app/test_results
      - ./test_evidences:/app/test_evidences
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: Dockerfile.frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

Create `Dockerfile.backend`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/

WORKDIR /app/backend

CMD ["python", "main.py"]
```

Create `Dockerfile.frontend`:

```dockerfile
FROM node:18 as build

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

Create `nginx.conf`:

```nginx
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

Deploy:

```bash
docker-compose up -d
```

### Option 2: Manual Deployment

#### Backend Deployment

1. **Install system dependencies:**

```bash
sudo apt-get update
sudo apt-get install -y python3.9 python3-pip python3-venv
```

2. **Setup application:**

```bash
cd /opt
sudo git clone https://github.com/yourusername/QualityForceAI.git
cd QualityForceAI/backend

sudo python3 -m venv venv
sudo venv/bin/pip install -r ../requirements.txt
```

3. **Create systemd service** (`/etc/systemd/system/qualityforce-backend.service`):

```ini
[Unit]
Description=QualityForce AI Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/QualityForceAI/backend
Environment="PATH=/opt/QualityForceAI/backend/venv/bin"
ExecStart=/opt/QualityForceAI/backend/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

4. **Start service:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable qualityforce-backend
sudo systemctl start qualityforce-backend
```

#### Frontend Deployment

1. **Build frontend:**

```bash
cd frontend
npm install
npm run build
```

2. **Install and configure Nginx:**

```bash
sudo apt-get install -y nginx

sudo cp dist/* /var/www/html/
```

3. **Configure Nginx** (`/etc/nginx/sites-available/qualityforce`):

```nginx
server {
    listen 80;
    server_name your-domain.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

4. **Enable and start Nginx:**

```bash
sudo ln -s /etc/nginx/sites-available/qualityforce /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Cloud Deployment

#### AWS Deployment

1. **Backend on EC2:**
   - Launch EC2 instance (t3.medium recommended)
   - Follow manual deployment steps
   - Configure security groups (ports 80, 443, 8000)

2. **Frontend on S3 + CloudFront:**
   - Build frontend: `npm run build`
   - Upload to S3 bucket
   - Configure CloudFront distribution
   - Setup API Gateway for backend

#### Azure Deployment

1. **Backend on App Service:**
   - Create App Service (Python 3.9)
   - Deploy backend code
   - Configure application settings

2. **Frontend on Static Web Apps:**
   - Deploy frontend build to Azure Static Web Apps
   - Configure API proxy

## Configuration

### Environment Variables

Backend (`.env`):

```bash
# API Settings
HOST=0.0.0.0
PORT=8000
DEBUG=False

# CORS (production domains)
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Storage
RESULTS_DIR=/var/lib/qualityforce/results
EVIDENCE_DIR=/var/lib/qualityforce/evidence

# AI API Keys (optional)
OPENAI_API_KEY=your-key-here
ANTHROPIC_API_KEY=your-key-here

# Execution
MAX_CONCURRENT_AGENTS=20
EXECUTION_TIMEOUT=7200

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://user:pass@localhost/qualityforce
```

### Security Considerations

1. **API Authentication** (recommended for production):

Add to `backend/main.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "your-secret-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return credentials

# Add to routes
@router.get("/", dependencies=[Depends(verify_token)])
```

2. **HTTPS Configuration:**

```bash
# Install certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

3. **Firewall Setup:**

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

## Monitoring and Logging

### Setup Application Logging

Update `backend/main.py`:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/qualityforce/app.log'),
        logging.StreamHandler()
    ]
)
```

### Monitor with systemd:

```bash
# View logs
sudo journalctl -u qualityforce-backend -f

# Check status
sudo systemctl status qualityforce-backend
```

## Troubleshooting

### Backend Issues

**Service won't start:**
```bash
# Check logs
sudo journalctl -u qualityforce-backend -n 50

# Test manually
cd /opt/QualityForceAI/backend
source venv/bin/activate
python main.py
```

**Port already in use:**
```bash
# Find process using port 8000
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

### Frontend Issues

**Build fails:**
```bash
# Clear cache
rm -rf node_modules package-lock.json
npm install
npm run build
```

**API not accessible:**
- Check CORS settings in backend
- Verify proxy configuration in Nginx
- Check firewall rules

### Performance Issues

**High memory usage:**
- Reduce `MAX_CONCURRENT_AGENTS`
- Increase server resources
- Implement result cleanup

**Slow response times:**
- Enable caching
- Optimize database queries
- Use CDN for frontend

## Scaling

### Horizontal Scaling

1. **Load Balancer Setup:**

```nginx
upstream backend {
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}

server {
    location /api {
        proxy_pass http://backend;
    }
}
```

2. **Shared Storage:**
- Use NFS or S3 for test results
- Shared database for execution state

### Vertical Scaling

- Increase CPU/RAM on existing servers
- Optimize concurrent execution limits
- Database optimization

## Backup and Recovery

### Backup Script

```bash
#!/bin/bash
BACKUP_DIR="/backup/qualityforce"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup results
tar -czf $BACKUP_DIR/results_$DATE.tar.gz /var/lib/qualityforce/results

# Backup database (if applicable)
pg_dump qualityforce > $BACKUP_DIR/db_$DATE.sql

# Cleanup old backups (keep 30 days)
find $BACKUP_DIR -mtime +30 -delete
```

### Recovery

```bash
# Restore results
tar -xzf results_YYYYMMDD_HHMMSS.tar.gz -C /var/lib/qualityforce/

# Restore database
psql qualityforce < db_YYYYMMDD_HHMMSS.sql
```

## Maintenance

### Regular Tasks

1. **Log rotation** - Setup logrotate
2. **Result cleanup** - Delete old test results
3. **Security updates** - Regular system updates
4. **Monitoring** - Check resource usage
5. **Backups** - Verify backup integrity

### Updates

```bash
# Pull latest code
cd /opt/QualityForceAI
sudo git pull

# Update backend
cd backend
source venv/bin/activate
pip install -r ../requirements.txt
sudo systemctl restart qualityforce-backend

# Update frontend
cd ../frontend
npm install
npm run build
sudo cp -r dist/* /var/www/html/
```

## Support

For deployment issues:
- Check logs first
- Review configuration
- Consult documentation
- Submit GitHub issue
