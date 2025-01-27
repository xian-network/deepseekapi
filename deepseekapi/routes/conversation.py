import fastapi
import aiohttp
import logging
import json
from urllib.parse import unquote
import os
from fastapi.responses import StreamingResponse

logger = logging.getLogger(__name__)

async def request_deepseek_api_normal(conversation):
    """
    Handles non-streaming requests to the DeepSeek API.
    """
    request_dict = {
        "messages": conversation["messages"],  # Standard JSON structure
        "model": "deepseek-chat",
        "stream": False  # Disable streaming
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/chat/completions",
                json=request_dict,
                headers={
                    "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                    "Content-Type": "application/json"
                }
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.text()
                    logger.error(f"DeepSeek API returned status {response.status}: {error_message}")
                    return {"message": "Failed to fetch response from DeepSeek API", "success": False}
    except Exception as err:
        logger.error(f"Error while calling DeepSeek API: {err}")
        return {"message": "Something went wrong", "success": False}


async def request_deepseek_api_stream(conversation):
    """
    Handles streaming requests to the DeepSeek API.
    """
    request_dict = {
        "messages": conversation["messages"],  # Standard JSON structure
        "model": "deepseek-chat",
        "stream": True  # Enable streaming
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://api.deepseek.com/chat/completions",
                json=request_dict,
                headers={
                    "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                    "Content-Type": "application/json"
                }
            ) as response:
                # Stream the response content
                async for chunk in response.content.iter_chunked(512):
                    yield chunk
    except Exception as err:
        logger.error(f"Error while calling DeepSeek API: {err}")
        yield json.dumps({"message": "Something went wrong", "success": False}).encode("utf-8")


def add_route(app):
    @app.post('/conversation')
    async def conversation(
        new_message: str,
        fastapi_request: fastapi.Request,
        previous_conversation: str = '{"messages": []}',  # Default to an empty structure
        stream: bool = False  # Flag to toggle between streaming and non-streaming
    ):
        try:
            # Parse the previous conversation as JSON
            try:
                previous_conversation = json.loads(unquote(previous_conversation))
                if not isinstance(previous_conversation, dict) or "messages" not in previous_conversation:
                    raise ValueError("Previous conversation must be a JSON object with a 'messages' key")
            except Exception as err:
                logger.error(err)
                return {"message": "Previous conversation is not a valid JSON structure", "success": False}

            # Combine the previous conversation with the new message
            messages = previous_conversation["messages"] + [{"role": "user", "content": new_message}]
            conversation_data = {"messages": messages}

            if stream:
                # Call the streaming function
                stream_generator = request_deepseek_api_stream(conversation_data)
                return StreamingResponse(stream_generator, media_type="application/json")
            else:
                # Call the non-streaming function
                response = await request_deepseek_api_normal(conversation_data)
                return response  # Return the full response as JSON
        except Exception as err:
            logger.error(err)
            return {"message": "Something went wrong", "success": False}
