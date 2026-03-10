from datetime import date, timedelta
from app.models import Aula

def calcular_proxima_revisao(aula: Aula) -> Aula:
    """
    Motor 3R v1.0: Regras de repetição espaçada.
    """
    hoje = date.today()
    
    # Lógica simples inicial: revisão no dia seguinte
    aula.proxima_revisao = hoje + timedelta(days=1)
    
    # Aqui no futuro você pode adicionar a lógica de dificuldade:
    # if aula.dificuldade == 3: # Matéria muito difícil
    #    aula.prioridade = 10
    # else:
    
    aula.prioridade = 5
    
    return aula