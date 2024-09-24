# Quick API Guide

## Overview
This guide covers the API routes implemented using Flask in your current project. These routes include functionalities to get tweets, search for tweets, post tweets, manage draft tweets, pull mentions, and retrieve the home timeline.

## Project Structure
The project now includes a new file:
- `/api/get_home_timeline_route.py`: Handles the endpoint for retrieving the home timeline.

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
          "requested_tweet": {
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
          "root_tweet": { /* Similar structure to requested_tweet */ },
          "ancestor_chain": [ /* Array of tweets leading to the requested tweet */ ],
          "sibling_tweets": [ /* Array of tweets with the same parent as the requested tweet */ ],
          "children_tweets": [ /* Array of direct replies to the requested tweet */ ]
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

7. **Get Home Timeline**
    - **Endpoint:** `/api/get_home_timeline`
    - **Method:** `GET`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Query Parameters:**
      - `max_results` (integer, optional): The number of tweets to retrieve (default is 100, max 100)
      - `pagination_token` (string, optional): A token to retrieve the next page of results
    - **Response:**
      - On Success:
        ```json
        {
          "data": [
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
          ],
          "meta": {
            "result_count": <number_of_tweets_returned>,
            "next_token": "<pagination_token_for_next_page>"
          }
        }
        ```
      - On Failure:
        ```json
        {
          "error": "An error occurred while retrieving the home timeline"
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

## Changes to Existing Endpoints
- The `get_tweet` endpoint now returns more comprehensive information, including the requested tweet, root tweet of the conversation, ancestor chain, sibling tweets, and children tweets.
- The `get_home_timeline` endpoint has been added to retrieve the user's home timeline.

## Additional Information
- OAuth setup and validation are handled in `services/oauth_setup.py`.
- Services communicate with the external API (Twitter) via a custom `XService` class.
- The `CombinedServices` class in `services/combined_services.py` handles operations that involve both Airtable and Twitter services.
- The `process_x_response` function in `services/process_x_response.py` processes X API responses to include expanded data (author information, referenced tweets, media attachments) in the tweet objects.
- Rate limiting is handled by the `handle_rate_limit` decorator in `services/rate_limit_handler.py`.

For more details on the implementation, see the individual route files and the `main.py` file.