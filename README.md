# Account service
> Develop by FastAPI and MongoDB

<br>

## Setup environment variable
* Create **.env** file in **root folder**

| Variable name | Description        | Example                                               |
| ------------- | ------------------ | ----------------------------------------------------- |
| DB_URI        | MongoDB connection | `mongodb+srv://user:pass@cluster.mhaauzq.mongodb.net` |
| DB_NAME       | MongoDB DB name    | `account-service-testing`                             |
| SECRET_KEY    | JWT secret key     | `B50HiHr6w1JTR0P2zcWOcGthEGJOzqzxuym2S7FNhrE=`        |

<br>

## Run project with script
* Windows:
    ```powershell
    .\.script\run.bat
    ```

* Docker (Windows)
    ```powershell
    .\.script\docker.bat
    ```

<br>

## Run project manual
* Install Python packages
    ```bash
    pip install -r requirements.txt
    ```

* Change directory to source code folder
    ```bash
    cd src
    ```

* Run server
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 80
    ```

* Visit API document at http://localhost/docs

<br>

## Run tests
```bash
pytest
```
