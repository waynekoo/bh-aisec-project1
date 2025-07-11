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

### Build requirements.txt for classifier

```shell
$ docker build -t requirements -f Dockerfile_requirements .
```

### Build classifier

Use images from https://huggingface.co/datasets/ylecun/mnist.

```shell
$ docker build -t my-rest-server .
$ docker run -p 8081:8081 my-rest-server
$ curl -s -X POST -H "Content-Type: application/json"      -d '{"image": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wAALCAAcABwBAREA/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/9oACAEBAAA/APn+tXQvDWteJbv7No2mz3kg+95a/Kv+8x4H4mrninwTrvg5rQazbJELpC0bRyLIuQcFSVOMjj8656iva/COq/EXV/AsGheGdHtNL09YTGdSfMRnJbBKOxwWOcZAP1HFZnxWsm8O+CvBnhi6z/aNnFNNPgEoC7A8N0POen9RXk9dZ8ObfwzceL4P+Erulg02NDIA4OyWQEbUYjovUn6Y713XiLxx4bsdWGrR3x8SaxaYj0+BbXyNOslB42pnLFex/HsK5cfFXUtSV7fxZp9n4isy7SJFcr5bxMf7jpyo9q4a5lSe6mmjhSBJHZlijztQE52jJJwOnJNRUUUV/9k="}'      http://localhost:8081/classify/v0 | jq
$ python images/echo-server/client_repdict.py ./digit4.png http://localhost:8081/classify/v0

```