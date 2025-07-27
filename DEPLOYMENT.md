# Proxmox LXC Deployment Guide

This guide provides step-by-step instructions for deploying the workout tracker application on a Proxmox LXC container running Debian 11.

## 1. Create the LXC Container

1.  In the Proxmox web interface, click "Create CT".
2.  **General:**
    *   **Hostname:** `workout-tracker`
    *   **Password:** Choose a strong password.
3.  **Template:**
    *   **Storage:** `local`
    *   **Template:** `debian-11-standard`
4.  **Disks:**
    *   **Root disk:** `8GB` is sufficient for this application.
5.  **CPU:**
    *   **Cores:** `1` or `2` cores should be enough.
6.  **Memory:**
    *   **Memory:** `1024MB`
    *   **Swap:** `512MB`
7.  **Network:**
    *   **Name:** `eth0`
    *   **Bridge:** `vmbr0` (or your primary bridge)
    *   **VLAN Tag:** (optional)
    *   **Firewall:** (optional)
    *   **IPv4:** `DHCP` or a static IP address.
    *   **IPv6:** `DHCP` or a static IP address.
8.  **DNS:**
    *   **DNS domain:** (optional)
    *   **DNS servers:** (optional)
9.  **Confirm:** Review the settings and click "Finish".

## 2. Initial Server Setup

1.  Start the container and open a console session.
2.  Update the package list and upgrade the installed packages:
    ```bash
    apt update && apt upgrade -y
    ```
3.  Install required packages:
    ```bash
    apt install -y python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl
    ```

## 3. Database Setup

1.  Log in to the PostgreSQL interactive terminal:
    ```bash
    sudo -u postgres psql
    ```
2.  Create a new database:
    ```sql
    CREATE DATABASE workout_tracker;
    ```
3.  Create a new user and set a password:
    ```sql
    CREATE USER workout_tracker_user WITH PASSWORD 'your_password';
    ```
4.  Grant the user privileges on the database:
    ```sql
    GRANT ALL PRIVILEGES ON DATABASE workout_tracker TO workout_tracker_user;
    ```
5.  Exit the `psql` shell:
    ```
    \q
    ```

## 4. Application Setup

1.  Create a directory for the application:
    ```bash
    mkdir /opt/workout_tracker
    ```
2.  Create a virtual environment:
    ```bash
    python3 -m venv /opt/workout_tracker/venv
    ```
3.  Activate the virtual environment:
    ```bash
    source /opt/workout_tracker/venv/bin/activate
    ```
4.  Clone the application repository:
    ```bash
    git clone https://github.com/your-username/your-repo.git /opt/workout_tracker/app
    ```
5.  Install the required Python packages:
    ```bash
    pip install -r /opt/workout_tracker/app/requirements.txt
    ```
6.  Configure the application settings:
    *   Open `/opt/workout_tracker/app/workout_project/settings.py` and configure the `DATABASES` setting with the credentials you created in the previous step.
    *   Set `DEBUG = False`.
    *   Set `ALLOWED_HOSTS = ['your_domain_or_ip']`.
7.  Run the database migrations:
    ```bash
    python /opt/workout_tracker/app/manage.py migrate
    ```
8.  Collect the static files:
    ```bash
    python /opt/workout_tracker/app/manage.py collectstatic
    ```

## 5. Gunicorn Setup

1.  Create a Gunicorn systemd service file:
    ```bash
    nano /etc/systemd/system/gunicorn.service
    ```
2.  Add the following content to the file:
    ```ini
    [Unit]
    Description=gunicorn daemon
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/opt/workout_tracker/app
    ExecStart=/opt/workout_tracker/venv/bin/gunicorn \
        --access-logfile - \
        --workers 3 \
        --bind unix:/run/gunicorn.sock \
        workout_project.wsgi:application

    [Install]
    WantedBy=multi-user.target
    ```
3.  Start and enable the Gunicorn service:
    ```bash
    systemctl start gunicorn
    systemctl enable gunicorn
    ```

## 6. Nginx Setup

1.  Create an Nginx server block file:
    ```bash
    nano /etc/nginx/sites-available/workout_tracker
    ```
2.  Add the following content to the file:
    ```nginx
    server {
        listen 80;
        server_name your_domain_or_ip;

        location = /favicon.ico { access_log off; log_not_found off; }
        location /static/ {
            root /opt/workout_tracker/app;
        }

        location / {
            include proxy_params;
            proxy_pass http://unix:/run/gunicorn.sock;
        }
    }
    ```
3.  Create a symbolic link to the `sites-enabled` directory:
    ```bash
    ln -s /etc/nginx/sites-available/workout_tracker /etc/nginx/sites-enabled
    ```
4.  Test the Nginx configuration:
    ```bash
    nginx -t
    ```
5.  Restart Nginx:
    ```bash
    systemctl restart nginx
    ```

Your application should now be accessible at `http://your_domain_or_ip`.
