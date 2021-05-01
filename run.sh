#!/bin/bash
COMMAND="$*"
if [ $COMMAND == "test" ]; then
    COMMAND="python manage.py test && flake8"
fi
echo $COMMAND
docker-compose run app sh -c "$COMMAND"