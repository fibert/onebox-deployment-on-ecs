
# Usgage
## Clone this repository
```
git clone https://github.com/fibert/onebox-deployment-on-ecs.git
cd onebox-deployment-on-ecs
```

## Install dependencies
```
python3 -m venv .venv
source ./.venv/bin/activate

./scripts/install-deps.sh
```

## Manual deployment
### Deploy shared infrastructure
```
npx cdk deploy SharedInfrastructure
```

### Deploy backend
```
npx cdk deploy Backend
```

### Deploy frontend
```
npx cdk deploy Frontend
```


## Cleanup
```
npx cdk destroy --all -f
```