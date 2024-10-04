# Quick API Guide

## Overview

This guide covers the API routes implemented using Flask in your current project. These routes include functionalities to get tweets, search for tweets, post tweets, manage draft tweets, pull mentions, follow users, and unfollow users. Authentication is handled using a token.

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

7. **Follow User**

    - **Endpoint:** `/api/follow_user`
    - **Method:** `POST`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Request Body:**
        ```json
        {
            "username": "<twitter_handle>"
        }
        ```
    - **Response:**
        - On Success (Public Account):
            ```json
            {
                "success": true,
                "message": "Successfully followed user @username.",
                "following": true,
                "pending_follow": false
            }
            ```
        - On Success (Private Account):
            ```json
            {
                "success": true,
                "message": "Follow request sent to @username. Waiting for user approval.",
                "following": false,
                "pending_follow": true
            }
            ```
        - On User Not Found:
            ```json
            {
                "success": false,
                "error": "User not found",
                "message": "User with username username not found"
            }
            ```
        - On Other Failures:
            ```json
            {
                "success": false,
                "error": "An error occurred while following the user",
                "message": "Detailed error message"
            }
            ```

8. **Unfollow User**
    - **Endpoint:** `/api/unfollow_user`
    - **Method:** `POST`
    - **Headers:**
        ```http
        Authorization: Bearer <API_SECRET_KEY>
        ```
    - **Request Body:**
        ```json
        {
            "username": "<twitter_handle>"
        }
        ```
    - **Response:**
        - On Success:
            ```json
            {
                "success": true,
                "message": "Successfully unfollowed user @username.",
                "following": false
            }
            ```
        - On User Not Found:
            ```json
            {
                "success": false,
                "error": "User not found",
                "message": "User with username username not found"
            }
            ```
        - On Other Failures:
            ```json
            {
                "success": false,
                "error": "An error occurred while unfollowing the user",
                "message": "Detailed error message"
            }
            ```

## Authentication

All routes are protected and require an Authorization header with a bearer token. The token is validated against the `API_SECRET_KEY` set in your environment variables.
