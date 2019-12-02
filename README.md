# Kubernetes experiments

- Basic notes on Kubernetes & Helm - at `./kube`
- Launching minikube, configuring RBAC/ABAC - at `./kube/config/{abac|rbac}`

# Github Actions & Packages

- see `./github/` for a pipeline (only 1 job)
- see Packages at github repo - there will be a docker image available

### Notes on using this sample flask app

- connect (e.g. with Mongo Explorer - Intellij Idea plugin) with the following creds:
  - uri: `localhost:27017`
  - creds: `admin/admin`
  - auth database: `kube`
  - mechanism: `scram`

- example request to save json from body:
```bash
curl -X POST localhost:5000/api/docs -H 'content-type: application/json' -d '{"hello": "world"}'
```

or same via HTTPie:
```bash
http localhost:5000/api/docs hello=world
```

- venv:
```bash
pip3 install virtualenv
virtualenv venv --python python3
# export LC_ALL=C in case of unsupported locale
source venv/bin/activate
pip install -r requirements.txt 
```

- build actions:
```bash
docker build -t flask .
docker run -p 5000:5000 flask
docker exec -it <cnt_id> sh
```

- run Flask in dev mode == setting env `FLASK_ENV=development`

- running tests: `pytest` from here. or `pytest backend/tests` if not tests found

- to write messages from `print` straight to container's stdout, use `print = partial(print, flush=True)` which
flushes buffer (and writes data) immediately
