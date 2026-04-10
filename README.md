# Account service
> Develop by FastAPI and MongoDB

<br>

## Setup environment variable
* Create **.env** file in root folder

| Variable name | Description        | Example                                             |
| ------------- | ------------------ | --------------------------------------------------- |
| MONGODB_URI   | MongoDB connection | mongodb+srv://user:pass@cluster.mhaauzq.mongodb.net |

<br>

## Run project with script
* Windows:
    ```powershell
    .\run.bat
    ```
* Linux
    ```bash
    # Coming soon
    ```

* Docker
    ```bash
    # Coming soon
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
    uvicorn main:app --reload
    ```
