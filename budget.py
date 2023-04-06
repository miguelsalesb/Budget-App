from abc import abstractmethod
from functools import total_ordering
import math


class Category:

    description = ""
    total_amount = 0.00
    amount_object = dict()
    total_category = 0


    def __init__(self, category):
        self.category = category
        self.ledger = list()


    def __str__(self):
        text = list()
        category_length = len(self.category)
        # append all the text to the text list
        text.append("*" * int((30 - category_length)/2) + self.category + "*" * int((30 - category_length)/2) + "\n")
        for x in range(len(self.ledger)):
            amount_len = len("{:.2f}".format(self.ledger[x]['amount']))
            desc = self.ledger[x]['description'] + " " * (23 - len(self.ledger[x]['description']))
            amount = " " * (7-amount_len) + "{:.2f}".format(self.ledger[x]['amount'])
            self.total_category = self.total_category + self.ledger[x]['amount']
            text.append(desc[:23] + amount[:7] + "\n")
        text.append("Total: " + "{:.2f}".format(self.total_category))
        # put all the list items in a single string
        item_list = "".join(text)
        return item_list


    def deposit(self, amount=0, description=""):
        self.amount_object['amount'] = float(amount)
        self.amount_object['description'] = description
        self.total_amount = self.total_amount + float(amount)
        self.ledger.append(self.amount_object.copy())


    def withdraw(self, amount=0, description=""):
        if self.total_amount - amount < 0:  
            print('There are not enough funds in ' + self.category + ' to withdraw ' + str("{:.2f}".format(amount)))
            return False
        else:
            self.amount_object['amount'] = 0 - float(amount)
            self.amount_object['description'] = description
            self.total_amount = self.total_amount - float(amount)
            self.ledger.append(self.amount_object.copy())
            return True


    def get_balance(self):
        return self.total_amount


    def transfer(self, transfer_amount, another_budget_category):
        if self.get_balance() > transfer_amount:
            success = True 
            self.withdraw(transfer_amount, "Transfer to " + str(another_budget_category.category))
            another_budget_category.deposit(transfer_amount, "Transfer from " + self.category)
        else:
            success = False
        
        return success
    
    
    def check_funds(self, amount=0):
        balance = self.get_balance()
        if amount > balance:
            return False
        else:
            return True


def create_spend_chart(categories):

    total_withdrawls = 0
    withdrawls = dict() 
    percentages = dict()
    categories_list = list()
    categories_size = list()

    for cat in categories:
        # add the categories to a list
        categories_list.append(cat.category)
        # add the categories length
        categories_size.append(len(cat.category))
        for x in range(len(cat.ledger)):
            # get only the withdrawls
            if cat.ledger[x]['amount'] < 0 and 'Transfer' not in cat.ledger[x]['description']:
                # withdrawls by category 
                withdrawls[cat.category] = withdrawls.get(cat.category, 0) + cat.ledger[x]['amount']
                # total value of withdrawls
                total_withdrawls = total_withdrawls + cat.ledger[x]['amount']
        
    # get the percentage spent by category        
    for k in withdrawls:
        percentages[k] = "{:.0f}".format((withdrawls[k] * 100) / total_withdrawls)

    # the category name with the greater length 
    # 
    max_length = max(categories_size)

    l = list()

    # put dictionaries inside the list, one for each category 
    # add the index key
    # and a value with the corresponding category letter
    # the loop has a range with the length of the largest category
    for cat in range(len(categories_list)):
        cat_dict = dict()
        for v in range(max_length):
            if v < categories_size[cat]:
                cat_dict[v] = categories_list[cat][v] + "  "
            # when the size of the category is smaller than the largest category
            # since there is no letter to add, add a blank space    
            elif v >= categories_size[cat]:
                cat_dict[v] = "   "
        l.append(cat_dict.copy())


    # append the categories letters
    # starting with the first letter from each category
    # then the second, and so on 
    for i in l: 
        l_lis = list()    
        l_list = list()
               
        for k, v in i.items():
            count = 0
            for b in range(len(categories_list)):
            # append a letter from each of the categories and the necessary spaces
                if count == 0:
                    l_lis.append("     " + l[b][k])
                elif count != 0:
                    l_lis.append(l[b][k])
                count = count + 1    
            l_list.append(l_lis.copy())    
            l_lis = []


    l_perc = list()
    # loop from 100 in descending order with increments of 10
    for p in range(100,-1,-10):
        perc_dict = dict()
        perc_dict[p] = p
        l_perc.append(perc_dict.copy())
        for k, v in percentages.items():
            # if for instance the percentage is 75, it adds 10 to it 
            # so that each time the loop value is lower
            # it adds "o  " to the dictionary
            # else it adds "   "
            if p <= math.floor(int(v)):
                perc_dict[p] = "o  "
                l_perc.append(perc_dict.copy())
            else:
                perc_dict[p] = "   "
                l_perc.append(perc_dict.copy())
    n_list = list()
    count = -1

    for pe in l_perc:
        for k, v in pe.items():
            count = count + 1
            # there are four dictionaries for each multiple of 10
            # {100: 100}, {100: '   '}, {100: '   '}, {100: '   '}
            # get the key and the remaining 3 values 
            if count % (len(categories) + 1) == 0:
            # add k + "|" - result: "0|"
                if k == 100:
                    n_list.append(str(k) + "| ")
                elif k == 0:
                    n_list.append("  " + str(k) + "| ")
                else:
                    n_list.append(" " + str(k) + "| ")
            else:
                # add "   " three times
                n_list.append(v)
               
            # put arrays inside one list
            # with each multiple of 10 values
            # ex.:  [['100|', '   ', '   ', '   '],...
            f_lis = list()
            f_list = list()
            con = 0
            for f in n_list:
                f_lis.append(f)
                con = con + 1
                if con % (len(categories) + 1) == 0:
                    f_list.append(f_lis.copy())
                    f_lis = []        
           

    text = list()
    text.append("Percentage spent by category")
    for d in range(len(f_list)):
        text.append("\n")
        for v in range(len(f_list[d])):
            text.append(str(f_list[d][v]))
    text.append("\n" + "    -" + str((len(categories)*("---"))) + "\n")
    siz = len(l_list)
    for l in range(len(l_list)):
        for v in l_list[l]:
            text.append(str(v))
        if l != (siz - 1):
            # don't append a newline after the last item    
            text.append("\n") 
        else:
            break
       
    chart = "".join(text)
    
    return chart