from typing import Optional
import json
from app.schemas.token import TokenCreate, TokenUpdate, TokenResponse
from app.mixins.redis import RedisMixin


class TokensRepository(RedisMixin):

    async def get(self, token_hash: str) -> TokenResponse | None:
        token_data = await self._redis.get(token_hash)
        if not token_data:
            return None

        data = json.loads(token_data)
        return TokenResponse(**data)

    async def create(self, token: TokenCreate) -> bool:
        is_created = await self._redis.set(
            name=token.refresh_token_hash,
            value=token.json(),
            ex=token.refresh_token_expires_in
        )
        return is_created

    async def update(self, token: TokenUpdate) -> bool:
        is_updated = await self._redis.set(
            name=token.refresh_token_hash,
            value=token.json(),
            ex=token.refresh_token_expires_in
        )
        return is_updated