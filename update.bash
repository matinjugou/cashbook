docker build -t cashbook:latest .
docker stop cashbook
docker rm cashbook
docker run --name=cashbook -p 30001:5000 -d cashbook
