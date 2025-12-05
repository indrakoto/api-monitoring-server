## API Monitoring Server


### Install Python
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential
python3 --version
pip3 --version
```


Clone API Backend
```bash
cd /var/www

git clone git@github.com:indrakoto/api-monitoring-server.git backend

cd backend

chmod +x /var/www/backend/api-monitoring-server.py

cp /var/www/backend/api-monitoring-server.service /etc/systemd/system

python3 -m venv venv

source venv/bin/activate

sudo systemctl daemon-reload
sudo systemctl enable api-monitoring-server
sudo systemctl start api-monitoring-server
sudo systemctl status api-monitoring-server
```

### Cek status
```bash
sudo systemctl status api-monitoring-server
```

### Cek logs
```bash
sudo journalctl -u api-monitoring-server -f
```

### Cek process
```bash
ps aux | grep api-monitoring-server
```

### Test API
```bash
curl http://localhost:5005/health
```