import xml.etree.ElementTree as ET
import sys
import time

from os import listdir
from os.path import isfile, join

def main(XML_FOLDER):
    # XML_FOLDER = 'shhs/polysomnography/annotations-events-nsrr/shhs1/'
    XML = '-nsrr.xml'
    TRUTH_OUTPUT_FOLDER = 'ground_truths/'
    files = prepFiles(XML_FOLDER)

    t = 0
    for f in files:
        t = t + 1
        times = getStagesFromXML(XML_FOLDER + f + XML)
        print 'Finished XML no. {} out of {}'.format(t, len(files)) + ' --- {}% completed.'.format(int(float(t) / len(files) * 100))
        with open(TRUTH_OUTPUT_FOLDER + 'truth_' + f + '.txt', 'w') as res:
            res.write('\n'.join('%s %s' % x for x in times))

def prepFiles(path):
    return [f[:-9] for f in listdir(path) if isfile(join(path, f))]

def getStagesFromXML(xmlFile):
    timeStages = [] # [(time, stage)]
    tree = ET.parse(xmlFile)

    root = tree.getroot()

    events = root.findall('./ScoredEvents/ScoredEvent[EventType="Stages|Stages"]')

    for e in events:
        child = list(e)
        eventType = child[0].text
        eventConcept = child[1].text
        start = int(float(child[2].text))
        duration = int(float(child[3].text))
        end = start + duration
        wakeStage = 0
        if eventConcept.split('|')[0] == 'Wake':
            wakeStage = 1
        for tick in range(duration):
            timeStages.append((start + tick + 1, wakeStage))

    return timeStages

start = time.time()

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        path = str(sys.argv[1])
        main(path)
        end = time.time()
        print 'Time taken: {}'.format(end - start)
    else:
        print 'Please input XML folder path.'
