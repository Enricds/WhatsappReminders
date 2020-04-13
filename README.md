# WhatsappReminders
## Sending reminder messages through Whatsapp using Twilio and Functions in IBM Cloud

These are the instructions to create, starting from scratch, a simple application to send periodic reminder messages through whatsapp using Twilio and Functions in the IBM Cloud. Twilio makes it very easy to send whatsapp messages and Functions (OpenWhisk-based) makes it very easy to create an app without worrying on server configurations and execute the app based on many types of triggers. The cost for this use case is 0. If the number of messages you send grows both Twilio/WhatsApp and Functions may require some investment.

There are limitations when using the Twilio Whatsapp Sandbox. One of them is that if the end user (whoever receives the messages) doesn't answer something in 24h, the sending of messages is disabled (to avoid spam, obviously).

NOTE: This is not meant for serious production environments. If that's the case you'd probably need to work with Twilio/WhatsApp Business (although the code would be basically the same)

(I'll use the convention of preceding all commands with a $ and put them in _italics_)

## Prepare the tools you need

I'm going to assume you have a laptop where you'll do your coding. I have a Mac so my examples will be based on that platform but you can find Linux/Windows equivalents easily.

### You need an editor to code (just a little bit)

I use VSCode (https://code.visualstudio.com/) but this application is very simple so any text editor will do. I like Atom for example, which is simpler than VSCode and also for free: https://atom.io/ (If you want to use Atom, it's very handy to install "Shell Commands" so that you can open atom from terminal command line: just open the atom application, in the Menu go to Atom-> Install Shell Commands. Now you can write atom <file> from any terminal)

### You need a Twilio account and a Twilio WhatsApp Console

Just register here: https://www.twilio.com/try-twilio

Twilio has a nice WhatsaApp SandBox console, very easy to use, and for what we want is more than enough. Once you have registered, go to the Whatsapp Twilio console and follow the instructions:

https://www.twilio.com/console/sms/whatsapp/learn

Then go to the console Dashboard and make sure you take note of: 

Be sure to take note of:
*  _Account SSID_ (that's just a way to identify your account)
*  _Auth Token_  (that's just a "password" to access your account)

and also (from the previous step):
*  _Telephone that sends_ the Whatsapp  (will be a +1... number)
*  _Telephone that receives_ the Whatsapp  (your phone, for example)

(The full tutorial is here in case you want to learn more, but not necessary: https://www.twilio.com/docs/whatsapp/quickstart/python)

### Prepare the runtimes so that your application works on your laptop

You need the python and twilio libraries in your laptop to run and test the application. You just need to install them.

(you may want to install Anaconda if you plan to have multiple development environments but it's really not necessary)

Install _Homebrew_ (if you don't have it). It's a Mac package manager that will save you a lot of time and make installation of most runtimes really easy. (https://brew.sh/)

Just open a Terminal and execute:   
_$ /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"_   
(remember to also execute this so that the Homebrew directory is accessible: _$ export PATH="/usr/local/opt/python/libexec/bin:$PATH"_)

Once you have Homebrew in place, install python as easy as this: _$ brew install python_

Now install Twilio, very easy also once you've done the previous: _$ pip install twilio_

Now you can start coding your application.

## Code your application and test it locally before uploading to the cloud

The application has the following parts, all them in this GitHub:

* _Missatge.py_: This has the logic of the application
* _SampleParms.json_: This has the information (telephones, account,...) that we don't want to put directly in the application code. 
* _Dockerfile_: This is the Docker file that will contain the Twilio (and a couple more) runtimes. You don't need it for the local testing but you need it to upload the app into Cloud.

Create a directory in your laptop for this project and copy these files to your environment (for example click the "Clone or download" button in the GitHub repo, donwload as a zip and put the files in the newly created directory)

Rename _SampleParms.json_ to _parmsPackage.json_, open the file, fill it with your values.

Test you application using a terminal and the following command (you must be in the project directory): 

_$ python -c 'import Missatge; Missatge.main(0)'_  (you should receive a message through Whatsapp)

You can go to the Twilio Console and see what happens to your messages (beware that you can only send messages to phones that have "joined" your account, in the Console it explains how): https://www.twilio.com/console/sms/logs

Once you are happy with the basic sending of messages, we'll put the application in the Cloud and define when we want to trigger it but before we need to prepare a Docker image with the runtimes we need. 

## Prepare a Docker image with the runtimes that the application uses so that we can move them to the Cloud

If you don't have it, install Docker: https://docs.docker.com/docker-for-mac/install/ 

Create a DockerHub Account (this is where the image will be made available so that we can get it from Cloud): https://hub.docker.com/   
In DockerHub, create a **public** repository, for example, _whatsappruntime_ (must be lowercase)

From the terminal and in your project directory create the Docker image:   
 _$ docker build -t_ <your_dockerhub_user>/whatsappruntime:inicial .  (don't forget the "." at the end of the command!)
 
 This will use Dockerfile to create the image. The image will be stored in Docker local repository, don't expect to see it in the directory

Now send the Docker image with your runtimes to DockerHub so that it can be retrieved from the Cloud (you may have to _$ docker login_ first): 
_$ docker push <your_dockerhub_user>/whatsappruntime:inicial_

## Get an IBM Cloud free account

Just register here: https://cloud.ibm.com
The Service that you'll be using is called "Functions": https://cloud.ibm.com/functions/

You can take a look to all this through the IBM Cloud Console but I'd recommend to use commands from you terminal to manage it

## Uploading the application to the Cloud

All the documentation to use Functions is here: https://cloud.ibm.com/docs/openwhisk?topic=cloud-functions-getting-started
And all CLI commands are here: https://cloud.ibm.com/docs/openwhisk?topic=cloud-functions-cli-plugin-functions-cli

The **basic things** you need to know are:

* Your Application will be an _Action_, that is, a piece of code that will be executed depending on a _Trigger_
* A _Trigger:_ is an event that can trigger the execution of an _Action_ (for example, in our case, certain times)
* A _Rule_ is what ties a _Trigger_ with an _Action_
* A _Package_ is a way to wrap a group of _Actions_ so that they can be managed all together (we won't use it since we only have one Action but can be useful for more complex scenarios)
* A _Namespace_ is just a "space" in your Cloud where all the Functions resources live
* A _Resource Group_ is just an administrative concept in the Cloud to manage your resources (Functions or any other thing)

The only concepts that you really need to have clear are _Action_, _Trigger_ and _Rule_


Install the IBM Cloud CLI and plug-in in your laptop, this will allow you to send commands to the Cloud from your laptop: https://cloud.ibm.com/docs/openwhisk?topic=cloud-functions-cli_install

After you install the CLI remember to install the plugin:

* Login to IBM Cloud if you have not done so before: _$ ibmcloud login_ 
* Select a Region if you have not been asked, for example, US South: _$ ibmcloud target -r us-south_ (this means your app will be executed in Dallas)
* Select a Resource Group if you have not been asked (this is just some administration requirement):
    * _$ ibmcloud resource groups_ will list your resource groups, pick one
    * _$ ibmcloud target -g default_ (I chose default)
* _$ ibmcloud plugin install cloud-functions_ (install the plugin)

Check if you have any IAM-based namespace: _$ ibmcloud fn namespace list_  
If you don't, create one, for example WhatsName: _$ ibmcloud fn namespace create WhatsName_  
Select the Namespace where you'll deploy the app and create the triggers:   
_$ ibmcloud fn property set --namespace WhatName_

Create the Action based on your app: _$ ibmcloud fn action create EnviarMissatge --docker <your_dockerhub_user>/whatsappruntime:inicial Missatge.py_

(If you change your application and want to update it just use the command: 

_$ ibmcloud fn action update EnviarMissatge --docker <your_dockerhub_user>/whatsappruntime:inicial Missatge.py_)

Create the trigger that will eventually invoke the action (the trigger will be called _periodic_):

_$ ibmcloud fn trigger create periodic  --feed /whisk.system/alarms/alarm --param cron "0 9,13,22 * * *" --param timezone "Europe/Berlin"_

(this will create an event at 9 o'clock, 13 and 22 hours. The syntax is that of cron: https://en.wikipedia.org/wiki/Cron)

(you can update the trigger schedule with: _$ ibmcloud fn trigger update periodic --feed-param cron "0 9,13,21 * * *"_)

Create a rule that links your _Action_ with your _Trigger:   
_$ ibmcloud fn rule create Rule_Periodic_EnviarMissatge periodic EnviarMissatge_   
(If you used the console to create the Action and the Trigger, a Rule is created automatically)

Check that the Rule is active with the following command: _$ ibmcloud fn rule list_

If it's not active, just activate it using: _$ ibmcloud fn rule enable Rule_Periodic_EnviarMissatge_

Just one final step and we are there. We have created an Action with our application, a Trigger to awake the action and now we need to pass the parameters to the Action (without writing them on the application). To do that, we just update the action and specify that our application parameters are in a file called paramsPackage.json:

_$ ibmcloud fn action update EnviarMissatge_ --docker <your_dockerhub_user>/whatsappruntime:inicial --param-file parmsPackage.json Missatge.py 

(yes... we could have done that at the very beginning when creating the Action for the first time)

You can check the properties of your Action with this command (you should see all the parameters): \
_$ ibmcloud fn action get EnviarMissatge_

And finally: try to force invoking the Action directly to see if it works from the Cloud: \
_$ ibmcloud fn action invoke EnviarMissatge --result_

And this should make it work. You can monitor the invocations of the action from the Cloud console in the Functions section: https://cloud.ibm.com/functions/dashboard



