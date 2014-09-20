#!/usr/bin/python
import operator

'''
This method is a helper function that helps change a list to 
a dictionary with counts of each word and gets a sorted list 
based on the frequency of each word.
'''
def helper(data):
    total_count = len(data)
    result_dict = dict( [ (i, float(data.count(i))/total_count) for i in set(data) ] )
    sorted_dict = sorted(result_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:20]
    #print sorted_dict
    return result_dict

'''
This method is a helper function that helps change a list to 
a dictionary with counts of each word and gets a sorted list 
based on the frequency of each word.(smoothed version)
'''
def smoothing_helper(data, V):
    total_count = len(data)
    result_dict = dict( [ (i, float(data.count(i) + 1) / (total_count + V)) for i in set(data) ] )
    sorted_dict = sorted(result_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:20]
    #print sorted_dict
    return result_dict

'''
This method is for part1: The Collection Background Language Model.
'''
def collection_background(location):
    data = []
    f = open(location)
    for line in f:
        each_line = line.split()
        data.extend(each_line)
    result_dict = helper(data)
    return result_dict

'''
This method is for part2: The Topic Language Model.
'''
def topic(location, topic_word):
    f = open(location)
    topic_list = []
    for line in f:
        each_line = line.split()
        if topic_word in each_line:
            topic_list.extend(each_line)
    result_dict = helper(topic_list)
    return result_dict

'''
This method is for part3: Normalization of Topic Language Models.
'''
def normalization(location, topic_word):
    collection_dict = collection_background(location)
    topic_dict = topic(location, topic_word)
    normalized_dict = {x:float(topic_dict[x])/collection_dict[x] for x in topic_dict}
    sorted_dict = sorted(normalized_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:20]
    print "Normalized " + topic_word + ":"
    print sorted_dict

'''
This method is for part4: Smoothing of Background Language Model.
'''
def smoothing_collection_background(location, V):
    data = []
    f = open(location)
    for line in f:
        each_line = line.split()
        data.extend(each_line)
    result_dict = smoothing_helper(data, V)
    return result_dict

def smoothing_normalization(location, topic_word, V):
    collection_dict = smoothing_collection_background(location, V)
    topic_dict = topic(location, topic_word)
    normalized_dict = {x:float(topic_dict[x])/collection_dict[x] for x in topic_dict}
    sorted_dict = sorted(normalized_dict.iteritems(), key=operator.itemgetter(1), reverse=True)[:20]
    print "Smoothing Normalized " + topic_word + ":"
    print sorted_dict

'''
This is the main function of reading and analyzing the data files.
'''
def main():
    #read the file
    location = "yelp.txt"
    
    # part1
    #collection_background(location)
    # part2
    #chinese_topic_dict = topic(location, "chinese")
    #mexican_topic_dict = topic(location, "mexican")
    # part3
    #normalization(location, "chinese")
    #normalization(location, "mexican")
    # part4
    #smoothing_collection_background(location, 20000) 
    smoothing_normalization(location, "chinese", 20000)
    smoothing_normalization(location, "mexican", 20000)


if __name__ == '__main__':
    main()