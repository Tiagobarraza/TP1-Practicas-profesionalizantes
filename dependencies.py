from fastapi import HTTPException, Query, Depends

def verify_api_token(token: str = Query(...)):
    if token != "nivel-intermedio-2026":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return token
