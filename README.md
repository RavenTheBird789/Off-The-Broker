# Off-The-Broker
CLI tool that automates opt-out requests to databrokers via email

![Alt text](images/1000001096.jpg)

Prerequisites:
1. Ensure the latest version of python in installed in your terminal (python 3.x)
2. Ensure you have a virtual env for the required python library (If you don't, one can easily be created by executing the command "python3 -m venv env")
3. Create an app password for your Google account that'll be used as the value for one of your .env variables

Installation & Execution:
* To install, simply type "https://github.com/RavenTheBird789/Off-The-Broker" in your terminals command line

1. After installing, use the command "cd Off-The-Broker" to enter the Off-The-Broker directory
2. Once in the directory, activate your env with the command "source env/bin/activate"
3. After your env is activated, run the command "pip install -r requirements.txt" to install the required library

* To run, simply type "python3 broker.py" in your terminals command line or use the bash alias command to create a shortcut to run the program in your terminal such as "alias broker="python3 broker.py""

![Alt Text](images/1000001090.jpg)

Notes:
* KeyboardInturrupt (Ctrl + C) can be used to terminate the program easily within the terminal session
* It is highly recommended to use a burner email/Google account for the sender email input field that'll be stored in the .env text file as the value for the SENDER_EMAIL variable
* A rate limit of 150 emails is implemented into the tool to prevent your email from being flagged as spam
