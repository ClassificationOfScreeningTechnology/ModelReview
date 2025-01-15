
# Inzynier API Project

This project is an API built using FastAPI, which processes image files and makes predictions based on the uploaded content. The API allows you to upload either a single image or multiple images and receive predictions in response. It is containerized using Docker for easy deployment.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Docker**: Docker must be installed on your system. If you don’t have it yet, you can install Docker from [here](https://www.docker.com/get-started).
- **Python**: You will need Python installed if you're not using the containerized environment.

## Getting Started

Follow these steps to build and run the project using Docker.

### 1. Clone the Repository

Clone the repository to your local machine.

```bash
git clone https://github.com/BigMoistLochu/ModelReview.git
```

### 2. Build the Docker Image

Build the Docker image using the following command. This will create an image named `inzynier-app` based on the `Dockerfile` present in the project.

```bash
docker build -t inzynier-app .
```

### 3. Run the Docker Container

Once the image is built, you can run it using Docker. This command will run the container in interactive mode (`-it`), mapping port 8000 on your local machine to port 8000 in the container, allowing you to access the FastAPI application via `localhost:8000`.

```bash
# docker run -it --name myapp-container -p 8000:8000 inzynier-app /bin/bash
docker run -it --name myapp-container -p 8000:8000 -p 8501:8501 inzynier-app /bin/bash

```

- `--name myapp-container`: Assigns a name to your running container (`myapp-container`).
- `-p 8000:8000`: Maps port 8000 on your host machine to port 8000 inside the container.
- `/bin/bash`: Starts an interactive bash shell inside the container.

### 4. Start the FastAPI Application

Inside the container, run the following command to start the FastAPI app with Uvicorn. This will launch the API on `0.0.0.0:8000`, making it accessible from your browser or any client application.

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
# http://localhost:8501  dla frontendu
streamlit run app/streamlit_app.py
```

- `app.main:app`: This tells Uvicorn to run the `app` instance from the `main.py` file located in the `app` directory.
- `--host 0.0.0.0`: Makes the application accessible from any IP address (not just `localhost`).
- `--port 8000`: Specifies that the app should run on port 8000.

### 5. Access the Application

After starting the server, the FastAPI application will be available at:

```
http://localhost:8000
```

You can view the interactive API documentation at:

```
http://localhost:8000/docs
```

Here, you can test the endpoints, such as uploading a file, directly from the web interface.

### 6. Stopping the Container

When you're done with the project, you can stop the container with the following command:

```bash
docker stop myapp-container
```

If you want to remove the container after stopping it:

```bash
docker rm myapp-container
```

### 7. Rebuilding the Docker Image (if needed)

If you make changes to your application and want to rebuild the Docker image, use the following command:

```bash
docker build -t inzynier-app .
```

Then, restart the container as described in step 3.
