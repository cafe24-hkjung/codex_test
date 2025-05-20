import asyncio
import openai
from typing import Optional, Dict, Any
from .types import AsyncResult, CodeAnalysisResult
from .decorators import async_retry, performance_monitor
from dependency_injector.wiring import inject, Provider

class CodeGenerationStrategy:
    async def generate(self, prompt: str) -> str:
        raise NotImplementedError

class GPT4Strategy(CodeGenerationStrategy):
    @async_retry(retries=3)
    async def generate(self, prompt: str) -> str:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert programmer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=2000
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
        return f"""
        Create a highly optimized and well-documented implementation with:
        - Type hints
        - Error handling
        - Performance considerations
        - Unit tests
        
        Original prompt: {prompt}
        """ 