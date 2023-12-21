import argparse
import pandas as pd
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    args = parser.parse_args()
    dataFile = args.data

    data = pd.read_csv(dataFile, header=None)

    total = len(data)
    num_a = (data[0]=='A').sum()
    num_b = (data[0]=='B').sum()
    pa = num_a/total
    pb = num_b/total

    attr1 = data[1]
    attr2 = data[2]
    class_label = data[0]
    sum1a = sum1b = 0
    sum2a = sum2b = 0

    for i in range(total):
        if(class_label[i] == 'A'):
            sum1a += attr1[i]
            sum1b += attr2[i]
        else:
            sum2a += attr1[i]
            sum2b += attr2[i]
    mean1a = sum1a/num_a
    mean2a = sum1b/num_a
    mean1b = sum2a/num_b
    mean2b = sum2b/num_b

    s1a = s1b = 0
    s2a = s2b = 0
    for i in range(total):
        if (class_label[i] == 'A'):
            s1a += ((attr1[i]-mean1a) ** 2)
            s2a += ((attr2[i]-mean2a) ** 2)
        else:
            s1b += ((attr1[i] - mean1b) ** 2)
            s2b += ((attr2[i] - mean2b) ** 2)

    var1a = s1a / (num_a-1)
    var1b = s1b / (num_b-1)
    var2a = s2a / (num_a-1)
    var2b = s2b / (num_b-1)

    miss_count = 0
    for i in range(total):
        f_1_a = (1/(np.sqrt(2*np.pi*var1a)))*np.exp(-((attr1[i]-mean1a)**2)/(2*var1a))
        f_2_a = (1/(np.sqrt(2*np.pi*var2a)))*np.exp(-((attr2[i]-mean2a)**2)/(2*var2a))
        f_1_b = (1/(np.sqrt(2*np.pi*var1b)))*np.exp(-((attr1[i]-mean1b)**2)/(2*var1b))
        f_2_b = (1/(np.sqrt(2*np.pi*var2b)))*np.exp(-((attr2[i]-mean2b)**2)/(2*var2b))
        prod_a = pa * f_1_a * f_2_a
        prob_b = pb * f_1_b * f_2_b
        if(class_label[i] == 'A' and prod_a<prob_b):
            miss_count += 1
        if(class_label[i] == 'B' and prod_a>prob_b):
            miss_count += 1


    print("{},{},{},{},{}".format(mean1a, var1a, mean2a, var2a, pa))
    print("{},{},{},{},{}".format(mean1b, var1b, mean2b, var2b, pb))
    print("{}".format(miss_count))