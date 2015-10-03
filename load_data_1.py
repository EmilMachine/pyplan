# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 20:51:08 2015

@author: emil
"""
#import numpy as np
import cPickle as pickle

# TODO consider putting in class?
# TODO add other than latex load
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def load_data_1(filename):
    # define variables
    actors_name = []   
    tasks_name = []
    actors = []    
    tasks = []
    
    collect_actors = False
    
    
    file = open(filename,'r')            
    try:
        for line in file:
            # Collect actor names
            if collect_actors:
                if '}' in line:
                    collect_actors = False
                    pos = line.find('}')
                    line = line[:pos+1]
                pos = line.find('@')
                actors_name.append(line[pos+1:-1])
                actors.append([])
            if line.startswith('\\actors{\n'):
                print line
                collect_actors = True
            
            # Collect task names and participants
            if has_numbers(line[:4]):
                # get name
                pieces = line.split('&')
                tasks_name.append(pieces[1].strip())
                # get task matrix
                # TODO make custom class to do more efficient 
                # TODO get do stuff
                
                
                #tasks_num = np.zeros([1,len(pieces[2:])])
                tasks_num = []
                #tasks[task_id] = []
                for nr,item in enumerate(pieces[2:]):
                    if not '\q' in item: tasks_num.append(nr)
                    
                tasks.append(tasks_num)

        # make revese actor lookup tasks.
        for task_num,actor_list in enumerate(tasks):
            for actor in actor_list:
                actors[actor].append(task_num)
                
                
        
    except:
        file.close()
        print('exception')
    file.close()
        
    return {'actors':actors,
            'actors_name':actors_name, 
            'tasks':tasks, 
            'tasks_name':tasks_name}


# --- dummy run test --- 
# - TODO: remove executeable code
# (bad practice...)


dummy_file = './test_data/rollematrix.tex'
out = load_data_1(dummy_file)
      
#print('actors_name')
#print(out['actors_name'])
#print('tasks_name')
#print(out['tasks_name'])
#print('actors')
#print(out['actors'])
#print('tasks')
#print(out['tasks'])
      
with open('test_data/fysrevy_data.pkl', 'wb') as output:
    pickle.dump(out, output, -1)
    
