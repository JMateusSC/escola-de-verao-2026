"""
Experimento 2 - Observabilidade
Analisador de logs estruturados
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime


class LogAnalyzer:
    """Ferramenta para análise de logs estruturados"""
    
    def load_logs_from_file(self, log_file: str = None) -> List[dict]:
        """
        Carrega logs de um arquivo JSON
        
        Args:
            log_file: Caminho para o arquivo de log. Se None, usa logs/service.log
            
        Returns:
            Lista de entradas de log (dicionários)
            
        Raises:
            FileNotFoundError: Se o arquivo não existir
        """
        if log_file is None:
            log_dir = os.path.join(os.path.dirname(__file__), "logs")
            log_file = os.path.join(log_dir, "service.log")
        
        if not os.path.exists(log_file):
            raise FileNotFoundError(f"Log file not found: {log_file}")
        
        logs = []
        with open(log_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        logs.append(json.loads(line))
                    except json.JSONDecodeError:
                        # Pular linhas malformadas
                        continue
        
        return logs
    
    def filter_by_level(self, logs: List[dict], level: str) -> List[dict]:
        """
        Filtra logs por nível de severidade
        
        Args:
            logs: Lista de entradas de log (dicionários)
            level: Nível desejado (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            
        Returns:
            Lista de logs que correspondem ao nível especificado
            
        Raises:
            ValueError: Se o nível fornecido não for válido
        """
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        
        if level not in valid_levels:
            raise ValueError(
                f"Invalid log level: {level}. "
                f"Must be one of {', '.join(valid_levels)}"
            )
        
        return [log for log in logs if log.get("level") == level]
    
    def filter_by_timerange(
        self, 
        logs: List[dict], 
        start: str, 
        end: str
    ) -> List[dict]:
        """
        Filtra logs por intervalo de tempo
        
        Args:
            logs: Lista de entradas de log
            start: Timestamp de início (formato ISO 8601)
            end: Timestamp de fim (formato ISO 8601)
            
        Returns:
            Lista de logs dentro do intervalo especificado
            
        Raises:
            ValueError: Se os timestamps não estiverem em formato válido
        """
        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
        except ValueError as e:
            raise ValueError(f"Invalid datetime format: {e}")
        
        filtered = []
        for log in logs:
            try:
                log_dt = datetime.fromisoformat(log["timestamp"])
                if start_dt <= log_dt <= end_dt:
                    filtered.append(log)
            except (KeyError, ValueError):
                # Pular entradas de log malformadas
                continue
        
        return filtered
    
    def find_errors(self, logs: List[dict]) -> List[dict]:
        """
        Encontra todos os logs de erro
        
        Args:
            logs: Lista de entradas de log
            
        Returns:
            Lista de logs com nível ERROR ou CRITICAL
        """
        return [
            log for log in logs 
            if log.get("level") in ["ERROR", "CRITICAL"]
        ]
    
    def calculate_error_rate(self, logs: List[dict]) -> float:
        """
        Calcula a taxa de erro dos logs
        
        Args:
            logs: Lista de entradas de log
            
        Returns:
            Taxa de erro como porcentagem (0.0 a 100.0)
            Retorna 0.0 se não houver logs
        """
        if not logs:
            return 0.0
        
        error_count = len(self.find_errors(logs))
        total_count = len(logs)
        
        return (error_count / total_count) * 100.0


if __name__ == "__main__":
    analyzer = LogAnalyzer()
    
    print("=== Análise de Logs ===\n")
    
    try:
        # Carregar logs do arquivo
        logs = analyzer.load_logs_from_file()
        print(f"Total de logs carregados: {len(logs)}\n")
        
        if not logs:
            print("Nenhum log encontrado. Execute service.py primeiro para gerar logs.")
        else:
            # Filtrar por nível
            errors = analyzer.filter_by_level(logs, "ERROR")
            print(f"Logs de ERROR: {len(errors)}")
            for log in errors:
                print(f"  - {log['message']}")
            
            # Encontrar todos os erros
            all_errors = analyzer.find_errors(logs)
            print(f"\nTotal de erros: {len(all_errors)}")
            
            # Calcular taxa de erro
            error_rate = analyzer.calculate_error_rate(logs)
            print(f"Taxa de erro: {error_rate:.2f}%")
            
            # Mostrar últimos 5 logs
            print(f"\nÚltimos 5 logs:")
            for log in logs[-5:]:
                print(f"  [{log['level']}] {log['message']}")
    
    except FileNotFoundError as e:
        print(f"Erro: {e}")
        print("Execute service.py primeiro para gerar logs.")
