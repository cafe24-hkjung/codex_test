import ast
from typing import List, Dict, Set
from .types import SecurityIssue, PerformanceMetrics, CodeAnalysisResult
from .decorators import performance_monitor
from datetime import datetime

class CodeAnalyzer:
    def __init__(self):
        self.security_patterns: Dict[str, SecurityLevel] = {
            "eval": SecurityLevel.HIGH,
            "exec": SecurityLevel.HIGH,
            "__import__": SecurityLevel.MEDIUM,
            "subprocess": SecurityLevel.MEDIUM
        }

    @performance_monitor
    async def analyze(self, code: str) -> CodeAnalysisResult:
        tree = ast.parse(code)
        
        security_issues = await self._analyze_security(tree)
        complexity = await self._calculate_complexity(tree)
        performance = await self._analyze_performance(tree)
        
        return CodeAnalysisResult(
            complexity_score=complexity,
            suggestions=self._generate_suggestions(tree),
            security_issues=security_issues,
            performance=performance,
            code_quality_score=self._calculate_quality_score(tree)
        )

    async def _analyze_security(self, tree: ast.AST) -> List[SecurityIssue]:
        issues = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    func_name = node.func.id
                    if func_name in self.security_patterns:
                        issues.append(
                            SecurityIssue(
                                severity=self.security_patterns[func_name],
                                description=f"Dangerous function '{func_name}' detected",
                                location=f"Line {node.lineno}",
                                timestamp=datetime.now()
                            )
                        )
        return issues

    async def _calculate_complexity(self, tree: ast.AST) -> float:
        complexity = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.For, ast.While)):
                complexity += 1
            elif isinstance(node, ast.FunctionDef):
                complexity += len(list(ast.walk(node)))
        return complexity

    async def _analyze_performance(self, tree: ast.AST) -> PerformanceMetrics:
        nested_loops = self._count_nested_loops(tree)
        time_complexity = self._estimate_time_complexity(nested_loops)
        
        return PerformanceMetrics(
            time_complexity=time_complexity,
            space_complexity=self._estimate_space_complexity(tree),
            optimization_suggestions=self._generate_optimization_suggestions(tree),
            memory_usage=0.0,  # Will be filled by performance monitor
            execution_time=0.0  # Will be filled by performance monitor
        )

    def _count_nested_loops(self, tree: ast.AST, depth: int = 0) -> int:
        max_depth = depth
        for node in ast.iter_child_nodes(tree):
            if isinstance(node, (ast.For, ast.While)):
                current_depth = self._count_nested_loops(node, depth + 1)
                max_depth = max(max_depth, current_depth)
        return max_depth

    def _estimate_time_complexity(self, nested_loops: int) -> ComplexityLevel:
        complexity_map = {
            0: ComplexityLevel.O_1,
            1: ComplexityLevel.O_N,
            2: ComplexityLevel.O_N_2
        }
        return complexity_map.get(nested_loops, ComplexityLevel.O_N_2) 