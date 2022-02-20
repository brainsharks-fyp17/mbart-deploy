### Run
Start the frontend
Add the following `.env` file in the `frontend` directory
```
BACKEND_HOST=backend-service
BACKEND_PORT=8000
```
```bash
cd frontend && python3 main.py
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
```
cd frontend && python3 main.py
```

### Run using Docker Compose
From the root of the repository,
```bash
docker-compsoe up
```


## Build new images
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
