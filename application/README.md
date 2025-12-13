# 🚀 Age and Gender Predictor 🚀

## 📋 Prerequisites

Dependencies:

* Docker

* Python 3

  * Pip (Usually included with python)

## ⚡ Quick Start Guide

From `/application/` directory, execute the build script:

```sh
build.sh
```

This script will:

1. ✅ Check for dependencies (`docker`, `python3`).

2. 📦 Download the required models.

3. 🛠️ Build Docker images

4. Run application.

Once it's done, you can access the application at `http://localhost:8000`.

## ❓ Troubleshooting

### ⚠️ Model Download Fails

If `download_models.sh` fails:

* **Is Python 3 installed?** Verify by running `python3 --version`.

* **Is Pip available?** The script needs `pip` to install `gdown`. You can get
it by following the official guide: [Installing
Pip](https://pip.pypa.io/en/stable/installation/).

### ⚙️ Docker Errors

* **Permission Denied (Docker):** If you see errors like `permission denied`,
you may need to run Docker with `sudo` or [add your user to the `docker`
group]([https://docs.docker.com/engine/install/linux-postinstall/](https://docs.docker.com/engine/install/linux-postinstall/)).

* **Docker Daemon Not Running:** If commands fail with a `Cannot connect to the
Docker daemon` message, you need to start the Docker service on your machine.

* **Port is already allocated:** If you see an error that port `8000` is in
use, another application is using it. You can either stop that application or
change the port in your `docker-compose.yml` file (e.g., change `"8000:8000"`
to `"8001:8000"`).
