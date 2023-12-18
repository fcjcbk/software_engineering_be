# SoftEngineer project Backend

## Quick Start
```sh
pip install -r requirements.txt
```

### start and Hot-Reload for Development

```sh
cd app
uvicorn main:app --reload
```

### before commit
```sh
# if you add new package please update dependency before commit
pip freeze > requirements.txt
```