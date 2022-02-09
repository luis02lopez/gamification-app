# gamification-app
This application envelop all the gamification ideas from the Engineer Margarita Gamarra

Steps to deploy:

docker buildx build --platform linux/amd64 -t gamification-cuc .
docker tag gamification-cuc registry.heroku.com/gamification-cuc/web
heroku container:login
docker push registry.heroku.com/gamification-cuc/web
heroku container:release web -a gamification-cuc