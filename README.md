# Milk price estimator

This repository contains the code to execute a training pipeline and the deployment of an API to predict the price of milk in Chile based on rainfall and macroeconomic variables.

To execute in a local environment it is necessary to have Docker installed, and run the following commands:
```shell
git clone https://github.com/davichoar/mle-aag
cd mle-aag/
docker build -t milkprice . && docker run -d -p 8080:8080 -it milkprice
```
This will run the training pipeline and expose the API on port 8080.

## Estructura del proyecto
```text
│mle-aag
│
├── data                    <- Data provided to recreate the model.
│
├── pipeline                <- Folder that contains the pipeline code.
│   ├── config.py           <- File to store the configuration parameters for the pipeline.
│   ├── preprocess.py       <- Preprocessing functions of the pipeline.
│   ├── run.py              <- File that orchestrates the pipeline.
│   ├── train.py            <- Training functions of the pipeline.
│   └── wrangler.py         <- Data wrangling functions of the pipeline.
│ 
├── review-nb               <- Folder that contains DS original nb, and a copy of it for 
│                              debugging and validation.
│ 
├── aag_collection.json     <- Postman collection to test endpoints.
├── app.py                  <- Main file for the FastAPI service, containing routes.
├── constants.py            <- File containing configuration vars and testing samples.
├── Dockerfile              <- File to create Docker image
├── domain.py               <- Definitions of the request and response structures.
├── healthcheck.py          <- Functions for the healtcheck endpoint.
├── pipeline_and_deploy.sh  <- Bash file that runs the pipeline and deploys the API.
├── pipeline.joblib         <- Model created from running locally the pipeline.run module.
├── README.md               <- This file.
├── requirements.txt        <- Python requirements for pipeline and API.
└── utils.py                <- Python utilities for request handling and preprocess.
```


## API Documentation

### GET /docs
Endpoint created automatically by FastAPI for auto-documentation using the pydantic models.It uses an OpenAPI standard. No metadata has been provided to enrich these docs but it is a good start to understand the requests and responses of the endpoints.

### POST /predict
Main endpoint to execute online prediction. The request has 5 parts: 
1. periodo: Date in the format "%Y-%m-%d".
2. precipitaciones: Dictionary containing monthly rainfall information (8 chilean cities).
3. pib: Dictionary containing monthly gross domestic product information (28 items).
4. imacec: Dictionary containing monthly economic activity information (9 items).
5. indiceVentasNoDurablesIVCM: non-durable trade sales index monthly measure.

The response contains only one key named 'precio' (price), for the milk price estimation.

<p align="center">
  <img height="400" src="https://i.ibb.co/gFqDyqT/postman-demo.png" alt="Postman demo"/>
</p>

### GET /health
Endpoint to check if the model was correctly built, testing it against a random feature vector containing the columns of the training phase. It should return a 'PASS' status.

## Notes
- Due to time and practicality limitations in the indications for the challenge, the pipeline was made in separated python modules instead of using a tool like Kubeflow that will require a cluster to execute the pipeline steps.
- The original notebook showed more features in the results displayed, resulting in a better performance on the validation set. Running a copy of the notebook, the results were quite different, so it was assumed that some functions of the notebook were deleted and the pipeline/API had to be made only with the logic inside the notebook.
- Due to the nature of the pipeline (feature selection steps such as SelectKBest), it is posible that the final artifact does not use some of the columns sent in the request. Nevertheless, all features are required in the body of the request as a new version of the model could select another features as important.


