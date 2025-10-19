from comps import MicroService, ServiceOrchestrator
from comps.cores.mega.constants import ServiceType, ServiceRoleType
from comps.cores.proto.api_protocol import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatCompletionResponseChoice,
    ChatMessage,
    UsageInfo,
)
from fastapi import HTTPException
import os

EMBEDDING_SERVICE_HOST_IP = os.getenv("EMBEDDING_SERVICE_HOST_IP", "0.0.0.0")
EMBEDDING_SERVICE_PORT = int(os.getenv("EMBEDDING_SERVICE_PORT", 6000))
LLM_SERVICE_HOST_IP = os.getenv("LLM_SERVICE_HOST_IP", "0.0.0.0")
LLM_SERVICE_PORT = int(os.getenv("LLM_SERVICE_PORT", 8008))


class ExampleService:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.endpoint = "/v1/example-service"
        self.megaservice = ServiceOrchestrator()

    def add_remote_service(self):
        llm = MicroService(
            name="llm",
            host=LLM_SERVICE_HOST_IP,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )
        self.megaservice.add(llm)

    def start(self):
        self.service = MicroService(
            name=self.__class__.__name__,
            service_role=ServiceRoleType.MEGASERVICE,
            host=self.host,
            port=self.port,
            endpoint=self.endpoint,
            input_datatype=ChatCompletionRequest,
            output_datatype=ChatCompletionResponse,
        )

        self.service.add_route(self.endpoint, self.handle_request, methods=["POST"])
        self.service.start()

    async def handle_request(self, request: ChatCompletionRequest) -> ChatCompletionResponse:
        try:
            # Convert messages to dicts (handle dicts or Pydantic models safely)
            messages = [
                msg.dict() if hasattr(msg, "dict") else msg for msg in request.messages
            ]

            ollama_request = {
                "model": request.model or "llama3.2:1b",
                "messages": messages,
                "stream": False,
            }

            # Send the request via the orchestrator
            result = await self.megaservice.schedule(ollama_request)
            print("Received request:", request)
            print("Orchestrator result:", result)

            content = "No response content available"

            # Handle tuple (dict_response, dag) or just dict response
            if isinstance(result, tuple) and len(result) == 2:
                response_dict = result[0]  # Extract the dict from tuple
            else:
                response_dict = result

            response_data = None
            if isinstance(response_dict, list) and len(response_dict) > 0:
                response_data = response_dict[0].get("llm/MicroService")
            elif isinstance(response_dict, dict):
                response_data = response_dict.get("llm/MicroService")

            if response_data:
                if hasattr(response_data, "json") and callable(response_data.json):
                    # Await json() coroutine if exists
                    json_body = await response_data.json()
                    content = (
                        json_body.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", content)
                    )
                elif hasattr(response_data, "body_iterator"):
                    # If streaming response, read all chunks
                    response_body = b""
                    async for chunk in response_data.body_iterator:
                        response_body += chunk
                    content = response_body.decode("utf-8")
                elif isinstance(response_data, dict):
                    # If already a dict response
                    content = (
                        response_data.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", content)
                    )
                else:
                    content = str(response_data)

            response = ChatCompletionResponse(
                model=request.model or "llama3.2:1b",
                choices=[
                    ChatCompletionResponseChoice(
                        index=0,
                        message=ChatMessage(role="assistant", content=content),
                        finish_reason="stop",
                    )
                ],
                usage=UsageInfo(prompt_tokens=0, completion_tokens=0, total_tokens=0),
            )

            return response

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


example = ExampleService()
example.add_remote_service()
example.start()
