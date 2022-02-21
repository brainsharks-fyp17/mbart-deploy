##  Deploy on minikube
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
helm upgrade --install loki grafana/loki-stack  --set grafana.enabled=true,prometheus.enabled=true,prometheus.alertmanager.persistentVolume.enabled=false,prometheus.server.persistentVolume.enabled=false
```
Deploy the application on k8s
```bash
kubectl apply -f ./k8s-resources
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
## Deploy on GKE
todo