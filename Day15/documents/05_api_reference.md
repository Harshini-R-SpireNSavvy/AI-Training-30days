# Internal Tools API Reference

## Authentication
All requests require a Bearer token from the SSO token endpoint. Tokens expire after 3600 seconds. Refresh using the `/oauth/token` endpoint with the refresh grant.

## Rate limits
The public API tier allows 100 requests per minute per API key. Burst allowance is 20 additional requests over a 10-second window. Exceeding limits returns HTTP 429 with a `Retry-After` header in seconds.

## Pagination
List endpoints return at most 50 items per page. Use the `cursor` query parameter from the `next_cursor` field in the response body for subsequent pages.
