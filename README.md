# CodeReviewAI

## How to run

Python should be installed
```commandline
git clone github.com/mdubyna/CodeReviewAI
cd  CodeReviewAI
pip install poetry
poetry init
poetry install
poetry python app.py
```

## Run with docker

- Docker should be installed
- Docker compose should be installed
- Copy .env.example -> .env 
```
docker-compose up --build
```
You can try it here http://127.0.0.1:8000/docs or http://127.0.0.1:8000/review

## Part 2: What if

- Consider utilizing a database to track token usage within the repository, enabling analytics and planning for the appropriate OpenAI Tier subscription.
- Under heavy application loads, we could scale horizontally by incorporating Nginx/Kubernetes or leveraging cloud infrastructure such as AWS ALB and AWS ECR/ECS.
- To avoid rate limit errors in GitHub integration, implementing a queue would be beneficial. Following GitHub’s best practices, sequential requests are preferred over parallel ones to prevent rate limit overload.
- For OpenAI integration, it’s essential to calculate not just the number of requests but also the token count. Additionally, attention should be paid to the usage limit, which imposes monthly cost constraints based on the selected Tier.
- Implementing functionality to review only specific parts of the code, such as the first 500 characters of a file, could help reduce token consumption.
- For cost efficiency, batching requests with a 24-hour response time may be worth considering, as it reduces the request price by 50%.
