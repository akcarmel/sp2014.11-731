import codecs
def get_best_sent(indices,source_file,lin,clean):
    if lin:
        output_file='output.lin.txt'
    else:
        output_file='output.log.txt'
    if clean:
        output_file+='.clean'
    src=codecs.open(source_file,'r','utf-8')
    a=codecs.open(output_file,'w','utf-8')
    source_list=[]
    for src_line in src:
        sentence=src_line.split('|||')[1]
        source_list.append(sentence)
    src.close()
    for k,v in enumerate(indices):
        bestindex=100*int(k)+int(v)
        best_sentence=source_list[bestindex]
        #a.write(str(best_sentence)+'\n')
        a.write(best_sentence+'\n')
    a.close()
        

