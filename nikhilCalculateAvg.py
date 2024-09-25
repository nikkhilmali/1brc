import time
import logging

LOGGER = logging.getLogger("SCRIPT")

start = time.time()

f = open("measurements_1M.txt", "r")
city_list = f.readlines()

print(f"Total Number for values => {len(city_list)}")

filter_city_list = []
city_list_dict = {}
result_dict = {}

for cl in city_list:
    filter_city_list.append(cl[:-1])

for fcl in filter_city_list:
    temp = fcl.split(";")
    temp_list = city_list_dict.get(temp[0], [])
    if temp_list is None:
        temp_list = []
    temp_list.append(float(temp[1]))
    temp_list.sort()
    city_list_dict[temp[0]] = temp_list

for city, temp in city_list_dict.items():
    min_value = temp[0]
    max_value = temp[-1]
    mean = round(sum(temp) / len(temp), 1)
    result_dict[city] = [min_value, mean, max_value]

print(f"Time Taken =>{time.time() - start}s")
