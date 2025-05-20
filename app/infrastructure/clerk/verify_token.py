import httpx
from jose import jwt, JWTError

CLERK_ISSUER = "https://modest-chipmunk-16.clerk.accounts.dev"
CLERK_JWKS_URL = f"{CLERK_ISSUER}/.well-known/jwks.json"

async def verify_token(token: str):
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(CLERK_JWKS_URL)
            jwks = resp.json()

            # Decodificar JWT y verificar firma
            kid = jwt.get_unverified_header(token)["kid"]
            key = next(k for k in jwks["keys"] if k["kid"] == kid)

            payload = jwt.decode(
                token,
                key,
                algorithms=["RS256"],
                issuer=CLERK_ISSUER,
                options={"verify_aud": False},
            )
            return payload
    except (JWTError, Exception) as e:
        print(f"Error en verificar token: {e}")
        return None

