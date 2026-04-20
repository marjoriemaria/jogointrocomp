def calcular_dano(atacante, alvo):
    dano = atacante.ataque - alvo.defesa
    if dano < 0:
        dano = 0
    return dano


def aplicar_dano(atacante, alvo):
    dano = calcular_dano(atacante, alvo)
    alvo.vida -= dano
    return dano


def verificar_vitoria(aliados, inimigos):
    if all(not i.esta_vivo() for i in inimigos):
        return "VITORIA"
    
    if all(not a.esta_vivo() for a in aliados):
        return "DERROTA"
    
    return None