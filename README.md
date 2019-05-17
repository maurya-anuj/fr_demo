# fr_demo


### Setup steps:
- check kubernetes master is not running
	```
	kubeadm reset
	```
- check wifi connection

- run kubeedge init
	```
	./kubeeadge init
	```

- check certificates path of edgecontroller then make and run it from:
    ```
        cd /home/src/github.com/kubeedge/kubeedge/cloud/
    ```
- apply the create.yaml checking that training:1 image is available in local
	```
	kubectl apply -f /home/src/fr_demo/demo/create.yaml
	```

- Edge side
- check the certificates folder in /etc/kubeedge/certs
- check the ip of edgecontroller in conf/edge.yaml
    ```cassandraql
    vi /home/root1/go/src/github.com/kubeedge/kubeedge/edge/conf/edge.yaml
    ```
- check recog image is locally present. If not get it via:
	- from docker hub:
        ```
         docker pull anujmaurya/recog:1
        ```

    - build it with base-docker then rocog_docker folder of demo repo.
        ```
        cd /home/src/fr_demo/demo/demo_docker/        - build it with base-docker then rocog_docker folder of demo repo.
        docker build -t demo-docker:1 ./
        cd /home/src/fr_demo/demo/create_docker/
        docker build -t training:1 ./
        ```
- run the repository and push recog:1 image in localhost:5000/facerecog:1
	[https://docs.docker.com/registry/deploying/](https://docs.docker.com/registry/deploying/) 

- run edge & check node is ready.
- apply recog.yaml from cloud
	```
        kubectl apply -f /home/src/fr_demo/demo/recog.yaml
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