# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 09:46:28 2015

@author: emil
"""

import pickle as pickle

def intersect(t1,t2):
    return(list(set(t1) & set(t2)))


def task_possible(tasks):
    pos_tasks = []
    for actor_list in tasks:
        if not actor_list: #not actor_list = list is empty
            pos_tasks.append([])
        else:
            tmp_list = []
            for i,al2 in enumerate(tasks):
                # Check if acotor list_is not empty and does not have actor overlap
                # TODO: FIX problem that int (1 entry) is not iterable
                if al2 and not(intersect(actor_list,al2)):
                    tmp_list.append(i)
            pos_tasks.append(tmp_list)
    return pos_tasks

#class note:
#    def


## === Old Falied recursive list ==
def task_combi(master,tmp,combi_list,pos_list):
        if not(combi_list):
            # base case
            return tmp
        else:
            # build stuff
            for t in combi_list:
                tmp.append(t)
                combi_list = intersect(combi_list,pos_list[t])
                tmp = task_combi(master,tmp,combi_list,pos_list)
                master.append(tmp)
            return master

# todo rename function to something more accurate
def get_all_list(pos_list):
    master = []
    for i,t1 in enumerate(pos_list):
        tmp = [i]
        next_master = task_combi([],tmp,t1,pos_list)
        # TODO make nested list merge that exclude dublicates
        master += next_master



# === MAIN ===

with open('test_data/fysrevy_data.pkl', "rb") as input_file:
    in_data = pickle.load(input_file)

# in_data is a dict with
# 'actors':actors,
# 'actors_name':actors_name,
# 'tasks':tasks,
# 'tasks_name':tasks_name

tasks = in_data['tasks']

pos_tasks = task_possible(tasks)

g = get_all_list(pos_tasks)









