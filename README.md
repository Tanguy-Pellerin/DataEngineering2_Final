# Project Data Engineering II Final Project

### Made by Marc-Antoine BOCK & Tanguy PELLERIN

## Project Summary 

The purpose of this project is to provide a solid example of real-life application development in a DevOps environment.

The application is a Twitter search application, where the user inputs a search string, and the application returns the top 20 tweets which are similar to the search string. As result this will return the most 20 similar tweets.

## Task Management

For our team internal task management, we use Trello. We decided to use four columns: To Do, Production, Test, and Done. After he is finished, the task will be moved to To be test for another team member to check it. If the reviewer accepts the changes, he or she moves the task to Done.


## Source Code Management

We use this GitHub repository to keep track of all our changes and our version controls. For each task done, a new Branch is created. At task completion, we create a pull request (PR) in GitHub and move the task in Trello to To be test. 

## Automation
We use Jenkins for automating the building, testing, deployment and release.

We have a Jenkins pipeline constructed which connects to the different github branches, and applies appropriate respective actions:
•	build and run unit tests on feature branches.
•	stress test and push to release on the develop branch
•	wait for user acceptance on the release branch before pushing to master
•	deploy on merging with master

http://localhost:8080

## Containarization 
The final application deliverable is a Docker image, that contains the pre-trained model as well as the application web interface. The twitter dataset is also be bundled with the application. By Running the container off the delivered image allow users to view a web interface on their browser and be able to immediately start running the app.

## Monitoring and Alert our Application
We monitor multiple metrics like hardware and software metrics.
Hardware metrics: like CPU usage, memory usage, and disk space usage.
Software metrics: We integrate different software metrics inside our application to monitor information like response time, user requests count, exceptions, lantency ...

We create different alert like:
App instance is down, ApplicationException, PrometheusNotConnectedToAlertmanager ,AlertWhenAverageRequestTooktolong, HostHighCpuLoad,DiskSpace10percentFree, HighMemoryUsage

All code about monitoring and rules for alert are in prometheus.yml and rules.yml in the branch prometheus.


We use different different software to monitoring our application.
We use Prometheus, node-exporter and alertmanager and grafana
The dashboard grafana is in the grafana branch in json format.

[prometheus_download](https://prometheus.io/download/)


#### Launch different software to monitor

```bash
cd node_exporter_file_name
./node_exporter
```

```bash
cd grafana_file_name/bin
./grafana-server
```
```bash
cd alertmanager_file_name/bin
./alertmanager
```

```bash
cd prometheus_file_name
./prometheus --config.file=prometheus.yml
```

#### Different port to access

alertmanager : localhost:9093

prometheus : localhost:9090

node_exporter : localhost:9100

## Running the application 

The application needs a redis container to store the pretrained model and a flask container to serve the web interface. To start and connect both containers, we use a docker-compose file (see docker-compose.yaml). As a prerequisite, you need to have Docker installed on your machine.

To start the whole application, navigate to the folder in which the docker-compose.yaml can be found. From there, execute the following command:

```bash
docker compose up
```

to stop the application

```bash
docker compose down
```

You can visit the website, for the user interface locally under http://0.0.0.0:5000/ or http://localhost:5000/. 
