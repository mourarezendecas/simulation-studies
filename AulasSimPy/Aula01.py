import random
import simpy

TEMPO_MEDIO_CHEGADAS = 1.0
TEMPO_MEDIO_ATENDIMENTO = 1


def geraChegadas(env):
    contaChegada = 0
    while True:
        yield env.timeout(random.expovariate(1 / TEMPO_MEDIO_CHEGADAS))
        contaChegada += 1
        print(f"{env.now:.1f} Chegada do cliente {contaChegada}")
        env.process(atendimentoServidor(env, f"cliente {contaChegada}", servidorRes))


def atendimentoServidor(env, nome, servidorRes):
    with servidorRes.request() as request:
        yield request
        print(f"{env.now:.1f} Servidor inicia atendimento do {nome}")

        yield env.timeout(random.expovariate(1.0 / TEMPO_MEDIO_ATENDIMENTO))
        print(f"{env.now:.1f} Servidor terminar atendimento {nome}. Clientes na fila {len(servidorRes.queue)}")


random.seed(25)
env = simpy.Environment()
servidorRes = simpy.Resource(env, capacity=1)
env.process(geraChegadas(env))
env.run(until=15)
