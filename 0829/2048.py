# conding:utf-8
"""
this game is 2048
"""
import random
import sys,random,time,pygame
from pygame.locals import  *
 
pygame.init()
screen = pygame.display.set_mode((6,5))
 
random_list = [2,2,2,2,2,4]
 
def add_random_number(lst):
    """random a number from random_list to  4*4 list if the position is 0"""
    while True:
        random_index = random.randint(0,15)
        if lst[random_index] == 0:
            random_number = random.choice(random_list)
            lst[random_index] = random_number
            break
        else:
            continue
 
def deal_add_left(lst):
    """
    give a ordered list to left,
    this func do add number cal,return list
         4     4     *     *
         2     2     2     *
         2     2     2     *
         8     4     *     *
    ----->
         8     *     *     *
         4     2     *     *
         4     2     *     *
         8     4     *     *
    """
    for i in range(4):
        l = lst[i*4:i*4+4]
        l = func_left(l)
        lst[i*4:i*4+4] = l
 
def move_to_left(lst):
    """
    give a 4*4 list,return 4 rows number ,every row move to left
    and then return 4*4 list
    """
    for i in range(4):
        l = lst[i*4:i*4+4]
        l = return_lst_left(l)
        lst[i*4:i*4+4] = l
 
    return lst
 
def deal_add_right(lst):
    """the same as deal_add_left(lst),
    but this func deal with right operate"""
    for i in range(4):
        l = lst[i*4:i*4+4]
        l = func_right(l)
        lst[i*4:i*4+4] = l
 
    return lst
 
def move_to_right(lst):
    """4*4 list ,all rows move to right"""
    for i in range(4):
        l = lst[i*4:i*4+4]
        l = return_lst_right(l)
        lst[i*4:i*4+4] = l
 
    return lst
 
def func_left(lst):
    """[2,4,4,2] union the nearly same element to left-> [2,8,2,0]"""
    for i in range(3):
        if lst[i] == lst[i+1] and lst[i] != 0:
            lst[i] = lst[i] << 1
            lst[i+1:4] = lst[i+2:4] + [0]
    return lst
 
def func_right(lst):
    """[2,4,4,2] union the nearly same element to left-> [0,2,8,2]"""
    for i in range(3,0,-1):
        if lst[i] == lst[i-1] and lst[i] != 0 and lst[i-1] != 0:
            lst[i] = lst[i] << 1
            lst[0:i] =  [0]+lst[0:i-1] 
    return lst
 
def deal_add_top(lst): 
    """get 4 column from 4*4 list,then do func_left for every column"""
    for i in range(4):
        l = lst[i:16:4]
        l = func_left(l)
        lst[i:16:4] = l
    return lst
 
 
def return_lst_left(lst):
    """give a list(4 number),return a list which all number left ordered if it > 0
    [2,0,4,4] ---->[2,4,4,0]"""
    l = []
    for x in lst:
        if x > 0:
            l.append(x)
    l += [0,0,0,0]
    l = l[0:4]
    return l
 
def move_to_top(lst):
    """the same as move_to_left"""
    for i in range(4):
        l = lst[i:16:4]
        l = return_lst_left(l)
        lst[i:16:4] = l
 
    return lst
 
def deal_add_buttom(lst): 
    """the same as move_to_right"""
    for i in range(4):
        l = lst[i:16:4]
        l = func_right(l)
        lst[i:16:4] = l
    return lst
 
def return_lst_right(lst):
    """give a list(4 number),return a list which all number right ordered if it > 0
    [2,0,4,4] ---->[0,2,4,4]"""
    l = []
    while len(lst) > 0:
        x = lst.pop()
        if x > 0:
            l.append(x)
    l += [0,0,0,0]
    l = l[0:4]
    l.reverse()
    return l
 
def move_to_buttom(lst):
    """the same as move_to_right"""
    for i in range(4):
        l = lst[i:16:4]
        l = return_lst_right(l)
        lst[i:16:4] = l
    return lst
 
def print_result(lst):
    """print result as following:
     4     2     *     *
     4     *     *     *
     4     *     *     *
     8     2     *     2
    """
    for i in range(4):
        for j in range(4):
            if lst[i*4+j] == 0:
                print("%6s"%"*",end="")
            else:
                print("%6d"%lst[i*4+j],end="") 
        print()
    print()
 
def action_a(number_list_test):
    deal_add_left(move_to_left(number_list_test))
def action_d(number_list_test):
    deal_add_right(move_to_right(number_list_test))
def action_w(number_list_test):
    deal_add_top(move_to_top(number_list_test))
def action_s(number_list_test):
    deal_add_buttom(move_to_buttom(number_list_test))
 
def deal_error_op_s_w(number_list_test):
    """key_s or key_w pressed,judge whether can operate"""
    count = 0 #count number of a element >0 in a list
    for x in number_list_test:
        if x > 0:
            count += 1
    if count == 16: #all element > 0
        cal = 0 #if nearly element is not equal,cal+1;
        #if cal ==12,it stand for no element is equal with it's nearby element
        for i in range(3):
            for j in range(4):
                #compare by row,row 1 compare with row 2
                if number_list_test[i*4+j] == number_list_test[(i+1)*4+j]:
                    return False
                else:
                    cal += 1
        if cal == 12:
            return True
    else:   
        return False
 
def deal_error_op_a_d(number_list_test):  
    """key_a or key_d pressed,judge whether can operate""" 
    count = 0
    for x in number_list_test:
        if x > 0:
            count += 1
    if count == 16:
        cal = 0 
        for i in range(4):
            for j in range(3):
                #compare by column,column 1 compare with column 2
                if number_list_test[i*4+j] == number_list_test[i*4+j+1]:
                    return False
                else:
                    cal += 1
        if cal == 12:
            return True
    else:   
        return False
 
def win_game(number_list_test):
    """if one element >= 2048,player win"""
    for x in number_list_test:
        if x >= 2048:
            print("Congratulation on your perfect preformance!")
            return True
    return False
 
 
def main1():
    pygame.init()
    screen = pygame.display.set_mode((1,1))
    number_list_test = [
    0,4,0,2,
    2,0,2,0,
    0,2,2,0,
    8,0,0,2,
    ]
    # random.shuffle(number_list_test)
    print_result(number_list_test)
    tag = False#if player reach 2048,save the choice of continue or not
    while True:
        if deal_error_op_s_w(number_list_test) == True and deal_error_op_a_d(number_list_test) == True:
            print("Game over!")
            exit()
        else:
            for event in pygame.event.get():
                if event.type ==KEYDOWN:
                    keys = pygame.key.get_pressed()
                    if keys[97]:#a
                        if deal_error_op_a_d(number_list_test) == False:
                            action_a(number_list_test)
                            add_random_number(number_list_test)
                            # print_result(number_list_test)
                        else:
                            print("cant move to left")
                    elif keys[115]:#s
                        if deal_error_op_s_w(number_list_test) == False:
                            action_s(number_list_test)
                            add_random_number(number_list_test)
                            # print_result(number_list_test)
                        else:
                            print("can't move to buttom")
                    elif keys[119]:#w
                        if deal_error_op_s_w(number_list_test) == False:
                            action_w(number_list_test)
                            add_random_number(number_list_test)
                            # print_result(number_list_test)
                        else:
                            print("can't move to top")
                    elif keys[100]:#d
                        if deal_error_op_a_d(number_list_test) == False:
                            action_d(number_list_test)
                            add_random_number(number_list_test)
                            # print_result(number_list_test)
                        else:
                            print("can't move to right")
                    elif keys[112]: #q
                        #to add move action if needed
                        pass
                    else:
                        exit()
                elif event.type == KEYUP:
                    print_result(number_list_test)
        if tag == False:
            win = win_game(number_list_test)
            if win:
                next = input("continue or not,press y/Y to continue")
                if next == 'y' or next == 'Y':
                    tag = True
                    continue
                else:
                    exit()
 
if __name__ == "__main__":
    main1()
