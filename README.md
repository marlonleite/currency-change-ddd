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

## Documentation

You can find the Swagger Documentation OAS3. The project will be available at `http://localhost:8080/docs`.

 ### Entrypoints
```
 - GET /api/v1/healthcheck
 - GET /api/v1/currencies
 - POST /api/v1/currencies
 - DELETE /api/v1/currencies/{item_id}
 - GET /api/v1/currencies/convert/{code}/{amount}
```

## Test and Quality Assurance

`$ make test` or `$ make test_v`
