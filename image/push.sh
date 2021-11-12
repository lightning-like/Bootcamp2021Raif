docker build . -t millionaire
docker tag millionaire curisca/millionaire:latest
docker push curisca/millionaire:latest