# remove exited containers
# sudo docker rm -v $(docker ps --filter status=exited -q)
sudo docker rm --force flooke_server
# remove dangling images
# sudo docker rmi $(sudo docker images -f 'dangling=true' -q) -f
# sudo docker rmi $(sudo docker images) -f
sudo docker rmi flooke-server-image -f
sudo docker compose up -d --remove-orphans