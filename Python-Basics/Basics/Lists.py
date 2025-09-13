print('Converting Temperature of Celcius Scale To Kelvin: ')
temps = [22.1, 23.5, -9999, 34.0, 23.0, -285.95]
new_temps = [temp + 273.15 for temp in temps if temp > -273.15]
print(new_temps)

def summing_list(lst):
    return sum(float(elem) for elem in lst )

print(summing_list(temps))
print(summing_list(new_temps))

