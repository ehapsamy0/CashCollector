
# cash_collector

A cash collection application


### Entity Relationship Diagram (ERD):
![alt erd](https://github.com/ehapsamy0/CashCollector/blob/main/erd/digram.jpeg)


[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

## Settings

Moved to [settings](http://cookiecutter-django.readthedocs.io/en/latest/settings.html).

## Basic Commands

### Setting Up Your Users

- To create a **normal user account**, just go to Sign Up and fill out the form. Once you submit it, you'll see a "Verify Your E-mail Address" page. Go to your console to see a simulated email verification message. Copy the link into your browser. Now the user's email should be verified and ready to go.

- To create a **superuser account**, use this command:

      $ python manage.py createsuperuser

For convenience, you can keep your normal user logged in on Chrome and your superuser logged in on Firefox (or similar), so that you can see how the site behaves for both kinds of users.

### Type checks

Running type checks with mypy:

    $ mypy cash_collector

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    $ coverage run -m pytest
    $ coverage html
    $ open htmlcov/index.html

#### Running tests with pytest

    $ pytest

### Live reloading and Sass CSS compilation

Moved to [Live reloading and SASS compilation](https://cookiecutter-django.readthedocs.io/en/latest/developing-locally.html#sass-compilation-live-reloading).

### Celery

This app comes with Celery.

To run a celery worker:

```bash
cd cash_collector
celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd cash_collector
celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd cash_collector
celery -A config.celery_app worker -B -l info
```

### Sentry

Sentry is an error logging aggregator service. You can sign up for a free account at <https://sentry.io/signup/?code=cookiecutter> or download and host it yourself.
The system is set up with reasonable defaults, including 404 logging and integration with the WSGI application.

You must set the DSN url in production.

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](http://cookiecutter-django.readthedocs.io/en/latest/deployment-with-docker.html).

### Makefile Commands

You can use the following make commands to build and manage your Docker project:

- **Build and Up**: Build and start the Docker containers.
    ```bash
    make upbuild
    ```

- **Up**: Start the Docker containers.
    ```bash
    make up
    ```

- **Build**: Build the Docker containers.
    ```bash
    make build
    ```

- **Run**: Run a command in a new container.
    ```bash
    make run <command>
    ```

- **Restart**: Restart the Docker containers.
    ```bash
    make restart
    ```

- **Shell**: Open a Django shell.
    ```bash
    make shell
    ```

- **Bash**: Open a bash shell in the Django container.
    ```bash
    make bash
    ```

- **Make Migrations**: Create new database migrations based on the models.
    ```bash
    make makemigrations
    ```

- **Migrate**: Apply the database migrations.
    ```bash
    make migrate
    ```

- **Make Messages**: Create translation messages.
    ```bash
    make makemessages
    ```

- **Compile Messages**: Compile translation messages.
    ```bash
    make compilemessages
    ```

- **Superuser**: Create a new superuser.
    ```bash
    make superuser
    ```

- **Show URLs**: Show all registered URLs.
    ```bash
    make urls
    ```

- **Logs**: View the logs of the Docker containers.
    ```bash
    make logs
    ```

- **Test**: Run the test suite with Django settings for testing.
    ```bash
    make test
    ```

- **Test Local**: Run the test suite inside the running Django container.
    ```bash
    make test_local
    ```

- **Pytest**: Run tests with pytest.
    ```bash
    make pytest
    ```

- **Mypy**: Run type checks with mypy.
    ```bash
    make mypy
    ```

- **Debug**: Run a command in a new container with service ports enabled.
    ```bash
    make debug <command>
    ```

- **Down**: Stop and remove the Docker containers.
    ```bash
    make down
    ```

- **Destroy**: Stop and remove the Docker containers, volumes, and networks.
    ```bash
    make destroy
    ```

- **Remove Pyc**: Remove Python bytecode files.
    ```bash
    make rm_pyc
    ```
