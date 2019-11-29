#!/usr/bin/env bash

set -e

docker-compose up --build --exit-code-from martinez

STATUS=$?

docker-compose down --remove-orphans

if [[ "$STATUS" -eq "0" ]]; then
	echo "tests passed";
else
	echo "tests failed to pass"
fi

exit ${STATUS}
