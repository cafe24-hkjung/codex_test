import openai
from typing import Dict

from dependency_injector.wiring import Provider, inject

from .decorators import async_retry, performance_monitor
from .types import AsyncResult

DEFAULT_MODEL = "gpt-4"
DEFAULT_TEMPERATURE = 0.2
DEFAULT_MAX_TOKENS = 2000
SYSTEM_PROMPT = "You are an expert programmer."

PREPROCESS_PROMPT_TEMPLATE = """
Create a highly optimized and well-documented implementation with:
- Type hints
- Error handling
- Performance considerations
- Unit tests

Original prompt: {prompt}
"""

class CodeGenerationStrategy:
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError

class GPT4Strategy(CodeGenerationStrategy):
    @async_retry(retries=3)
    async def generate(self, prompt: str) -> str:
        response = await openai.ChatCompletion.acreate(
            model=DEFAULT_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=DEFAULT_TEMPERATURE,
            max_tokens=DEFAULT_MAX_TOKENS,
        )
        return response.choices[0].message.content

class CodeGenerator:
    def __init__(self, strategy: CodeGenerationStrategy = None):
        self.strategy = strategy or GPT4Strategy()
        self._cache: Dict[str, AsyncResult[str]] = {}
        
    @performance_monitor
    async def generate_code(self, prompt: str) -> AsyncResult[str]:
        try:
            if prompt in self._cache:
                return self._cache[prompt]
            
            processed_prompt = await self._preprocess_prompt(prompt)
            code = await self.strategy.generate(processed_prompt)
            result = AsyncResult(value=code)
            
            self._cache[prompt] = result
            return result
            
        except Exception as e:
            return AsyncResult(error=e)

    async def _preprocess_prompt(self, prompt: str) -> str:
        return PREPROCESS_PROMPT_TEMPLATE.format(prompt=prompt)
