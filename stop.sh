echo "Stopping containers"
docker stop $(docker ps -q)
