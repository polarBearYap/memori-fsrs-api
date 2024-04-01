# Memori Django API
Web API that implements the open source Free Spaced Repetition Scheduler (FSRS) algorithm to support learning scheduling of FSRS API.

## Dev Requirements
1. Python >= 3.11
2. Docker

## Libraries
1. Django REST framework

## Getting Started
1. Set a new Django secret key in the .env file.
```
SECRET_KEY = "your_secret_key_here"
```

2. Create a python virtual environment for local development and testing, using the given requirements.txt.
- Create a venv at your desired location.
```
python3 -m venv yourenvname
```
- On Windows, run:
```
yourenvname\Scripts\activate
```
- On Unix or MacOS, run:
```
source yourenvname/bin/activate
```
- Lastly, install the required packages.
```
pip install -r requirements.txt
```

3. Run the test.
```
pytest -s
```

4. Run the command below to start the API with default port number 8000. 
```
python manage.py runserver
```

5. Run the curl command below to validate the app.
```
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"due": "2024-02-17T17:49:24Z", "stability": 0.7596866918143955, "difficulty": 0.1299008959107234, "elapsed_days": 5, "scheduled_days": 2, "reps": 5, "lapses": 5, "state": 2, "last_review": "2024-02-05T09:23:17Z", "current_review": "2024-02-17T17:49:24Z"}' \
  http://localhost:8000/scheduleusercard
```

6. Run the command below to run in Docker.
```
docker build -t fsrs_api:1.0 .
```
- You may specify a location to bind the log file.
```
docker run -d --rm -p 8000:8000 -v /your_desired_location_logs:/app/logs fsrs_api:1.0
```

## Acknowledgement

1. The FSRS algorithm implementation is accredited to this open source python package [(links)](https://github.com/open-spaced-repetition/py-fsrs)

## License

Distributed under the MIT License. See LICENSE for more information.
