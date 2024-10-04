# X-Proxy

X-Proxy is an API for simplifying X (formerly Twitter) requests for a single authenticated account. This project provides a set of endpoints that wrap around the X API, making it easier to interact with X's features programmatically. It handles renewing authentication tokens, albeit

## Features

-   Get tweets by ID
-   Search for tweets
-   Post new tweets (with optional media)
-   Manage draft tweets
-   Pull mentions
-   Follow and unfollow users
-   Retrieve home timeline
-   Secure authentication using bearer tokens

## API Endpoints

For a detailed list of available endpoints and their usage, please refer to the [API Documentation](api.md).

## Getting Started

### Prerequisites

-   Python 3.10 or higher
-   Poetry (for dependency management)

### Installation

1. Clone the repository:

    ```
    git clone https://github.com/virtuous-cycles/x-proxy.git
    cd x-proxy
    ```

2. Install dependencies:

    ```
    poetry install --no-root
    ```

3. Set up environment variables:
    - Copy the `.env.example` file to create a new `.env` file:
        ```
        cp .env.example .env
        ```
    - Open the `.env` file and fill in the necessary environment variables as defined in `config.py`. The `.env.example` file provides a template with placeholder values for all required variables.

### Running the Application

To start the application, run:

```
poetry run python main.py
```

## Authentication

All API routes are protected and require an Authorization header with a bearer token. The token is validated against the `API_SECRET_KEY` set in your environment variables.

## Project Structure

-   `api/`: Contains route definitions and API logic
-   `services/`: Houses service classes for interacting with X API and other functionalities
-   `config.py`: Configuration settings
-   `main.py`: Main application entry point

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]

## Acknowledgements

-   X API Documentation
-   Flask
-   Tweepy
