#!/usr/bin/python
'''
Created on Nov 1, 2013
'''

'''
This method is for changing a file into a list of lines.
'''
def file_to_list(input_file):
    data = []
    for line in input_file:   
        each_line = line.split(',')
        line_len = len(each_line) # 9
        each_line_x = each_line[:(line_len - 1)]
        each_line_y = each_line[line_len - 1]
        each_line_y = each_line_y.rstrip()
        data.append((each_line_x, each_line_y))
    #print data[len(data)-2][1].rstrip()
    return data


'''
Class of Naive Bayes algorithm
'''
class NaiveBayes:
    def __init__(self, n):
        self.data = []
        self.dim = n
        self.labels = {} # dictionary of labels
        #self.totals = {}
        self.counts = [{} for i in range(n)] # list of all 
                                             # dictionaries of features
        self.features_sets = [set() for i in range(n)] # ensure no duplicates

    '''
    This method initializes the (training) data.
    '''
    def addData(self, data):
        for row in data:
            row_x_len = len(row[0])
            if row_x_len != self.dim:
                return False

        self.data.extend(data);

        for row in data:
            if row[1] not in self.labels:
                self.labels[row[1]] = 1
            else:
                self.labels[row[1]] += 1
        #print self.labels.keys()
        #print self.labels.values()
        return True    

    '''
    This method trains the training data.
    '''
    def train(self):
        for row in self.data:
            row_x = row[0]
            row_y = row[1] # label

            for i in range(self.dim):
                new_feature = row_x[i]
                self.features_sets[i].add(new_feature);

                if row_y not in self.counts[i]:
                    self.counts[i][row_y] = {}

                if new_feature not in self.counts[i][row_y]:
                    self.counts[i][row_y][new_feature] = 1
                else:
                    self.counts[i][row_y][new_feature] += 1

        #for j in range(8):
        #    print len(self.features_sets[j])
        #    print self.features_sets[j]
        #    print 'Bachelors' in self.features_sets[j]

    '''
    This method gets a specific conditional probablity.
    With the given feature_detail and label provided.
    '''
    def get_probability(self, feature_detail, label):
    	index = 0
        for i in range(self.dim):
            if feature_detail in self.features_sets[i]:
                index = i
        theta_ijk = 0.0 
        if feature_detail in self.counts[index][label]:
            numerator = float(self.counts[index][label][feature_detail]) + 1
            denominator = self.labels[label] + len(self.features_sets[index])
            theta_ijk = numerator / denominator
        return theta_ijk

    def get_prior(self, label):
        train_data_count = len(self.data)
        pi_k = float(self.labels[label]) / train_data_count	
        return pi_k

    '''
    This method predicts on the test data based on the model trained from
    the training data.
    '''
    def predict(self, test):
        if len(test) != self.dim:
            print "Unclassifiable test data."
            return False
        new_data = {} # dictionary to store feature_num:new_row_x
        ps = []
        for i in range(self.dim): # 0 - 7
            if test[i] not in self.features_sets[i]:
                new_data[i] = test[i]
        
        for row_y in self.labels:
            train_data_count = len(self.data)
            pi_k = float(self.labels[row_y]) / train_data_count
            theta_ijk = pi_k
            i = 0
            while theta_ijk > 0.0 and i < self.dim:
                if i not in new_data:
                    new_feature = test[i]
                    if new_feature in self.counts[i][row_y]:
                        numerator = float(self.counts[i][row_y][new_feature]) + 1
                        denominator = self.labels[row_y] + len(self.features_sets[i])
                        theta_ijk *= numerator / denominator
                    else:
                        theta_ijk = 0.0
                i += 1
            ps.append((theta_ijk, row_y))

        #if len(new_data) != 0:
        #    print len(new_data)
        # In this case, no new data are found.
        #print ps
        return max(ps, key = lambda x:x[0])

'''
The main function for training and testing.
'''
def test():
    train_input_file = open('train_data.txt', 'rU')
    train_data = file_to_list(train_input_file)
    train_input_file.close()
    features_dim = len(train_data[0][0])
    test_input_file = open('test_data.txt', 'rU')
    test_data = file_to_list(test_input_file)
    test_input_file.close()
    nb = NaiveBayes(features_dim)
    nb.addData(train_data)
    nb.train()
    ###
    prob = nb.get_prior('<=50K')
    print 'Probability for (a) is:', prob
    ###
    prob = nb.get_probability('Bachelors', '>50K')
    print 'Probability for (b) is:', prob
    ###


    test_data_count = len(test_data)
    correct = 0
    for row in test_data:
        test = nb.predict(row[0]) # predict with first 8 fields
        if test[1] == row[1]:
            correct += 1
    print '# of Accurate Predictions:', correct
    print '# of Total Tests:', test_data_count	
    print 'Prediction Accuracy:', float(correct) / test_data_count
    print 'Error Rate', float(test_data_count - correct) / test_data_count
if __name__ == '__main__':
    test()
