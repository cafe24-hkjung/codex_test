import asyncio
import logging
from pathlib import Path
from dotenv import load_dotenv
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from .code_generator import CodeGenerator, GPT4Strategy
from .code_analyzer import CodeAnalyzer

class Container(DeclarativeContainer):
    code_generator = Singleton(CodeGenerator, strategy=Singleton(GPT4Strategy))
    code_analyzer = Singleton(CodeAnalyzer)

async def main():
    try:
        # 환경 변수 로드
        load_dotenv()
        
        # 로깅 설정
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # DI 컨테이너 초기화
        container = Container()
        
        # 서비스 인스턴스 가져오기
        generator = container.code_generator()
        analyzer = container.code_analyzer()
        
        # 예제 프롬프트
        prompt = """
        Create a highly optimized implementation of a B-Tree data structure
        with complete error handling and thread-safety
        """
        
        # 코드 생성
        logging.info("Generating code...")
        result = await generator.generate_code(prompt)
        
        if result.error:
            logging.error(f"Code generation failed: {result.error}")
            return
        
        # 생성된 코드 분석
        logging.info("Analyzing generated code...")
        analysis = await analyzer.analyze(result.value)
        
        # 결과 출력
        print("\nGenerated Code:")
        print(result.value)
        print("\nCode Analysis:")
        print(f"Complexity Score: {analysis.complexity_score}")
        print(f"Code Quality Score: {analysis.code_quality_score}")
        print("\nSecurity Issues:")
        for issue in analysis.security_issues:
            print(f"- {issue.severity}: {issue.description} at {issue.location}")
        print("\nPerformance Metrics:")
        print(f"Time Complexity: {analysis.performance.time_complexity}")
        print(f"Space Complexity: {analysis.performance.space_complexity}")
        print("\nOptimization Suggestions:")
        for suggestion in analysis.performance.optimization_suggestions:
            print(f"- {suggestion}")
            
    except Exception as e:
        logging.error(f"Application error: {e}", exc_info=True)

if __name__ == "__main__":
    asyncio.run(main()) 