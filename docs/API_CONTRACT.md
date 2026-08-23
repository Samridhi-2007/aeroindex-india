# API Contract (Initial Scaffold)

## Base URL

- Local: `http://127.0.0.1:8000`

## Endpoints

### Health Check

- **Method:** `GET`
- **Path:** `/health`
- **Description:** Service liveness probe.

#### Response 200

```json
{
  "status": "ok",
  "service": "aeroindex-backend"
}
```

## Error Shape (Planned)

Future endpoints should return consistent error payloads:

```json
{
  "error": {
    "code": "STRING_CODE",
    "message": "Human readable message",
    "details": {}
  }
}
```

## Versioning Strategy (Planned)

- Prefix API routes under `/api/v1` as functional endpoints are introduced.
