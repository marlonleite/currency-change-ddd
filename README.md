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
This command builds and runs the project.

To just run the project after building:
`$ make run` or `$ make up` verbose

To stop the project:
`$ make down`

To restart the project:
`$ make restart`

To migrate data to the database:
`$ make makemigrations`
`$ make migrate`

There are other commands inside the Makefile map. They are helpful for developers to debug their code.

## Docs

You can find the Swagger Documentation OAS3. The project will be available at `http://localhost:8080/docs`.

## Test and Quality Assurance

You can run all the tests at once...

`$ make test` or `$ make test_v` verbose or `$ make report` covarage.

## Github Action

There is a GitHub action workflow to check the code quality helper in pull_request.
