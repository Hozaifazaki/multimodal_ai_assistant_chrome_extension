import uvicorn
from fastapi import FastAPI, HTTPException, Response
from models.chat_models import ChatInput, ChatResponse
from services.llm_service import AIAssistant



# Create the server
## This initializes the FastAPI app, which will handle incoming HTTP requests.
app = FastAPI()

# Create the chat end-point
## Defines a POST endpoint /ai-assistant where users can send a question and webpage content. 
### FastAPI automatically deserializes the request into a ChatInput object.
#### By marking the function as async, you allow FastAPI to handle the long-running I/O operations (like querying the LLM model) asynchronously. 
##### This means that while the request is waiting for an external response (e.g., from the LLM), the server can continue to process other incoming requests.
@app.post("/ai-assistant")
async def get_response(request: ChatInput):
    try:
        print(request.user_prompt, request.webpage_content)
        ai_assistant = AIAssistant(request.user_prompt, request.webpage_content, None)

        assistant_response = ai_assistant.generate_response()
        return ChatResponse(assistant_response=assistant_response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
