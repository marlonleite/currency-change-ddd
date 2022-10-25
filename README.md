# Currency Api

Register currencies and convert

## Local environment

Your local environment can be configured through and env file or using docker.

## Instalation

The `Makefile` file that exists on the project root, has all the commands mapped, from building to testing.

To build the project and run it in docker:
`$ make build`

To just run the project after building it in docker:
`$ make run` or `$ make up`

## Docs

You can find the Swagger Documentation OAS3. The project will be available at `http://localhost:8080/docs`.

## Test and Quality Assurance

You can run all the tests at once...

`$ make test` or `$ make test_v` verbose.
