# Classification of captured JSON-RPC messages

Capture taken against the remote server deployed on Render, using
capture_session.py, with TLS decrypted via SSLKEYLOGFILE.

| Frame # | JSON-RPC type | Method | Direction | Description |
|---|---|---|---|---|
| 327 | Request | initialize | Client -> Server | Session start request, includes protocolVersion and clientInfo |
| 363 | Response | initialize | Server -> Client | Response with capabilities and serverInfo |
| 366 | Notification (synchronization) | notifications/initialized | Client -> Server | Confirms the client already processed the initialize response, carries no id |
| 368 | HTTP acknowledgment, no JSON-RPC content | (none) | Server -> Client | HTTP 204 No Content, the transport layer still returns a response even though the notification expects none at the JSON-RPC level |
| 370 | Request | tools/list | Client -> Server | Requests the catalog of available tools |
| 375 | Response | tools/list | Server -> Client | Returns the 3 tools with their inputSchema |
| 378 | Request | tools/call | Client -> Server | Call to search_by_symptom with symptom=fiebre |
| 381 | Response | tools/call | Server -> Client | Successful result, isError false |
| 384 | Request | tools/call | Client -> Server | Call to purchase_medication with amoxicilina |
| 389 | Response | tools/call | Server -> Client | Result with isError true, prescription required |

## Classification criteria

Every message with the id field present that expects a response was
classified as Request. Every message containing result or error,
correlated to its Request by the same id value, was classified as
Response. The only message without an id field, notifications/initialized,
was classified as a synchronization message (Notification), since
JSON-RPC 2.0 defines that a message without id neither expects nor
receives a response at the protocol level.

Frame 368 is worth noting separately, it is an HTTP-level response
(204 No Content) to the notification, even though no JSON-RPC response
was expected. This reflects a distinction between the two layers
involved, HTTP as the transport always completes a request/response
cycle, while JSON-RPC as the application protocol defines whether that
response carries meaningful content or not.