COE 379L — Project 2 Inference Server

This folder contains the deployed inference server for my Hurricane Harvey building-damage classifier, including the Docker image, server code, and usage instructions.

📁 Included Files
File	Description
Dockerfile	Builds the inference server container
docker-compose.yml	Runs the container on port 5000
server/app.py	Flask inference server
server/requirements.txt	Python dependencies
saved_models/best_model.keras	Persisted trained model used for deployment
🚀 1. Build the Docker Image

Run inside the folder containing the Dockerfile:

docker build -t leenajoshi/coe379l-proj2:latest .


This creates an x86-compatible image (required by course instructions).

📤 2. Push Image to Docker Hub

Tag and push:

docker tag leenajoshi/coe379l-proj2:latest 
docker push leenajoshi/coe379l-proj2:latest


You must be logged in:

docker login

▶️ 3. Run the Inference Server

Using docker-compose:

docker-compose up --build


This launches the server at:

http://127.0.0.1:5000

📄 4. API Endpoints
GET /summary

Returns metadata about the deployed model.

curl http://127.0.0.1:5000/summary


Example response:

{
  "model": "alt_lenet",
  "input_shape": [128,128,3],
  "num_params": 8498625,
  "description": "Damage vs no_damage classifier"
}

POST /inference

Accepts raw binary jpeg bytes.
Returns "damage" or "no_damage".

curl -X POST \
  --data-binary @example.jpeg \
  http://127.0.0.1:5000/inference


Example output:

{
  "prediction": "damage"
}

📌 Notes

The inference server performs zero preprocessing at the API boundary (as required).

All resizing and normalization happens inside the server.

The model used is the best-performing alt_lenet model from Part 2.
