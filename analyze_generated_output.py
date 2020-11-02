import os
import sys

inp_file = sys.argv[1]
out_dir = sys.argv[2]

thresh = 10
trunc_length = 30

with open(inp_file) as f:
    lines = f.readlines()
f_cnt = 0
m_cnt = 0
f_words = {}
m_words = {}
for line in lines:
    words = line.split()
    word_set = set()
    for word in words[1:(trunc_length + 1)]:
        if not word in m_words.keys():
            m_words[word] = 0
            f_words[word] = 0
        word_set.add(word)
    if words[0] == "<MALE>:":
        m_cnt += 1
        for word in word_set:
            m_words[word] += 1
    else:
        f_cnt += 1
        for word in word_set:
            f_words[word] += 1

word_counts = []
for word in m_words:
    if m_words[word] + f_words[word] > thresh:
        p_given_m = m_words[word] / m_cnt
        p_given_f = f_words[word] / f_cnt
        p_given_m = max(p_given_m, 0.00000000001)
        ratio = p_given_f / p_given_m
        word_counts.append((ratio, p_given_f, p_given_m, word))

word_counts.sort(key = lambda x: x[0])

with open(os.path.join(out_dir, "word-occurence-analysis.txt"), 'w') as f_out:
    for word in word_counts:
        f_out.write("{0}:\t\t\t{1}\t\t{2}\t\t{3}\n".format(word[3],round(word[0], 5), round(word[1], 5), round(word[2], 5)))
    
he_words = ['he', 'him', 'his', 'male', 'man']
she_words = ['she', 'her', 'hers', 'female', 'woman']

with open(os.path.join(out_dir, "incorrect-gender-indicator.txt"), 'w') as f_out:
    for line in lines:
        words = line.split()
        if words[0] == "<MALE>:":
            for word in words[1:(trunc_length + 1)]:
                if word.lower() in she_words:
                    f_out.write(line)
                    break
        else:
            for word in words[1:(trunc_length + 1)]:
                if word.lower() in he_words:
                    f_out.write(line)
                    break


print("Number of female pages: ", f_cnt)
print("Number of male pages: ", m_cnt)