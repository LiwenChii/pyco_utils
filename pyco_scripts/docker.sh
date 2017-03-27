


#stop all container

docker stop $(docker ps -a -q)

#remove all container

docker rm $(docker ps -a -q)

# remove all exited container

docker ps -a | grep Exit | cut -d ' ' -f 1 | xargs docker rm

# remove all none image

docker rmi $(docker images | grep "^<none>" | awk "{print $3}")



####
# python 官方
https://hub.docker.com/_/python/
# slim
# alpine
# wheezy(debian)
# onbuild
# windowsservercore
#

$ docker run -it --rm --name {NAME} -v "$PWD":/usr/src/myapp -w /usr/src/myapp python:3 python {{manage.py}}