# Project Setup

## Environment Variables

To run this project using Docker Compose or a Dockerfile, you need to set specific environment variables. Use the provided `.env.example` file as a reference.

### Required Environment Variables

1. `POLYGON_URL`: URL for the Polygon API.
2. `POLYGON_TOKEN`: Authentication token for accessing the Polygon API.
3. `DATABASE_URL`: URL for the database connection.
4. `DATABASE_ECHO`: Flag indicating whether to echo database queries.
5. `CACHE_URL`: URL for the cache server.

### Setting Environment Variables

Create a `.env` file in the root directory of your project. Assign the required values to each variable, replacing placeholders in the `.env.example` file with actual values specific to your setup.

Refer to the [official Docker documentation](https://docs.docker.com/compose/environment-variables/) for more information on setting environment variables in Docker Compose or Dockerfile.

## Stock API Routes

This project provides the following API routes for interacting with stock data:

### Routes

1. **GET `/stock/{stock_symbol}`**: Retrieve detailed information about a specific stock and the amount the user owns, identified by its symbol.

2. **POST `/stock/{stock_symbol}`**: Modify the amount of stock the user owns. The `amount` field in the request body acts as a sum operator and can be either negative or positive.

### Usage

To access these routes, make HTTP requests to the corresponding endpoint, replacing `{stock_symbol}` with the desired stock symbol.

For detailed information on how to use these routes and the expected response formats, refer to the API documentation available at the `/docs` endpoint.
