## Run locally
Start the frontend
Add the following `.env` file in the `frontend` directory
```
BACKEND_HOST=backend-service
BACKEND_PORT=8000
```
Install dependencies
```bash
cd frontend
pip install -r requirements.txt
```
```bash
python3 main.py
```
Start the backend
Add the following `.env` file in the `backend` directory
```config
MODEL_PATH=Rumesh/mbart-si-simp
MAX_LENGTH=700
NUM_BEAMS=5
TASK=com-sim
ENABLE_METRICS=1
REDIS_HOST=redis-service
REDIS_PORT=6379
```
Install dependencies
```bash
cd backend
pip install -r requirements.txt -r requirements-local.txt 
```
```bash
python3 main.py
```

## Run using Docker Compose
Add the `.env` files to the respective directories.<br>
From the root of the repository,
```bash
docker-compose up
```


## Build new Docker images
Login to docker hub
```bash
docker login
```
Build and push the docker images
```bash
cd backend 
docker build -t rumeshms16/mabrt-simp:1.0.0 .
docker push rumeshms16/mabrt-simp:1.0.0
```

```bash
cd frontend 
docker build -t rumeshms16/simp-frontend:1.0.0 .
docker push rumeshms16/simp-frontend:1.0.0
```

## Deploy on K8s
See [k8s-resources](k8s-resources)
