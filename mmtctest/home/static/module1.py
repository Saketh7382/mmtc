import pandas as pd
import json

file = 'C:\\Users\\Hp\\SRM Hackathon\\SRM Hackathon\\final\\trainjson.json'
file1 = 'C:\\Users\\Hp\\SRM Hackathon\\SRM Hackathon\\final\\flightjson.json'
with open(file) as train_file:
    dict_train = json.load(train_file)
# converting json dataset from dictionary to dataframe
train = pd.DataFrame.from_dict(dict_train, orient='columns')
train.reset_index(level=0, inplace=True)
with open(file1) as flight_file:
    dict_flight = json.load(flight_file)
flight = pd.DataFrame.from_dict(dict_flight, orient='columns')
flight.reset_index(level=0, inplace = True)

source = str(input("Enter source\n")).upper()
destination = str(input("Enter destination\n")).upper()

s = []
for i in range(0,train.shape[0]):
    b = []
    if train.iloc[i,12] == source:
        if train.iloc[i,7] == destination:
            print(train.iloc[i,1:])
            print('\n\n\n')
            b.append(train.iloc[i,:])
            s.append(b)
            
g = []
for i in range(0,flight.shape[0]):
    b = []
    if flight.iloc[i,7] == source:
        if flight.iloc[i,10] == destination:
            print(flight.iloc[i,1:])
            print('\n\n\n')
            b.append(flight.iloc[i,:])
            g.append(b)
