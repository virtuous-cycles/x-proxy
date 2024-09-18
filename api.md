# Quick API Guide

## Overview
This guide covers the API routes implemented using Flask in your current project. These routes include functionalities to get tweets, search for tweets, post tweets, manage draft tweets, and pull mentions. Authentication is handled using a token.

## Project Structure
The project now includes a new file:
- `/services/process_x_response.py`: Contains utility functions for processing X API responses.

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
            "author": {
              "id": "<author_id>",
              "name": "<author_name>",
              "username": "<author_username>"
            },
            "referenced_tweets": [
              {
                "id": "<referenced_tweet_id>",
                "text": "<referenced_tweet_text>"
              }
            ],
            "media": [
              {
                "media_key": "<media_key>",
                "type": "<media_type>",
                "url": "<media_url>"
              }
            ]
          }
        }
        ```
      - On Failure:
        ```json
        {
          "error": "Missing tweet_id"
        }
        ```

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
              "author": {
                "id": "<author_id>",
                "name": "<author_name>",
                "username": "<author_username>"
              },
              "referenced_tweets": [
                {
                  "id": "<referenced_tweet_id>",
                  "text": "<referenced_tweet_text>"
                }
              ],
              "media": [
                {
                  "media_key": "<media_key>",
                  "type": "<media_type>",
                  "url": "<media_url>"
                }
              ]
            }
          ]
        }
        ```
      - On Failure:
        ```json
        {
          "error": "Missing query"
        }
        ```

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

4. **Get Drafts**
    - **Endpoint:** `/api/get_drafts`
    - **Method:** `GET`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Response:**
      - On Success:
        ```json
        {
          "drafts": [
            {
              "id": "<draft_id>",
              "fields": {
                "content": "<draft_content>",
                ...
              }
            },
            ...
          ]
        }
        ```

5. **Post Draft Tweet**
    - **Endpoint:** `/api/post_draft_tweet`
    - **Method:** `POST`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Request Body:**
      ```json
      {
        "draft_tweet_record_id": "<draft_tweet_record_id>"
      }
      ```
    - **Response:**
      - On Success:
        ```json
        {
          "success": true,
          "tweet_id": "<tweet_id>",
          "tweet_url": "<tweet_url>"
        }
        ```
      - On Failure:
        ```json
        {
          "error": "Draft tweet not found"
        }
        ```

6. **Pull Mentions**
    - **Endpoint:** `/api/pull_mentions`
    - **Method:** `GET`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Response:**
      - On Success:
        ```json
        {
          "mentions": [
            {
              "id": "<tweet_id>",
              "text": "<tweet_text>",
              "author": {
                "id": "<author_id>",
                "name": "<author_name>",
                "username": "<author_username>"
              },
              "referenced_tweets": [
                {
                  "id": "<referenced_tweet_id>",
                  "text": "<referenced_tweet_text>"
                }
              ],
              "media": [
                {
                  "media_key": "<media_key>",
                  "type": "<media_type>",
                  "url": "<media_url>"
                }
              ]
            },
            ...
          ]
        }
        ```

## Authentication
All routes are protected and require an Authorization header with a bearer token. The token is validated against the `API_SECRET_KEY` set in your environment variables.

## Application Setup
To run the application, use the following steps:
1. Ensure all dependencies are installed from `pyproject.toml`.
2. Set the required environment variables for OAuth and API configurations as defined in `config.py`.
3. Run the application:
    ```sh
    python main.py
    ```

### Flask Blueprint
All API routes are registered under a blueprint `api_bp` in `api/__init__.py` and then registered in the app in `main.py`.

## Additional Information
- OAuth setup and validation are handled in `services/oauth_setup.py`.
- Services communicate with the external API (Twitter) via a custom `XService` class.
- The `CombinedServices` class in `services/combined_services.py` handles operations that involve both Airtable and Twitter services.
- The `process_x_response` function in `services/process_x_response.py` processes X API responses to include expanded data (author information, referenced tweets, media attachments) in the tweet objects.

For more details on the implementation, see the individual route files and the `main.py` file.