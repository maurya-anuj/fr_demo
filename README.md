# fr_demo


### Cloud steps:
- clone repo in GOPATH:
    ```
    https://github.com/maurya-anuj/kubeedge.git
    ```
- check kubernetes master is not running
	```
	kubeadm reset
	```
- check wifi connection

- make and run kubeedge init from cloned repo:
	```
	./kubeeadge init
	```
- check training image is locally present. If not get it via:

	1> from docker hub:
	
         docker pull anujmaurya/training:1
         docker tag anujmaurya/training:1 training:2
        
    2> OR, build it with base-docker then create_docker folder of [demo repo](https://github.com/maurya-anuj/fr_demo).
       
        cd /home/src/
        cd fr_demo/demo/demo_docker/
        docker build -t demo-docker:1 ./
        cd ../create_docker/
        docker build -t training:2 ./
        
- make and run edgecontroller from cloned repo:


### Edge steps:
- run: **xhost +local:user:root**
- download edge release version from
    [kubeedge-v0.3.0-beta.0](https://github.com/kubeedge/kubeedge/releases/download/v0.3.0-beta.0/kubeedge-v0.3.0-beta.0-linux-amd64.tar.gz)

- clone demo repository in $GOPATH/src/
    ```oraclesqlplus
    git clone https://github.com/maurya-anuj/fr_demo.git
    ```
- copy certificates to /etc/kubeedge/certs from [demo repo](https://github.com/maurya-anuj/fr_demo/tree/master/certs)
- copy data folder from demo repository to /etc/kubeedge/

- check the ip of edgecontroller in conf/edge.yaml
    ```
    vi /home/root1/go/src/github.com/kubeedge/kubeedge/edge/conf/edge.yaml
    ```
- check recog image is locally present. If not get it via:
	1> from docker hub:
   
         docker pull anujmaurya/recog:1
         docker tag anujmaurya/recog:1 recog:1
    
    2> OR, build it with base-docker then recog_docker folder of [demo repo](https://github.com/maurya-anuj/fr_demo).
       
        cd $GOPATH/src/fr_demo/demo/demo_docker/
        docker build -t demo-docker:1 ./
        cd $GOPATH/src/fr_demo/demo/recog_docker/
        docker build -t recog:1 ./
       
- run the repository and push recog:1 image in localhost:5000/facerecog:1
	[https://docs.docker.com/registry/deploying/](https://docs.docker.com/registry/deploying/) 
	```
    docker run -d -p 5000:5000 --restart=always --name registry registry:2
    
    docker tag recog:1 localhost:5000/facerecog:1
    docker push localhost:5000/facerecog:1
    
    docker image remove recog:1
    docker image remove localhost:5000/facerecog:1
    
    docker pull localhost:5000/facerecog:1
    ```

- run edge & check node is ready.


## Start the apps:
- apply recog.yaml from cloud
	```
	    kubectl apply -f /home/src/fr_demo/demo/recog.yaml
    ```
- apply the create.yaml from cloud
	```
	    kubectl apply -f /home/src/fr_demo/demo/create.yaml
	```   


### IF kubeedge init breaks
- check edgecontroller is not running
    ```
    ps -ef | grep edgecontroller
    ```
- clear iptables
    ```
    iptables -F && iptables -t nat -F && iptables -t mangle -F && iptables -X
    ```
### IF pod deployment fails:
- xhost +local:user:root is applied
- image name matches in yaml and local docker images.