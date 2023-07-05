# Django Test Project

This is a test project built with Django. It aims to demonstrate skills Django usage. Please note that this project does not utilize Docker Compose and is intended for interview purposes only.

## Prerequisites

Make sure you have the following dependencies installed on your local machine before proceeding:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Python 3: [Install Python](https://www.python.org/downloads/)

## Getting Started

To run this Django application using Docker, follow the steps below:

1. Clone this repository to your local machine using the following command:

```bash
git clone https://github.com/DopeySlime/DjangoTestProject.git
```

2. Navigate to the project's directory:

```bash
cd DjangoTestProject
```

3. Build the Docker image by running the following command:

```bash
docker build -t django-docker-test .
```

4. Start a Docker container using the built image:

```bash
docker run -p 8000:8000 django-docker-test
```

5. Once the container is up and running, you can access the Django application by opening your web browser and visiting [http://localhost:8000](http://localhost:8000).

## Development

If you wish to modify the Django application and see the changes reflected in real-time, follow the steps below:

1. Install the project dependencies using Poetry:

```bash
poetry install
```

2. Make the desired changes to the Django application.

3. Activate the Poetry environment:

```bash
poetry shell
```

4. Run the Django development server locally:

```bash
python manage.py runserver
```

5. You can now access the Django application at [http://localhost:8000](http://localhost:8000) and see your changes.

Note: By using Poetry, the project dependencies are managed within a virtual environment specific to this project.

## Acknowledgments

This project was created as a test project for an interview.