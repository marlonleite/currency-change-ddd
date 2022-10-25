#!/bin/bash


echo $ENVIRONMENT
echo $TARGET

# development
if [[ $ENVIRONMENT == "development" ]]; then
    if [[ $TARGET == "api" ]]; then
        python -m alembic upgrade head;
        python -m uvicorn src.entrypoints.rest_application:get_app \
            --host 0.0.0.0 --port 8080 --reload --factory
    else
        echo "Unkown TARGET: $TARGET"
    fi


# Production
elif [[ $ENVIRONMENT=="production" || $ENVIRONMENT=="homolog" ]]; then
    if [[ $TARGET == "api" ]]; then
        python -m alembic upgrade head;
        python -m gunicorn --bind :8080 \
            --workers 1 --threads 8 --timeout 0 \
            -k uvicorn.workers.UvicornH11Worker \
             src.entrypoints.rest_application:get_app
    else
        echo "Unkown TARGET: $TARGET"
    fi

else
    echo "Unkown environment: $ENVIRONMENT"
fi
