# Movie theater simulation with simpy
# Goal: Average Wait <= 10min

# arrive at theater
# get in line to buy a ticket
# buy a ticket
# wait in line to have their ticket checked
# have their ticket checked
# decide to buy grosseries or not
# buy grosseries or go directly to seat

import simpy
import random
import statistics

wait_times = []


class Theater(object):
    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        self.env = env
        self.cashiers = simpy.Resource(env, num_cashiers)
        self.servers = simpy.Resource(env, num_servers)
        self.ushers = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        yield self.env.timeout(random.randint(1, 6))
