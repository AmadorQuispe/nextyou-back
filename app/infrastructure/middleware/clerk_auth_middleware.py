from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request, Response
from starlette.types import ASGIApp

from app.infrastructure.clerk.verify_token import verify_token
from app.infrastructure.container import Container

container = Container()

class ClerkAuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, protected_paths: list[str]):
        super().__init__(app)
        self.protected_paths = protected_paths

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":
            return await call_next(request)
        # Continuar si no es protected_path
        if not any(request.url.path.startswith(p) for p in self.protected_paths):
            return await call_next(request)

        
        if(request.headers.get("Authorization") is None):
            raise HTTPException(status_code=401, detail="No token provided")
        
        authorization = request.headers.get("Authorization")
        if not authorization.startswith("Bearer "):
            return Response("Unauthorized", status_code=401, headers={"WWW-Authenticate": "Bearer"})
        token = authorization.split(" ")[1]

        if not token:
            return Response("Unauthorized", status_code=401)

        try:
            payload = await verify_token(token)            
            if not payload:
                return Response("Unauthorized", status_code=401)
            ## Verificar que el usuario existe en la base de datos local
            user_local = await container.use_case_user.find_by_external_id(payload["sub"])
            if not user_local:
                return Response("Unauthorized", status_code=401)
            ## Guardar el user_id en la petición
            request.state.user_id = user_local.id
        except (Exception):
            return Response("Unauthorized", status_code=401)

       

        return await call_next(request)

