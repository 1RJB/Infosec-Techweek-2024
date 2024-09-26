# Flask CTF Docker Container

This project contains a Flask-based Capture the Flag (CTF) web application that runs inside a Docker container.

## Prerequisites

Make sure you have the following installed on your system:
- [Docker](https://docs.docker.com/get-docker/)

## Installation Steps

### 1. Clone the repository

- First, clone the project repository to your local machine:
``` shell
 git clone https://github.com/kaizez/directory-traversal
``` 

``` shell
 cd directory-traversal
```

### 2. Build Docker Image
- Second, Build the Docker Image
- Run the following command to build the Docker image:

```shell
 docker build -t ptraversal .
 ```

### 3. Run Container

- Thirdly, Run the Docker Container
- Once the image is built, you can run the Docker container using:
``` shell
 docker run -d -p 5000:5000 ptraversal
 ```
### 4. Verify Docker Container

- Fourthly, Verify the Flask CTF App
- Once the container is running, you should be able to access the CTF application by visiting http://localhost:5000 in your web browser.
