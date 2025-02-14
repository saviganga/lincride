# lincride

## Setup

### Prerequisites

To run the development environment, you need to have the following installed:

- **Python**
- **Docker**
- **Docker Compose**
- **Environment Variables**

### Environment Variables

A `.env.example` file has been added to the repository. You should create a `.env` file and fill in the required fields with your values to configure your environment. The `ENVIRONMENT` field has been prefilled to suit the configurations on the application.


## Run the project

1. Clone the repository
```bash
git clone git@github.com:saviganga/lincride.git
```

2. Set up your `.env` file
```bash
cd lincride/
cp .env.example .env
```
Fill the .env file with your values

3. Build the project using `docker-compose`
```bash
docker-compose build
```

4. After the build is completed, start the project with `docker-compose`
```bash
docker-compose up
```


5. Run migrations
```bash
docker ps # get the list of running containers (take note of the container id)
docker exec -it <container_id> bash # access the shell of the running lincride container
python manage.py makemigrations
python manage.py migrate
```


6. Run tests
```bash
docker ps # get the list of running containers (take note of the container id)
docker exec -it <container_id> bash # access the shell of the running lincride container
python manage.py test
```

The documentation for this project can be found in the `docs.md` file.
