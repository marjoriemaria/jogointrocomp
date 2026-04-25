def calcular_dano(atacante, alvo):
    dano = atacante.ataque * (50 / (50 + alvo.defesa))
    return max(1, int(dano))


def aplicar_dano(atacante, alvo):
    dano = max(0, atacante.ataque - alvo.defesa)
    alvo.receber_dano(dano) 
    return dano


def verificar_vitoria(aliados, inimigos):
    aliados_vivos = [a for a in aliados if a.esta_vivo()]
    inimigos_vivos = [i for i in inimigos if i.esta_vivo()]

    if not inimigos_vivos:
        return "VITORIA"
    
    if not aliados_vivos:
        return "DERROTA"
    
    return None
