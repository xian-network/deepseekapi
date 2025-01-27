# DeepSeekAPI - Installation and Deployment Guide

This guide provides instructions for cloning, building, and running the DeepSeekAPI service.

## Features

- Streamed and Non-Streamed Conversations with DeepSeek

## Cloning the Repository

Start by cloning the repository:

```bash
git clone https://github.com/xian-network/deepseekapi.git
```

## Setting Up for Development

For development purposes, you may set up the environment manually:

1. Install Python 3.11.
2. Install the project dependencies:

   ```bash
   cd deepseekapi
   pip3.11 install -e .
   touch .env

   # Add the following environment variables to the .env file
   # (replace the values with your own)
   echo "DEEPSEEK_API_KEY=<api-key>" >> .env
   ```

3. Run the application:

   ```bash
   python3.11 -m uvicorn deepseekapi.app:app --reload --port 3001 --host 0.0.0.0
   ```

The `--reload` flag is used for hot reloading during development.

## Accessing API Documentation

Once the service is running, access the API documentation at:

```
http://localhost:3001/docs
```

This URL provides interactive documentation and testing capabilities for API endpoints.

---

Ensure that all steps are followed according to your deployment needs. For production deployments, additional considerations for security, scalability, and environment-specific configurations should be taken into account.
