# Cloud-CA

This repo is dedicated to a Cloud Platform Development Module in College

# Running Structions

To run the script the very first thing is to set up a google cloud account, if you are a new user you can get 300 euros to use for a few months.

Create a new Project and next, for this to run properly we need to enable the APIS, basically you go to google cloud, click on APIs and Services, you should find "VM Instances", then enable the API.

Next, you need to set up your environment, download google cloud sdk.
I personally like VS Code, so once the google cloud is installed you can install vs code.

Then, we gonna run the command, gcloud init, then option 1 for "Re-initialize this configuration" with new settings, next, you have to select your account and after that, you've already created the project so just select it.

The script was created in Python, so to run this we need to install python as well.

Once all the steps above are done, you can go to the folder that contains the script.py

Then we run using "py script.py"

Once the process is complete, we can go back to google cloud to check the VM running.

You can click on SSH and allow it to open, and we're gonna run the following commands:

sudo apt-get update - this command will update the package lists on our VM
sudo apt-get install apache2 php7.0 - this command will install Apache2 HTTP Server
echo '<!doctype html><html><body><h1>Hello World!</h1></body></html>' | sudo tee /var/www/html/index.html - this one will overwrite the apache web server, we can leave Hello World or type in something else.

Once everything is done, you can check the External IP for your vm, e.g 34.105.164.215
Then open up a new tab and paste this IP, you should see the HTML.

Thanks!

Student Name - Thiago Silva Moreira
SN - 10600338
