## Run locally
Create a virtual environment
```bash
virtualenv env
```
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
Install Docker: Refer - https://docs.docker.com/engine/install/ubuntu/ <br>
Add the `.env` files to the respective directories.<br>
From the root of the repository,
```bash
docker-compose up --build
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
![ml-deploy](https://user-images.githubusercontent.com/32504465/154938944-95257691-75e0-4775-9df1-e784d289aec7.png)

###  Deploy on minikube
Install kubectl
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
```
Install minikube
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube_latest_amd64.deb
sudo dpkg -i minikube_latest_amd64.deb
```
Install Helm
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```
Add the grafana chart to Helm
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
```
Start minikube
```bash
minikube start
```
Run the minikube dashboard (optional)
```bash
minikube dashboard &
```
Add monitoring tools: Grafana, Loki, Promtail
```bash
helm upgrade --install loki grafana/loki-stack  --set grafana.enabled=true,prometheus.enabled=true,prometheus.alertmanager.persistentVolume.enabled=false,prometheus.server.persistentVolume.enabled=false --set-file extraScrapeConfigs=k8s-resources/extraScrapeConfigs.yaml --set-file prometheus.extraScrapeConfigs=extraScrapeConfigs.yaml
```
The --set-file flag sets the prometheus config required for prometheus to scrape metrics from the backend. <br>
Deploy the application on k8s
```bash
helm install mbart-deploy ./helm-chart
```
Access Grafana: get the `admin` password
```bash
kubectl get secret --namespace default loki-grafana -o jsonpath="{.data.admin-password}" | base64 --decode ; echo
```
Port forward to access services
```bash
kubectl port-forward svc/frontend-service 5000:5000 --address=0.0.0.0 &
kubectl port-forward svc/loki-grafana 3000:80 --address=0.0.0.0 &
```
### Deploy on GKE
todo