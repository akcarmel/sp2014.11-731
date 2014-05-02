import codecs
import subprocess
import sys
'''
def WriteMeteorFiles(sentences, hyp_filename, ref_filename):
  hyp_file = open(hyp_filename, "w")
  ref_file = open(ref_filename, "w")
  for sentence in sentences:
    for hyp in sentence.hypos:
      ref_file.write(" ".join(sentence.ref) + "\n")
      hyp_file.write(" ".join(hyp.words) + "\n")
  hyp_file.close()
  ref_file.close()
'''

def run_meteor(hyp_filename, ref_filename, meteor_out_filename):
  meteor_jar = "./meteor-1.4/meteor-1.4.jar"
  meteor_command=["java", "-Xmx1G", "-jar " + meteor_jar, hyp_filename, ref_filename]
  sys.stderr.write("Running Meteor scorer\n")
  #WriteMeteorFiles(sentences, hyp_filename, ref_filename)
  meteor_stdout = subprocess.check_output(" ".join(meteor_command), shell=True)
  open(meteor_out_filename, "w").write(meteor_stdout)
  return meteor_stdout.split("\n")

def generate_source_hyp_files(ref,new_ref,hyp):
    g=codecs.open(new_ref,'w','utf-8')
    f=codecs.open(ref,'r','utf-8')
    for myline in f:
        for i in range(100):
            g.write(myline)
    f.close()
    g.close()

def get_meteor_scores(ref,new_ref,hyp,meteor_out):
    generate_source_hyp_files(ref,new_ref,hyp)
    run_meteor(hyp,new_ref,meteor_out)

def extract_only_sentences(hypfeat,hyp):
    f=codecs.open(hypfeat,'r','utf-8')
    g=codecs.open(hyp,'w','utf=8')
    for myline in f:
        sentence=myline.strip().split('|||')[1]
        g.write(sentence+'\n')
    g.close()
    f.close()
    
def parse_meteor_scores(meteor_out):
    grep_command=["grep", "Segment", meteor_out]
    grep_stdout = subprocess.check_output(" ".join(grep_command), shell=True)
    final_file=meteor_out+'.final'
    open(final_file, "w").write(grep_stdout)

if __name__=="__main__":
    meteor_out="meteor.out"
    hyp="experimental_data/dev.100best.sent"
    extract_only_sentences("experimental_data/dev.100best",hyp)
    get_meteor_scores("experimental_data/dev.ref","experimental_data/dev.ref.new",hyp,meteor_out)
    parse_meteor_scores(meteor_out)
    

    

