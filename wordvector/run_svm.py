import numpy as np
from subprocess import call

#this readies the data for svm

# read the vectors.bin file and create a map
vec_dict = {}
# vec_file = open ('vectors.bin', 'r')

with open ('vectors.bin', 'r') as fp:
    for i, line in enumerate (fp):
        if i == 0:
            continue
        parts = line.split ()
        word = parts[0]
        vector = []
        for i in range (1, 201):
            vector.append (float (parts[i]))
        vec_dict[word] = np.array (vector)

# now we read the train data
with open ('train.tsv', 'r') as fp:
    with open ('training_data_svm', 'w') as fpw:
        final_vec = np.zeros (200)
        for line in fp:
            [_id, tweet, label] = line.split ("\t")
            tweet_parts = tweet.split ()
            for word in tweet_parts:
                if word in vec_dict:
                    final_vec = final_vec + vec_dict[word]

            final_vec = final_vec / 200
            write_line = label.strip ("\n").strip ()
            for i in range (200):
                write_line += " "
                write_line += str (i + 1) + ":"
                write_line += str (final_vec[i])
            write_line += "\n"
            fpw.write (write_line)


# now for the test data
with open ('test.tsv', 'r') as fp:
    with open ('test_data_svm', 'w') as fpw:
        final_vec = np.zeros (200)
        for line in fp:
            [_id, tweet, label] = line.split ("\t")
            tweet_parts = tweet.split ()
            for word in tweet_parts:
                if word in vec_dict:
                    final_vec = final_vec + vec_dict[word]

            final_vec = final_vec / 200
            write_line = label.strip ("\n").strip ()
            for i in range (200):
                write_line += " "
                write_line += str (i + 1) + ":"
                write_line += str (final_vec[i])
            write_line += "\n"
            fpw.write (write_line)


# call(["python", "easy.py", "training_data_svm", "test_data_svm"])
print ""
