# Currency Api

Register currencies and convert

## Local environment

Your local environment can be configured through and env file or using docker.

## Instalation

The `Makefile` file that exists on the project root, has all the commands mapped, from building to testing.

The project is configured to run in Docker with FastApi and Postgres and tests are configured to run in SQLite. But you can use others setups if you need.

### Commands Make and/or Docker

To build the project and run it:
```
make build
```
*This command builds and runs the project.*

To just run the docker project after building:
```
make run
```
or
```
make up
```
*verbose mode*

To stop the docker project:
```
make down
```

To restart the project:
```
make restart
```

### Database:

To create a new data migration:
```
make makemigrations
```

To migrate:
```
make migrate
```

To downgrade:
```
make downgrade
```

*There are other commands inside the Makefile map. They are helpful for developers to debug their code.*

## Docs

You can find the Swagger Documentation OAS3. The project will be available at `http://localhost:8080/docs`.

## Test and Quality Assurance

You can run all the tests at once...

To test you must run the command to enjoy in the docker container:

```
make bash
```

After that, inside the docker container:
```
make test
```

## Author

* **Marlon Leite** - [GitHub](https://github.com/marlonleite)
