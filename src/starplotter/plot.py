import matplotlib.pyplot as plt
from src.starplotter import main

# from random import random
#
# def do_something():
#     global res
#     for p in range(10000000):
#         res = res + p
#
#
# fig, ax = plt.subplots()
# x = []
# y = []
# for i in range(50):
#     x.append(i)
#     y.append(50 * random())
#     ax.cla()  # clear plot
#     ax.plot(x, y, 'r', lw=1)  # draw line chart
#     # ax.bar(y, height=y, width=0.3) # draw bar chart
#     # do_something()
#     plt.pause(0.1)
fig, (ship, booster) = plt.subplots(2, 1)
t = []
speed_booster = []
speed_ship = []
altitude_booster = []
altitude_ship = []


def plot_data(data, timestamp):
    print("Plotting data")
    print(data)
    print(timestamp)
    print("Main loop")

    speed_booster.append(data["speed_booster"])
    speed_ship.append(data["speed_ship"])
    altitude_booster.append(data["altitude_booster"])
    altitude_ship.append(data["altitude_ship"])
    str_time = data["time"][1:]
    print(str_time)
    int_time = int(str_time.split(":")[0]) * 3600 + int(str_time.split(":")[1]) * 60 + int(str_time.split(":")[2])
    if data["time"][0] == "-":
        int_time = -int_time
    t.append(int_time)

    ship.cla()
    booster.cla()
    ship.plot(t, speed_ship, 'r', lw=1)
    ship.plot(t, altitude_ship, 'b', lw=1)
    booster.plot(t, speed_booster, 'r', lw=1)
    booster.plot(t, altitude_booster, 'b', lw=1)
    print(t, speed_ship, altitude_ship, speed_booster, altitude_booster)
    plt.pause(0.1)


def thread_plot():
    while True:
        data = main.on_plot_complete()
        plot_data(data["data"], data["timestamp"])
