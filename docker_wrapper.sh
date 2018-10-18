#docker_wrapper.sh

echo "## rebuilding docker-compose"
_cmd="docker-compose --file ./docker-compose.yml up -d --force-recreate"
echo "> ${_cmd}"
/bin/bash -l -c "${_cmd}"