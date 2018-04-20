# SyscoSocialMedia
This repository contains the source code to do a quick influencer model for a given twitter account.  
Quick run instructions:
* clone the master repository branch ```git clone https://github.com/albre116/SyscoSocialMedia.git```
* build the docker environment/conainers ```docker-compose build```
* fill in your twitter accounts details in the example keys.example and rename to keys.secret
* source the keys into the environment prior to deploy ```source keys.secret```
* deploy the jupyter notebook on port 8888 ```docker-compose up -d ```
* the password to the notebook is `Normal`