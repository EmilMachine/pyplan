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

def get_all_possible_combi(possible_cotasks):

    master = []
    # initiate recursion
    for i,tmp_cotasks in enumerate(possible_cotasks):
        tmp_tasks = [i]
        # do recursion for one
        # master is changed within the function.
        master = get_one_possible_combi(i,possible_cotasks,tmp_tasks,tmp_cotasks,master)

    return master


def get_task_lookup(task_lst, tasks_lst_of_lst):
    # lst = list.
    # taskes a list of tasks_list and make a lookup table
    # the lookuptable can be used to enter a task id, and get the ids of the list of lists, where the task is in.
    n_tasks = len(task_lst)

    task_combi_lookup = []

    # TODO can maybe be rewritten to list comprehention
    # loop over tasks (we assumme all tasks are numbered from 1 to n)
    for task in range(0,n_tasks):
        tmp = []
        # take a list of list (e.g. cotasks_master)
        for entry_id,entry in enumerate(tasks_lst_of_lst):
            # for each entry check if our task is one of them
            # if it is add that entry id_number to our lookup table for that task.
            if task in entry:
                tmp.append(entry_id)
        # After inner iteration inner lookup is complete.
        # The lookup list is added to the list.
        # (since we do them in order, the id of task and lookup will match)
        task_combi_lookup.append(tmp)

    return task_combi_lookup


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
    #print(tasks)

    pos_tasks = task_possible(tasks)
    # print(pos_tasks)


    # Test recursion for 0 case
    i = 0
    possible_cotasks = pos_tasks
    tmp_tasks = [i]
    tmp_cotasks = possible_cotasks[i]
    master = []

    master = get_one_possible_combi(i,possible_cotasks,tmp_tasks,tmp_cotasks,master)


    # try recursion for all
    cotask_master = get_all_possible_combi(pos_tasks)

    print(cotask_master)
    print(len(cotask_master))

    cotask_lookup = get_task_lookup(tasks,cotask_master)

    for id_t, t in enumerate(tasks):
        if t:
            print(id_t,cotask_lookup[id_t])

if __name__ == '__main__':
    main()







