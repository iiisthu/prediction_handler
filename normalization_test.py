from sklearn import preprocessing
import numpy as np

def normalization(input, scaler_file, output_file):
    lines = input.split(';')

    data_mat = []
    count = 0
    for line in lines:
        count += 1
        if count % 10000 == 0:
            print count
        row = []
        #values = line.split(',')[2:]        # if the power value is attached
        values = line.split(',') 
        for k in range(len(values)):
            values[k] = float(values[k])
        data_mat.append(values)

    print 'now begin normalizing...'
    #scaler_file = file_path + 'ts_yq01-ps-global-42-train-scaler.data'
    fin = open(scaler_file, 'r')
    lines = fin.readlines()
    scaler = preprocessing.StandardScaler(with_mean = True, with_std = True, copy = False)
    fin.close()
    means = lines[0].split()
    stds = lines[1].split()
    for k in range(len(means)):
        means[k] = float(means[k])
        stds[k] = float(stds[k])
    scaler.mean_ = np.array(means)
    scaler.std_ = np.array(stds)
    
    data_mat = np.array(data_mat)
    data_mat = scaler.transform(data_mat)
    
    print 'now output~'
    #output_file = file_path + 'dnn-' + file_name
    fout = open(output_file, 'w')
    length = len(data_mat[0])
    print 'length', length
    count = 0
    for row in data_mat:
        count += 1
        line = '0;0'
        for k in range(length):
            line += ' ' + str(row[k])
        line += ';1 ' + str(row[0]) + '\n'
        fout.write(line)
        if count % 10000 == 0:
            print count
            fout.flush()
    
    fout.close()
