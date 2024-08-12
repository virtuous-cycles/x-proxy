# Quick API Guide

## Overview
This guide covers the basic API routes implemented using Flask in your current project. These routes include functionalities to get a tweet, search for tweets, and post a tweet. Authentication is handled using a token.

## Endpoints

1. **Get Tweet**
    - **Endpoint:** `/api/get_tweet`
    - **Method:** `GET`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Query Parameters:**
      - `tweet_id` (string): The ID of the tweet to retrieve.
    - **Response:**
      - On Success:
        ```json
        {
          "tweet": {
            "id": "<tweet_id>",
            "text": "<tweet_text>",
            ...
          }
        }
        ```
      - On Failure:
        ```json
        {
          "error": "Missing tweet_id"
        }
        ```
      - See [`get_tweet_route.py`](rag://rag_source_6)

2. **Search Tweets**
    - **Endpoint:** `/api/search_tweets`
    - **Method:** `GET`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Query Parameters:**
      - `query` (string): The search query.
    - **Response:**
      - On Success:
        ```json
        {
          "tweets": [
            {
              "id": "<tweet_id>",
              "text": "<tweet_text>",
              ...
            },
            ...
          ]
        }
        ```
      - On Failure:
        ```json
        {
          "error": "Missing query"
        }
        ```
      - See [`search_tweets_route.py`](rag://rag_source_1)

3. **Post Tweet**
    - **Endpoint:** `/api/post_tweet`
    - **Method:** `POST`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Request Body:**
      ```json
      {
        "text": "<tweet_text>",
        "in_reply_to_tweet_id": "<optional: tweet_id>",
        "media_url": "<optional: media_url>"
      }
      ```
    - **Response:**
      - On Success:
        ```json
        {
          "tweet_id": "<tweet_id>"
        }
        ```
      - On Failure:
        ```json
        {
          "error": "Missing text"
        }
        ```
      - See [`post_tweet_route.py`](rag://rag_source_2)

## Authentication
All routes are protected and require an Authorization header with a bearer token. The token is validated against the `API_SECRET_KEY` set in your environment variables.

## Application Setup
To run the application, use the following steps:
1. Ensure all dependencies are installed from `pyproject.toml`.
2. Set the required environment variables for OAuth and API configurations as defined in [`config.py`](rag://rag_source_8).
3. Run the application:
    ```sh
    python main.py
    ```

### Flask Blueprint
All API routes are registered under a blueprint:
- [`api_bp`](rag://rag_source_1) in `api/__init__.py` and then registered in the app in `main.py`.

## Additional Information
- OAuth setup and validation are handled in `services/oauth_setup.py`.
- Services communicate with the external API (Twitter) via a custom `XService` class.

For more details on the implementation, see the individual route files and the `main.py` file.