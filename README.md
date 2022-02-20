### Run
Start the frontend
.env file
```
BACKEND_HOST=backend-service
BACKEND_PORT=8000
```
```
cd frontend && python3 main.py
```
Start the backend
```
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
