## Running ollama Third-Party Service

### Choosing a model 
you can get the model_id that ollama will launch from the [Ollama library]
https://olama.com/library

eg. https://olama.com/library/llama3.2

### Getting the Host IP

#### Linux
```sh
sudo apt install net-tools
ifconfig
```

LLM_ENDPOINT_PORT=8008 LLM_MODEL_ID="llama3.2:1b"
host_ip=172.18.250.25 docker-compose up