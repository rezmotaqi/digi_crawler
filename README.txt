
Run locally outside of docker
python3 -m venv venv
source ./venv/scripts/activate (in linux)
pip install requirements.txt
python3 -m ./main.py

To run tests
python3 -m tests.py

Run (using docker )
docker image build . --tag crawler:0.1
docker-compose up -d
