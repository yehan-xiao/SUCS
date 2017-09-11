# Semi-Automatic Utility Classification System (SUCS)

## Introduction

Semi-Automatic Utility Classification System (SUCS) is a system that is designed to automate the discovery, mapping and documentation of key city infrastructure items (referred to as "Street Furniture" and "Utilities" throughout this document) through the analysis of commercially available, street-level imagery.

SUCS utilises deep-learning based approaches to identify these key infrastructure items, allowing for the automated discovery and mapping of these items.

In doing so, the aim of SUCS is to allow city planners and infrastructure designers to quickly and accurately map a city's current infrastructure.

Visit the Project's [Wiki](https://gitlab.com/mrpike/SUCS/wikis/home) page for more information.


## System Composition

SUCS consists of 3 parts: 

**The front-end system** is the web interface.

**The main server** is the middle layer connecting the database, frontend system, image analysis server and map engine provided by Baidu, Google and OpenStreetView. 

**The image analysis server** is responsible for running image analysis algorithm.


## Core utility detection model training

The detection model in SUCS is based on Faster-RCNN detection algorithm and ResNet-50 deep neural network.

Through training with a dataset of 1299 manhole cover images, the detection accuracy of the model reaches 76.7% on the testset. SUCS just uses this model.

For your convenience, please check [Utility Detection Tool](https://github.com/yehan-xiao/utility-detection-tool.git) to see the details of training deep-learning model.


## Requirement:

**The front-end system:** Any web browser

**The main server:** python, MySQLdb, Webpy, Zip.js

**The image analysis server:** py-R-FCN (CUDA, cuDNN, pycaffe)


In installation steps, SUCS will install these requirement automatically except **CUDA** and **cuDNN**.

-------
Just for reference and troubleshooting:

CUDA: https://developer.nvidia.com/cuda-downloads

cuDNN: https://developer.nvidia.com/cudnn

Zip.js: https://gildas-lormeau.github.io/zip.js

py-R-FCN: https://github.com/Orpine/py-R-FCN


## Installation

The main server and the image analysis server can be arranged in one server or two different servers.

### The main server

1. Clone project code and install the dependencies

	    git clone git@gitlab.com:mrpike/SUCS.git
	    cd SUCS/main_server
	    chmod +x *.sh
	    ./setup.sh


2. Create a database and some tables  
(Since SUCS needs to store caches when the system runs, we need to creat a database.)
	    
	    #login to mysql
	    mysql -u[username] -p[password]
	    
	    CREATE DATABASE db_SUCS;
	    source create_database.sql
	       
	    
3. Modify SUCS/main_server/config.py according to your set.

	    #image analysis server adrress
	    __C.ADDRESSES
	    
	    #mysql username and password 
	    __C.USERNAME
	    __C.PASSWORD



### The image analysis server

1. Clone project code and install the dependencies

		#comment it when set up these two parts in one server
	    git clone git@gitlab.com:mrpike/SUCS.git    
	    
	    cd SUCS/image_analysis_server
	    chmod +x *.sh
	    ./setup.sh

2. Download directory manhole_net from [here](http://pan.baidu.com/s/1eR4wU1G) and put the whole directory into image_analysis_server.

	    #directory structure
	    SUCS
	    	|______image_analysis_server
	    					|______py-R-FCN
	    					|______images
	    					|______log
	    					|______manhole_net



## Running

### The main server

	    python main.py

### The image analysis server

	    python main.py
	    
### The webiste
1. Open web browser and input 

   address: [main_server_address]/static/login.html

2. Access with
 	
 	username: root
 	
 	password: root

## User Guide
**See [User Guide](https://github.com/yehan-xiao/SUCS-wiki/blob/master/general/user_guide.md) to learn how to use SUCS.**

## License

UCS is released under the MIT License (refer to the LICENSE file for details).
