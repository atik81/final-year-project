

Flask Application Setup
First things first, let's get the Flask application up and running.

#######       1st step  #########
 Environment Setup 
Start by cloning the repository and setting up your environment:
Create a .env file in the root directory.

Save your YouTube API key in the .env file 

API_key=***

apiKey = '**'
with the variable name API_KEY.
Running the Flask App
To start the Flask app, you'll need to run the following command from the root directory:   flask --app app run

###################### 3nd step #############

Virtual Environment (venv)
Using a virtual environment is crucial for managing dependencies without affecting your global Python setup.

If you've just cloned the repository, set up a new virtual environment:

python -m venv venv

To activate the virtual environment, 

venv/Scripts/Activate.ps1

(This command might vary depending on your OS and shell)
With the environment active, install the required packages:


pip3 install -r requirements.txt


Remember to navigate into the extension directory before starting the Flask app.


############ last step############


Chrome Extension Manual Upload
To load the YouTube Video Analyzer Extension into Chrome, you'll need to:

Open the Chrome Extensions page by navigating to chrome://extensions/ in your browser.
Enable Developer mode by toggling the switch in the top-right corner.
Click on Load unpacked and select the extension directory from your project files. This will manually load your extension into Chrome for testing and use.



if you face any error for upload this file in extension you need to delete __pycache__ file from code i did this one security