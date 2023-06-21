# Stark Skill Test
The server is hosted by an AWS EC2 instance at http://starkbank-skilltest.info.
It is composed of a django application served by nginx as a reverse proxy.

*NOTE*: In the given time to complete the task, I didn't finish aquiring the needed SSL certificate necessary to secure the site with https. For that reason, the setup to receive the webhook isn't functional. Since the starkbank sandbox API doesn't accept non-encrypted URLs, I would need more time to properly secure the webhook endpoint.

### Functionality
This application uses the `django_cron` module to schedule the issuing of 8-12 invoices during a 24h period.
The webhook was created using the starkbank sandbox environment with an `invoice` subscription. The value of the paid invoices (minus fees) is then transfered to a specified account.

### Infrastructure
The deployed instance consists in 2 docker containers that comunicate with each other through a unix socket. The first container is running a django-uwsgi worker process that interacts with the nginx web server to serve dynamic content. The containers communicate using shared docker volumes on the main file system.

![image](https://github.com/bennymirahy/stark_skilltest/assets/40213163/e23a8ee6-7490-4ff6-a9fc-b3259e98334b)

### Getting started

After cloning the repository, set up a python virtual environment and install the dependencies. The python version used was python3.11.2.
`pip install -r requirements.txt`

The dev_utils.sh script has some useful functions to ease the setup. 
Make sure it is executable.
`chmod +x dev_utils.sh`
And source the contents.
`. dev_utils.sh`

*NOTE*: You must configure the host of the EC2 instance in the `dev_utils` script to properly execute the functions that use ssh to interact remotely.

Ajust the script according to your setup of the file system.

Notice that the `redeploy` function syncs the production server's code with yours, builds the docker image and remotely executes `dkintegration-server.sh`.

For this, create the script with the following commands:

```docker stop integration-server
docker rm integration-server
docker run -d --restart=unless-stopped \
       --name=integration-server \
       -v /home/ubuntu/dkdata/integration-server/uwsgi:/uwsgi \
       -v /home/ubuntu/dkdata/integration-server/private-key:/private-key \
       --env-file=/home/ubuntu/integration-server.env \
       -e PRIVATE_KEY=<your starkapi sandbox private key> \
       integration-server start.sh
 ```
`dkdata/integration-server/uwsgi` is the path of your unix socket and the application's static files

Use the env file to pass environment variables to the container. 

To set up a private key, access https://starkbank.com/sandbox.

ssh on to the hosted instance and run the following script to execute the following script:

```docker stop nginx
docker rm nginx
docker run -d --restart=unless-stopped \
       --name=nginx -p 80:80 \
       -v /home/ubuntu/dkdata/nginx:/etc/nginx \
       -v /home/ubuntu/dkdata/nginx/conf.d:/etc/nginx/conf.d \
       -v /home/ubuntu/dkdata/nginx/include:/etc/nginx/include \
       -v /home/ubuntu/dkdata/integration-server/uwsgi:/uwsgi_integration-server \
       nginx
```

Notice the common mapping of volumes between the 2 containers.

According to the script, the nginx configuration files for this app should be at `~/dkdata/nginx`.

