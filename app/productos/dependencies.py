from fastapi import HTTPException, Query

def verify_api_token(token: str = Query(None)):
    if token != "nivel-intermedio-2026":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token