from datetime import date
from typing import List
from app.models import Aula

def gerar_plano_diario(revisoes_pendentes: List[Aula], aulas_pendentes: List[Aula]) -> dict:
    hoje = date.today()

    # 1. Regra do Descanso: Segunda a Sábado (Domingo = 6 no Python)
    if hoje.weekday() == 6:
        return {
            "status": "folga",
            "mensagem": "Domingo é dia de descanso! Recarregue as energias.",
            "revisoes": [],
            "aulas_novas": []
        }

    # 2. Organização das Aulas Novas por Dificuldade
    faceis = [a for a in aulas_pendentes if a.dificuldade <= 2]
    medias = [a for a in aulas_pendentes if a.dificuldade == 3]
    dificeis = [a for a in aulas_pendentes if a.dificuldade >= 4]

    plano_novas = []

    # 3. A Regra de Ouro: 2 Disciplinas/dia, NUNCA Difícil + Difícil.
    if dificeis:
        # Pega a primeira pedreira (ex: Contabilidade ou Direito Tributário)
        plano_novas.append(dificeis.pop(0)) 
        
        # O par dela tem que ser Média ou Fácil para balancear a carga cognitiva
        if medias:
            plano_novas.append(medias.pop(0))
        elif faceis:
            plano_novas.append(faceis.pop(0))
    else:
        # Se não há matérias difíceis pendentes, junta as médias e fáceis e pega duas
        todas_restantes = medias + faceis
        if todas_restantes:
            plano_novas = todas_restantes[:2] # Pega até 2 aulas

    # 4. Inclusão das Revisões
    # Pegamos as revisões e limitamos a um número seguro (ex: max 5 por dia) 
    # para caber nas 4 horas totais junto com as aulas novas.
    bloco_revisoes = revisoes_pendentes[:5]

    # 5. O Retorno "Estilo Tutory" (A interface só lê e exibe)
    return {
        "status": "estudo",
        "meta_diaria": "4 Horas (Revisões + 2 Disciplinas Novas)",
        "revisoes": bloco_revisoes,
        "aulas_novas": plano_novas
    }