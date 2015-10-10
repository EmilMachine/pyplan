# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 09:46:28 2015

@author: emil
"""
# todo use cpickle instead
import pickle as pickle

def intersect(t1,t2):
    return list(set(t1) & set(t2))

def difference(t1,t2):
    # Note it only return element in t1 not in t2.
    # Elements in t2 not in t1 are not returned.
    return list(set(t1) - set(t2))

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


def get_all_possible_combi(possible_cotasks):

    master = []
    # initiate recursion
    for i,tmp_cotasks in enumerate(possible_cotasks):
        tmp_tasks = [i]
        # do recursion for one
        # master is changed within the function.
        master = get_one_possible_combi(i,possible_cotasks,tmp_tasks,tmp_cotasks,master)

    return master

# Function is recursive.
# In most cases that would be slower than iterative versions.
# It might also cause errors as python has default 1000 recursion limit.
def get_one_possible_combi(i,possible_cotasks,tmp_tasks,tmp_cotasks,master):
    # define base case.
    # tmp_cotasks is empty. No more tasks can be combined.
    if not(tmp_cotasks):
        # Do not include solutions with lower i's
        # ensure no dublicates are stored in master
        if True in [k<i for k in tmp_tasks]:
            return master
        else:
            return master + [tmp_tasks]
    else:
        # pop first compatible task. Now called task j.
        j = tmp_cotasks[0]

        # get new tasks that can be combined with task j.
        i_and_j = intersect(tmp_cotasks,possible_cotasks[j])
        new_tmp_tasks = tmp_tasks + [j]

        master = get_one_possible_combi(i,possible_cotasks,new_tmp_tasks,i_and_j,master)

        # get tasks that can NOT be combined with task j
        i_and_not_j = difference(tmp_cotasks,possible_cotasks[j]+[j])
        # if no disagreement don't create new recursive branch.
        # Otherwise we will store subsets of full solution.
        if i_and_not_j:
            master = get_one_possible_combi(i,possible_cotasks,tmp_tasks,i_and_not_j,master)

        return master

# === MAIN ===

def main():
    with open('test_data/fysrevy_data.pkl', "rb") as input_file:
        in_data = pickle.load(input_file)
    input_file.close()
    # in_data is a dict with
    # 'actors':actors,
    # 'actors_name':actors_name,
    # 'tasks':tasks,
    # 'tasks_name':tasks_name

    tasks = in_data['tasks']

    pos_tasks = task_possible(tasks)
    # print(pos_tasks)


    # Test recursion for 0 case
    i = 0
    possible_cotasks = pos_tasks
    tmp_tasks = [i]
    tmp_cotasks = possible_cotasks[i]
    master = []

    master = get_one_possible_combi(i,possible_cotasks,tmp_tasks,tmp_cotasks,master)
    print(master)


    # try recursion for all
    master = get_all_possible_combi(pos_tasks)

    print(master)
    print(len(master))

if __name__ == '__main__':
    main()







