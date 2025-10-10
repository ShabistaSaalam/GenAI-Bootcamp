## Running ollama Third-Party Service

### Choosing a model 
you can get the model_id that ollama will launch from the [Ollama library]
(https://olama.com/library)

### Getting the Host IP

Get your IP address
#### Linux
```sh
sudo apt install net-tools
ifconfig
```

Or you can try this way `$(hostname -I | awk '{print $1}')`
HOST_IP==$(hostname -I | awk '{print $1}')
NO_PROXY=localhost
LLM_ENDPOINT_PORT=8008 LLM_MODEL_ID="llama3.2:1B"
docker-compose up

### Ollama API

Once the Ollama server is running we can make api calls to the Ollama API
`https://github.com/ollama/ollama/blob/main/docs/api.md`

## Download (pull) a model

`
curl http://localhost:11434/api/pull -d'{
  "model":"llama3.2"
}'
`

## Generate a request
`
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.2:1B",
  "prompt": "Why is the sky blue?"
}'
`

# Technical Uncertainty
```
Does bridge mode means we can only access ollama API with another model in the docker compose?
A: No, the host machine will be able to access it

Which port is being mapped 8008->141414
A: In this case 8080 is the port that host machine will access. the other port is the guest port (the port of the service inside the container)

If we pass the LLM_MODEL_ID to the ollama server will it download the model wehn on start?
A: It does not appear so . The Ollama CLI might be running multiple APIs so you need to call the pull api before trying to generate text

Will the model be downloaded in the container?
Does that mean the mol model will be deleted when the container stops running?

The model will download into the container, and vanish when the container stop running.You need to
mount a local drive and there's probably more work to be done.
```