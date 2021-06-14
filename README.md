# test_flask_app

Application implement a simple Rest API using Python Flask framework.
This service is to calculate distance between several locations giving human-readable addresses for each point.

The application was developed on ubuntu 20.04 with python3.8

To install and running the application, you need to run the following commands for Ubuntu:

# Install virtual environment for python
> sudo apt install python3-venv

# Edit flask.service file and after to run the following commands
> sudo cp flask.service /etc/systemd/system

> sudo systemctl daemon-reload

> sudo systemctl enable flask

> sudo systemctl start flask

# After, you can use the service using command line tools like cURL
## for upload data:
> curl -i -X POST -H "Content-Type: multipart/form-data" -F "data=@points.csv" http://127.0.0.1:5000/api/calculateDistances
## for retrieve a single stored task result object
> curl http://127.0.0.1:5000/api/getResult?task={task_uuid}
