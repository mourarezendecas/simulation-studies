import random
import simpy
import numpy as np

NUM_EMPLOYEES = 2
AVG_SUPPORT_TIME = 5
COSTUMER_INTERVAL = 2
SIM_TIME = 120

customers_handles = 0


class CallCenter:
    def __init__(self, env, num_employees, support_time):
        self.env = env
        self.num_employees = simpy.Resource(env, num_employees)
        self.support_time = support_time

    def support(self, customer):
        random_time = max(1, np.random.normal(self.support_time, 4))
        yield self.env.timeout(random_time)
        print(f"Support finished for {customer} at {self.env.now:.2f}")


def customer(env, name, call_center):
    global customers_handles
    print(f"New customer {name} enters waiting queue at {env.now:.2f}!")
    with call_center.staff.request() as request:
        yield request
        print(f"Customer {name} enters call at {env.now:.2f}!")
        yield env.process(call_center.support(name))
        print(f"Customer {name} leaves call at {env.now:.2f}!")
        customers_handles += 1


def setup(env, num_employees, support_time, customer_interval):
    call_center = CallCenter(env, num_employees, support_time)

    for i in range(1, 6):
        env.process(customer(env, i, call_center))

    while True:
        yield env.timeout(random.randint(customer_interval - 1, customer_interval + 1))
        i += 1
        env.process(customer(env, i, call_center))


print("Starting simulation.")
env = simpy.Environment()
env.process(setup(env, NUM_EMPLOYEES, AVG_SUPPORT_TIME, COSTUMER_INTERVAL))
env.run(until=SIM_TIME)

print(f"Customers handles: {customers_handles}")
print("Done.")
