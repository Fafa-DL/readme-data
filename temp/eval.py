import numpy as np

a  = np.array([[-5.577026524014705444e-03,-9.999411960755890671e-01,-9.300600307024509128e-03],
[-2.302812302839518654e-03,9.313562777788941816e-03,-9.999539762428479861e-01],
[9.999817967496450466e-01,-5.555352311489569761e-03,-2.354618875083813734e-03]])  
# print(np.linalg.inv(a))  
b = np.array([-1.372968924738809382e-01, -4.767565690522703736e-01, -8.905063382678727324e-01])

print(np.linalg.inv(a)) 

# A = np.matrix(a)
# B = np.matrix(b)
# print(A.I)
# print(-A.I.dot(B))

# from tqdm import tqdm
# from terminaltables import AsciiTable
# import numpy as np
# import time
# import random
# from math import cos, pi

# TOP1_ACCURACY = list(np.arange(90.00,95.87,0.01))
# TOP5_ACCURACY = list(np.arange(96.00,99.52,0.01))
# PRECISION = list(np.arange(90.00,99.87,0.01))
# RECALL = list(np.arange(90.00,99.87,0.01))
# TIME = list(np.arange(0.47,0.53,0.01))
    
# def annealing_cos(start, end, factor, weight=1):
#     cos_out = cos(pi * factor) + 1
#     return end + 0.5 * weight * (start - end) * cos_out

# def get_loss(epoch, epoches):

#     return 0.1 * pi * 100 ** ((epoches - epoch)/epoches)

# def main():
#     epoches = 500
#     train_batch = 197
#     val_batch = 23
#     start_lr = 1e-3
#     end_lr = 1e-5
#     # accList = list[90.15, 91.68, 92.33, 93.42, 94.26, 95.89, 96.77, 97.98, 98.32, 98.64, 98.67, 98.99.23, 99.01, ]
    
#     for epoch in range(epoches):
#         with tqdm(total=train_batch, desc=f'Train: Epoch {epoch + 1}/{epoches}', postfix=dict, mininterval=0.3) as pbar:
#             for i in range(train_batch):
#                 # print(i)
#                 pbar.set_postfix(**{'Loss': get_loss(i + epoch* epoches, train_batch * epoches), 
#                                     'Lr' : annealing_cos(start_lr, end_lr, epoch/epoches)
#                                     })
#                 # time.sleep(random.choice(TIME))
            
#                 pbar.update(1)

            
#         with tqdm(total=val_batch, desc=f'Test: Epoch {epoch + 1}/{epoches}', postfix=dict, mininterval=0.3) as pbar:
#             for i in range(val_batch):

#                 # time.sleep(random.choice(TIME))
            
#                 pbar.update(1)
        
#         epoch += 1
#         time.sleep(2)
#         t1_acc = random.choice(TOP1_ACCURACY)
#         print(t1_acc)
#         t5_acc = random.choice(TOP5_ACCURACY)
#         pre = random.choice(PRECISION)
#         rec = random.choice(RECALL)
#         f1s = 2 * pre * rec / (pre + rec)
#         TITLE = 'Validation Results'
#         TABLE_DATA = (
#         ('Top-1 Acc', 'Top-5 Acc', 'Mean Precision', 'Mean Recall', 'Mean F1 Score'),
#         (t1_acc, t5_acc, pre, rec, f1s)
#         )
#         table_instance = AsciiTable(TABLE_DATA, TITLE)
#         #table_instance.justify_columns[2] = 'right'
#         print()
#         print(table_instance.table)
#         print()
        
# if __name__ == "__main__":
#     main()