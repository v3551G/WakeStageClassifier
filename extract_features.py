import numpy as np
import sys
import time
from mne.io import read_raw_edf
from pyspark import SparkContext, SparkConf
from os import listdir
from os.path import isfile, join

def main(path):
    sc = getSC()
    files = prepFiles(path)
    files.sort()
    # sc = SparkContext('local', 'WakeStageClassifier')
    for file in files:
        getEEGFeatures(sc, path, file)

def prepFiles(path):
    return [f[:-4] for f in listdir(path) if isfile(join(path, f))]

def getSC():
    sc_conf = SparkConf()
    sc_conf.setAppName('Wake-Stage-Classifier-App')
    sc_conf.setMaster('spark://192.168.0.14:7077')
    sc_conf.set('spark.executor.memory', '14g')
    sc_conf.set('spark.executor.cores', '8')
    sc = None
    try:
        sc.stop()
        sc = SparkContext(conf=sc_conf)
    except:
        sc = SparkContext(conf=sc_conf)
    return sc

def getEEGFeatures(sc, EDF_FOLDER, file):
    TRUTH_FOLDER = 'ground_truths/truth_'
    TXT = '.txt'
    EDF = '.edf'
    OUTPUT_FOLDER = 'features/'
    raw = read_raw_edf(EDF_FOLDER + file + EDF, preload=True)
    channels = raw.info['ch_names']
    eeg_index = channels.index('EEG')
    sfreq = int(raw.info['sfreq'])
    start_time = 1
    end_time = int(round(raw.times[-1]))

    data, times = raw[:8, 1 * sfreq:sfreq * end_time]

    # Min-Max Normalize
    for i in range(len(data)):
        minVal = np.min(data[i])
        maxVal = np.max(data[i])
        data[i] = (data[i] - minVal) / (maxVal - minVal)

    data = data.T
    times = times[0:len(times):sfreq]
    data = data[0:len(data):sfreq]
    dataRDD = sc.parallelize(data).zipWithIndex().map(lambda x: (x[1] + 1, x[0]))
    truth = sc.textFile(TRUTH_FOLDER + file + TXT)
    truth = truth.map(lambda x: x.split(' ')).map(lambda x: (int(x[0]), int(x[1])))
    joined = dataRDD.leftOuterJoin(truth).map(lambda x: (x[1][0], x[1][1]))
    features = joined.map(lambda x: str(x[1]) + ' ' + ' '.join(str(i + 1) + ':' + str(x[0][i]) for i in range(len(x[0]))))
    features.repartition(1).saveAsTextFile(OUTPUT_FOLDER + file + '_svmlight/')

start = time.time()

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        path = str(sys.argv[1])
        main(path)
        end = time.time()
        print 'Time taken: {}'.format(end - start)
    else:
        print 'Please input XML folder path.'
