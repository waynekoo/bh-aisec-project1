### Go app

```shell
$ docker build -f images/echo-server/Dockerfile -t docker.io/laurentsimon/echo-server images/echo-server/
$ docker run --network=host laurentsimon/echo-server:latest
$ curl -s 127.0.0.1:8000/ -d "some-data"
```

### Flask app

```shell
$ docker build -t my-rest-server .
$ docker run -p 8081:8081 my-rest-server
$ curl -s -X POST -H "Content-Type: application/json"      -d '{"image": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="}'      http://localhost:8081/classify/v0 | jq
```