# 🚀 Age and Gender Predictor 🚀

A brief, one-sentence pitch for what your amazing application does.

## 📋 Prerequisites

Before you begin, ensure you have the following tools installed and running:

* **Docker & Docker Compose:** The engine that runs the application.

  * ✅ [Install Docker](https://docs.docker.com/get-docker/)

  * *Make sure the Docker daemon is running!*

* **Python 3 & Pip:** Required to download necessary model files.

  * ✅ [Install Python](https://www.python.org/downloads/) (Pip is usually included)

## ⚡ Quick Start Guide

Getting the application up and running is as simple as running one command.

From the project's root directory, execute the build script:

```
sh build.sh
```
This script will:

1. ✅ Check for dependencies (`docker`, `python3`).

2. 📦 Download the required models into the `webapp/` directory.

3. 🛠️ Build the Docker image and run the application in the background.

Once it's done, you can access the application at `http://localhost:8000`.

## ❓ Troubleshooting

Running into issues? Here are some common problems and their solutions.

### ⚠️ Model Download Fails

If the `download_models.sh` script fails, it's almost always a Python issue.

* **Is Python 3 installed?** Verify by running `python3 --version`.

* **Is Pip available?** The script needs `pip` to install `gdown`. You can get it by following the official guide: [Installing Pip](https://pip.pypa.io/en/stable/installation/).

### 💣 The "Nuke & Pave" Method (For Build Failures)

If the application isn't working correctly after a build, the best solution is often to start fresh. This clears out any old containers, networks, and build cache that might be causing conflicts.

**Step 1: Shut Down & Remove Everything**
This command stops and removes the containers and networks defined in your `docker-compose.yml`.
```
docker-compose down
```

**Step 2: Clear the Docker Build Cache**
This command removes all dangling build cache, forcing Docker to rebuild from scratch.
```
docker build prune
```
*You'll be asked to confirm (`y/N`). Press `y` and Enter.*

**Step 3: Re-run the Build Script**
Now, with a clean slate, run the original command.
```
sh build.sh
```
### ⚙️ Other Common Issues

* **Permission Denied (Docker):** If you see errors like `permission denied`, you may need to run Docker with `sudo` or [add your user to the `docker` group]([https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)).

* **Docker Daemon Not Running:** If commands fail with a `Cannot connect to the Docker daemon` message, you need to start the Docker service on your machine.

* **Port is already allocated:** If you see an error that port `8000` is in use, another application is using it. You can either stop that application or change the port in your `docker-compose.yml` file (e.g., change `"8000:8000"` to `"8001:8000"`).
