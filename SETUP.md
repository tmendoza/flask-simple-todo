# **ELI5 Guide: Docker on Kubuntu with LXC, plus Flask + PostgreSQL in VS Code**

Imagine you have a big playground called **Kubuntu** where you’ve already set up **LXC** (like little playground corners). Now you want to bring in **Docker** (another kind of playground corner) without messing up your LXC corners. Next, you’d like to build a small **Flask** (Python) app that talks to a **PostgreSQL** (database) server. Finally, you want to do all your coding and testing in **VS Code** easily. This guide explains each step **as simply as possible**, so you can follow along even if you’re new to Docker and PostgreSQL.

---

## **Table of Contents**
1. [What You Need to Know First](#1-what-you-need-to-know-first)  
2. [Step 1: Prepare Your System](#2-step-1-prepare-your-system)  
3. [Step 2: Install Docker](#3-step-2-install-docker)  
4. [Step 3: Make Docker and LXC Play Nicely](#4-step-3-make-docker-and-lxc-play-nicely)  
5. [Step 4: Build Your Flask + PostgreSQL Setup with Docker Compose](#5-step-4-build-your-flask--postgresql-setup-with-docker-compose)  
6. [Step 5: Work in VS Code Dev Containers](#6-step-5-work-in-vs-code-dev-containers)  
7. [Step 6: Check, Stop, and Restart as Needed](#7-step-6-check-stop-and-restart-as-needed)  
8. [Wrap Up](#8-wrap-up)  

---

## 1. What You Need to Know First
- **Kubuntu**: Like Ubuntu, but with a different desktop called KDE.  
- **LXC**: A way to run small “lightweight” systems inside your computer.  
- **Docker**: Another way to run programs in “containers,” but it’s more popular for running apps (like a web server or database).  
- **Flask**: A simple Python-based web framework.  
- **PostgreSQL**: A database server (stores data so your app can save and retrieve info).  
- **VS Code**: A code editor that can talk directly to Docker containers, so you can code “inside” them without messing up your main system.

---

## 2. Step 1: Prepare Your System

### 2.1 Update Your System
```bash
sudo apt update && sudo apt upgrade -y
```
**In simple terms**: We’re making sure our “sandbox” is clean and up to date. This helps avoid weird bugs later.

### 2.2 Check What LXC Containers You Already Have
```bash
lxc-ls --fancy
```
**In simple terms**: We’re looking at which LXC “corners” already exist in our playground. We don’t want to break them.

### 2.3 Look at LXC’s Networking
```bash
ip a | grep br
```
**In simple terms**: This helps you find any “bridge” networks LXC made (often called `lxcbr0`). Think of a “bridge” as the path data travels to go in and out of containers.

---

## 3. Step 2: Install Docker

### 3.1 Remove Old Docker Versions (If Any)
```bash
sudo apt remove docker docker-engine docker.io containerd runc
```
**In simple terms**: Throw out any older or half-installed Docker parts so we start fresh.

### 3.2 Add Docker’s Official Software Source
```bash
sudo apt update
sudo apt install ca-certificates curl gnupg lsb-release

sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```
**In simple terms**: We’re telling our computer, “Hey, here’s where the official Docker goodies live!” So when we install Docker, we get the real deal.

### 3.3 Install Docker
```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io \
  docker-buildx-plugin docker-compose-plugin
```
**In simple terms**: Now we get Docker itself plus all the tools needed to run containers and use Docker Compose.

### 3.4 Let Yourself Use Docker Without Sudo
```bash
sudo usermod -aG docker $USER
```
**In simple terms**: This makes sure you don’t have to type `sudo` every time you run a Docker command. You might need to log out and back in for this to work.

### 3.5 Test Docker
```bash
docker run hello-world
```
**In simple terms**: We’re making Docker pull a tiny test container to see if everything’s okay.

---

## 4. Step 3: Make Docker and LXC Play Nicely

### 4.1 Check Bridges Again
```bash
ip a
```
**In simple terms**: Confirm Docker made a `docker0` bridge. You’ll see `lxcbr0` for LXC, and `docker0` for Docker. They shouldn’t “argue” about using the same address range.

### 4.2 Optional: Create a Custom Docker Network  
(Only if `docker0` is fighting with `lxcbr0` over IP addresses)
```bash
docker network create --subnet=192.168.200.0/24 customdocker
```
Then, in your `docker-compose.yml`, you can point your containers to this new network if needed.

**In simple terms**: If Docker and LXC are stepping on each other’s toes, give Docker a new “play area” (subnet) to use.

### 4.3 Restart Services
```bash
sudo systemctl restart lxc-net
sudo systemctl restart docker
```
**In simple terms**: Tells your system, “Okay, re-check everything so we can use the new settings.”

---

## 5. Step 4: Build Your Flask + PostgreSQL Setup with Docker Compose

### 5.1 Make a Project Folder
```bash
mkdir ~/flask_postgres_project
cd ~/flask_postgres_project
```
**In simple terms**: This is the folder where we’ll keep all our code and Docker files.

### 5.2 Write a Dockerfile for Flask
**File**: `Dockerfile`
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 5000
CMD ["python", "app.py"]
```
**In simple terms**: Tells Docker how to build a box that has Python installed, installs your Python libraries, then runs your Flask web app.

### 5.3 Create a Simple Flask App
**File**: `app.py`
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World from Flask!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```
**In simple terms**: A tiny Python program that prints out a friendly message when you go to the homepage.

### 5.4 List Your Requirements
**File**: `requirements.txt`
```
flask==2.2.3
psycopg2-binary==2.9.6
```
**In simple terms**: We need Flask for the web server, and `psycopg2-binary` to connect to PostgreSQL (even if we’re not using it yet).

### 5.5 Write Your Docker Compose File
**File**: `docker-compose.yml`
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: flask_app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DB_HOST=db
      - DB_PORT=5432
      - DB_USER=postgres
      - DB_PASSWORD=postgres
      - DB_NAME=test_db
    depends_on:
      - db

  db:
    image: postgres:15-alpine
    container_name: postgres_db
    environment:
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_DB=test_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```
**In simple terms**:  
- **`web`**: Builds our Flask container from the Dockerfile.  
- **`db`**: Uses the official PostgreSQL image.  
- They can talk to each other thanks to Docker Compose.  
- The volume (`postgres_data`) stores the database files so data doesn’t vanish when the container restarts.

### 5.6 Build and Start Everything
```bash
docker-compose build
docker-compose up -d
```
**In simple terms**:  
- **`docker-compose build`**: Makes the “web” image using your Dockerfile.  
- **`docker-compose up -d`**: Starts both the “web” and “db” containers in the background.

### 5.7 Check If It’s Working
Open a browser or terminal and go to [http://localhost:5000/](http://localhost:5000/).  
You should see **“Hello, World from Flask!”**

---

## 6. Step 5: Work in VS Code Dev Containers

### 6.1 Install VS Code + Extensions
- **VS Code** from [https://code.visualstudio.com/](https://code.visualstudio.com/).  
- **Dev Containers** (or “Remote - Containers”) extension.  
- **Python** extension (for linting, IntelliSense).  

**In simple terms**: We’re setting up our coding environment so we can code inside containers, which means your host machine won’t get cluttered with library mismatches.

### 6.2 Create Dev Container Files
Make a folder called `.devcontainer` in your project, then add a file named `devcontainer.json` inside it.

**File**: `.devcontainer/devcontainer.json`
```json
{
  "name": "Flask Dev Container",
  "dockerComposeFile": "../docker-compose.yml",
  "service": "web",
  "workspaceFolder": "/app",
  "settings": {
    "terminal.integrated.defaultProfile.linux": "/bin/bash"
  },
  "extensions": [
    "ms-python.python",
    "ms-python.vscode-pylance"
  ],
  "remoteUser": "root"
}
```
**In simple terms**: Tells VS Code that:  
- We want to use the “web” service from our `docker-compose.yml`.  
- Our code folder inside the container is `/app`.  
- We want Python extensions installed automatically.

### 6.3 Open Your Project in a Container
1. Open VS Code and pick **File → Open Folder** → choose `~/flask_postgres_project`.  
2. VS Code will notice the `.devcontainer` folder and might ask: “Reopen in Container?”  
3. If it doesn’t, open the command menu (Ctrl+Shift+P), search for **“Dev Containers: Reopen in Container”**.

**In simple terms**: VS Code will spin up (or attach to) the `web` container, letting you edit, run, and debug code right there. You don’t need Python installed on your main system for this to work— Docker handles everything.

---

## 7. Step 6: Check, Stop, and Restart as Needed

### 7.1 Look at Logs
```bash
docker-compose logs web
docker-compose logs db
```
**In simple terms**: Peek at what your Flask app or database is saying. Useful if something breaks.

### 7.2 Stop Everything
```bash
docker-compose down
```
**In simple terms**: Takes down all containers so they’re no longer running.

### 7.3 Delete Volumes (Reset the Database)
```bash
docker-compose down -v
```
**In simple terms**: Also removes the stored PostgreSQL data so you can start fresh.

---

## 8. Wrap Up
Here’s what we just did:
1. **Updated** your Kubuntu system and checked LXC containers.  
2. **Installed Docker** and made sure it doesn’t fight with LXC.  
3. **Set up** a Flask app and a PostgreSQL database using Docker Compose.  
4. **Developed** inside a container with VS Code, so it’s easy and consistent.  

**Benefit**: You don’t have to install Python or PostgreSQL on your main system (beyond Docker), and everything can be put away with a single `docker-compose down`. No fuss, no mess!

