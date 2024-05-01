import json



def hasVoted(name):
    with open(r'./data.json', 'r') as file:
        data = json.load(file)

    for obj in data['names'] :
        if name == obj:
            return True
    return False



while True:
    name= input('Enter your name: ')
    choice = input('Enter you choice before/after: ')



    if not hasVoted(name):
        with open(r'./data.json', 'r') as file:
            data = json.load(file)
        
        data['names'][name] = choice
        

    with open(r'./data.json', 'w') as json_file:
    # Write the updated JSON data back to the file
        json.dump(data, json_file, indent=2)

    with open(r'./data.json', 'r') as file:
        data = json.load(file)
        
        data['counters'][choice]+=1
        

    with open(r'./data.json', 'w') as json_file:
    # Write the updated JSON data back to the file
        json.dump(data, json_file, indent=2)





