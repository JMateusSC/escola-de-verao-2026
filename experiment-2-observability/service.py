"""
Experimento 2 - Observabilidade
Serviço observável com logging estruturado e coleta de Golden Signals
"""

import logging
import json
import time
import random
from dataclasses import dataclass, asdict
from typing import Dict, Any
from datetime import datetime


@dataclass
class Metrics:
    """Armazena métricas do serviço (Golden Signals)"""
    latency_ms: float
    request_count: int
    error_count: int
    cpu_percent: float


class JSONFormatter(logging.Formatter):
    """Formatter customizado para logs estruturados em JSON"""
    
    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "context": getattr(record, "context", {}),
        }
        
        # Adicionar request_id se disponível
        if hasattr(record, "request_id"):
            log_entry["request_id"] = record.request_id
        
        return json.dumps(log_entry)


class ObservableService:
    """Serviço observável que emite logs estruturados e coleta métricas"""
    
    def __init__(self):
        self.setup_logging()
        self.metrics = Metrics(
            latency_ms=0.0,
            request_count=0,
            error_count=0,
            cpu_percent=0.0
        )
        self.total_latency = 0.0
    
    def setup_logging(self):
        """Configura logging estruturado em JSON"""
        self.logger = logging.getLogger("ObservableService")
        self.logger.setLevel(logging.DEBUG)
        
        # Remove handlers existentes para evitar duplicação
        self.logger.handlers.clear()
        
        # Handler para stdout com formato JSON
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(console_handler)
        
        # Handler para arquivo com formato JSON
        import os
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "service.log")
        
        file_handler = logging.FileHandler(log_file, mode='a', encoding='utf-8')
        file_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(file_handler)
        
        # Evitar propagação para o root logger
        self.logger.propagate = False
    
    def process_request(self, request_id: str, data: dict) -> dict:
        """
        Processa uma requisição, emitindo logs e coletando métricas
        
        Args:
            request_id: Identificador único da requisição
            data: Dados da requisição
            
        Returns:
            Resultado do processamento
        """
        start_time = time.time()
        
        # Log de início
        self.logger.info(
            f"Processing request {request_id}",
            extra={
                "request_id": request_id,
                "context": {"data_size": len(str(data))}
            }
        )
        
        try:
            # Simular processamento
            processing_time = random.uniform(0.01, 0.1)
            time.sleep(processing_time)
            
            # Simular falhas ocasionais (10% de chance)
            if random.random() < 0.1:
                raise ValueError("Simulated processing error")
            
            # Simular uso de CPU
            self.metrics.cpu_percent = random.uniform(20.0, 80.0)
            
            # Log de sucesso
            self.logger.info(
                f"Request {request_id} completed successfully",
                extra={
                    "request_id": request_id,
                    "context": {"status": "success"}
                }
            )
            
            result = {"status": "success", "request_id": request_id}
            
        except Exception as e:
            # Incrementar contador de erros
            self.metrics.error_count += 1
            
            # Log de erro
            self.logger.error(
                f"Request {request_id} failed: {str(e)}",
                extra={
                    "request_id": request_id,
                    "context": {
                        "error_type": type(e).__name__,
                        "error_message": str(e)
                    }
                }
            )
            
            result = {
                "status": "error",
                "request_id": request_id,
                "error": str(e)
            }
        
        finally:
            # Calcular latência
            latency = (time.time() - start_time) * 1000  # em milissegundos
            self.total_latency += latency
            
            # Atualizar métricas
            self.metrics.request_count += 1
            self.metrics.latency_ms = self.total_latency / self.metrics.request_count
            
            # Log de métricas
            self.logger.debug(
                f"Request {request_id} metrics",
                extra={
                    "request_id": request_id,
                    "context": {
                        "latency_ms": latency,
                        "total_requests": self.metrics.request_count
                    }
                }
            )
        
        return result
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Retorna as métricas do serviço (Golden Signals)
        
        Returns:
            Dicionário com latency, traffic, errors, saturation
        """
        return {
            "latency": self.metrics.latency_ms,
            "traffic": self.metrics.request_count,
            "errors": self.metrics.error_count,
            "saturation": self.metrics.cpu_percent
        }


if __name__ == "__main__":
    # Exemplo de uso
    service = ObservableService()
    
    print("=== Executando serviço observável ===\n")
    
    # Processar algumas requisições
    for i in range(10):
        request_id = f"req-{i:03d}"
        data = {"user_id": i, "action": "test"}
        
        result = service.process_request(request_id, data)
        print(f"Result: {result}")
    
    # Exibir métricas finais
    print("\n=== Golden Signals ===")
    metrics = service.get_metrics()
    print(json.dumps(metrics, indent=2))
