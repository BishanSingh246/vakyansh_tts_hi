"""**Importing Require Libraries**"""
from vakyansh.tts_infer.tts import TextToMel, MelToWav
from vakyansh.tts_infer.transliterate import XlitEngine
from vakyansh.tts_infer.num_to_word_on_sent import normalize_nums

import re
import numpy as np
from scipy.io.wavfile import write

from mosestokenizer import *
from indicnlp.tokenize import sentence_tokenize
import time
import pandas as pd

"""**Inference Code**"""
data = {
    "Index": [],
    "Text": [],
    "Before Writing Audio Time": [],
    "After Writing Audio Time": []
}

device = 'cuda'
print("device: " + device)

text_to_mel = TextToMel(glow_model_dir='vakyansh/tts_infer/odia/glow', device=device)
mel_to_wav = MelToWav(hifi_model_dir='vakyansh/tts_infer/odia/hifi', device=device)


def run_tts(text, lang,index):
    start = time.time()
    At_index = f"At index : {index} "
    print(At_index)

    final_text = text
    mel = text_to_mel.generate_mel(final_text)

    before_writing = time.time()

    audio, sr = mel_to_wav.generate_wav(mel)
    write(filename='temp.wav', rate=sr, data=audio) # for saving wav file, if needed
    
    end = time.time()
    # total time taken
    print("---------------------------------------------------------------------------------")
    print("Text - ",text)
    beforeWritingAudio = before_writing-start
    print(f"Execution time of the program before writing audio is : {beforeWritingAudio}")
    afterWritingAudio = end-start
    print(f"Execution time of the program after writing audio is : {afterWritingAudio}")
    data["Index"].append(index)
    data["Text"].append(text)
    data["Before Writing Audio Time"].append(beforeWritingAudio)
    data["After Writing Audio Time"].append(afterWritingAudio)
    print("------------------------------------------------------------------------------------------")
    return (sr, audio)

txts = [
"ପଚାଶ ଦଶକର ଶେଷରେ ତାଙ୍କୁ ପଚାଶତମ ଜନ୍ମଦିନ ପାଳନ କରାଯାଇଥିଲା।",
"ପଚାଶ ଦଶକର ଶେଷରେ ତାଙ୍କୁ ପଚାଶତମ ଜନ୍ମଦିନ ପାଳନ କରାଯାଇଥିଲା।",
"ପଚାଶ ଦଶକର ଶେଷରେ ତାଙ୍କୁ ପଚାଶତମ ଜନ୍ମଦିନ ପାଳନ କରାଯାଇଥିଲା।",
"ପଚାଶ ଦଶକର ଶେଷରେ ତାଙ୍କୁ ପଚାଶତମ ଜନ୍ମଦିନ ପାଳନ କରାଯାଇଥିଲା।",
"ପଚାଶ ଦଶକର ଶେଷରେ ତାଙ୍କୁ ପଚାଶତମ ଜନ୍ମଦିନ ପାଳନ କରାଯାଇଥିଲା।",
"ପଚାଶ କିଲୋମିଟର ଯାତ୍ରା କରିବା ପରେ ସେ ଥକି ଯାଇଥିଲେ।",
"ପଚାଶ କିଲୋମିଟର ଯାତ୍ରା କରିବା ପରେ ସେ ଥକି ଯାଇଥିଲେ।",
"ପଚାଶ କିଲୋମିଟର ଯାତ୍ରା କରିବା ପରେ ସେ ଥକି ଯାଇଥିଲେ।",
"ପଚାଶ କିଲୋମିଟର ଯାତ୍ରା କରିବା ପରେ ସେ ଥକି ଯାଇଥିଲେ।",
"ପଚାଶ କିଲୋମିଟର ଯାତ୍ରା କରିବା ପରେ ସେ ଥକି ଯାଇଥିଲେ।",
"ସେ ପଚାଶ ଦିନରେ ଏକ ନୂତନ କାର୍ଯ୍ୟକ୍ରମ ପ୍ରସ୍ତୁତ କରିଥିଲେ ।",
"ସେ ପଚାଶ ଦିନରେ ଏକ ନୂତନ କାର୍ଯ୍ୟକ୍ରମ ପ୍ରସ୍ତୁତ କରିଥିଲେ |",
"ସେ ପଚାଶ ଦିନରେ ଏକ ନୂତନ କାର୍ଯ୍ୟକ୍ରମ ପ୍ରସ୍ତୁତ କରିଥିଲେ |",
"ସେ ପଚାଶ ଦିନରେ ଏକ ନୂତନ କାର୍ଯ୍ୟକ୍ରମ ପ୍ରସ୍ତୁତ କରିଥିଲେ |",
"ସେ ପଚାଶ ଦିନରେ ଏକ ନୂତନ କାର୍ଯ୍ୟକ୍ରମ ପ୍ରସ୍ତୁତ କରିଥିଲେ |",
"2050 ରେ, ଏହା ବିଶ୍ୱର ଅଗ୍ରଣୀ ଟେକ୍ନୋଲୋଜି ଗନ୍ତବ୍ୟସ୍ଥଳ ହେବ |",
"2050 ରେ, ଏହା ବିଶ୍ୱର ଅଗ୍ରଣୀ ଟେକ୍ନୋଲୋଜି ଗନ୍ତବ୍ୟସ୍ଥଳ ହେବ |",
"2050 ରେ, ଏହା ବିଶ୍ୱର ଅଗ୍ରଣୀ ଟେକ୍ନୋଲୋଜି ଗନ୍ତବ୍ୟସ୍ଥଳ ହେବ |",
"2050 ରେ, ଏହା ବିଶ୍ୱର ଅଗ୍ରଣୀ ଟେକ୍ନୋଲୋଜି ଗନ୍ତବ୍ୟସ୍ଥଳ ହେବ |",
"2050 ରେ, ଏହା ବିଶ୍ୱର ଅଗ୍ରଣୀ ଟେକ୍ନୋଲୋଜି ଗନ୍ତବ୍ୟସ୍ଥଳ ହେବ |",
"ଯେତେବେଳେ ସେ ପଚାଶ ଥର ସ୍କୋର କରିଥିଲେ, ସେ ପ୍ରତିଯୋଗିତାର ବିଜେତା ହୋଇଥିଲେ |",
"ଯେତେବେଳେ ସେ ପଚାଶ ଥର ସ୍କୋର କରିଥିଲେ, ସେ ପ୍ରତିଯୋଗିତାର ବିଜେତା ହୋଇଥିଲେ |",
"ଯେତେବେଳେ ସେ ପଚାଶ ଥର ସ୍କୋର କରିଥିଲେ, ସେ ପ୍ରତିଯୋଗିତାର ବିଜେତା ହୋଇଥିଲେ |",
"ଯେତେବେଳେ ସେ ପଚାଶ ଥର ସ୍କୋର କରିଥିଲେ, ସେ ପ୍ରତିଯୋଗିତାର ବିଜେତା ହୋଇଥିଲେ |",
"ଯେତେବେଳେ ସେ ପଚାଶ ଥର ସ୍କୋର କରିଥିଲେ, ସେ ପ୍ରତିଯୋଗିତାର ବିଜେତା ହୋଇଥିଲେ |",
"ବ୍ୟକ୍ତିଗତ ବିକାଶ ସମୃଦ୍ଧତାକୁ ନେଇଥାଏ, ଏହା ଏକାନ୍ତ ଆବଶ୍ୟକ |",
"ବ୍ୟକ୍ତିଗତ ବିକାଶ ସମୃଦ୍ଧତାକୁ ନେଇଥାଏ, ଏହା ଏକାନ୍ତ ଆବଶ୍ୟକ |",
"ବ୍ୟକ୍ତିଗତ ବିକାଶ ସମୃଦ୍ଧତାକୁ ନେଇଥାଏ, ଏହା ଏକାନ୍ତ ଆବଶ୍ୟକ |",
"ବ୍ୟକ୍ତିଗତ ବିକାଶ ସମୃଦ୍ଧତାକୁ ନେଇଥାଏ, ଏହା ଏକାନ୍ତ ଆବଶ୍ୟକ |",
"ବ୍ୟକ୍ତିଗତ ବିକାଶ ସମୃଦ୍ଧତାକୁ ନେଇଥାଏ, ଏହା ଏକାନ୍ତ ଆବଶ୍ୟକ |",
"ସଫଳତା ଆସେ ଯିଏ ହାରିଯିବା ପରେ ମଧ୍ୟ ହାର ମାନେ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯିଏ ହାରିଯିବା ପରେ ମଧ୍ୟ ହାର ମାନେ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯିଏ ହାରିଯିବା ପରେ ମଧ୍ୟ ହାର ମାନେ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯିଏ ହାରିଯିବା ପରେ ମଧ୍ୟ ହାର ମାନେ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯିଏ ହାରିଯିବା ପରେ ମଧ୍ୟ ହାର ମାନେ ନାହିଁ |",
"ତୁମର ଚିନ୍ତାଧାରା ତୁମ ଜୀବନକୁ ବନାଇପାରେ କିମ୍ବା ଭାଙ୍ଗିପାରେ |",
"ତୁମର ଚିନ୍ତାଧାରା ତୁମ ଜୀବନକୁ ବନାଇପାରେ କିମ୍ବା ଭାଙ୍ଗିପାରେ |",
"ତୁମର ଚିନ୍ତାଧାରା ତୁମ ଜୀବନକୁ ବନାଇପାରେ କିମ୍ବା ଭାଙ୍ଗିପାରେ |",
"ତୁମର ଚିନ୍ତାଧାରା ତୁମ ଜୀବନକୁ ବନାଇପାରେ କିମ୍ବା ଭାଙ୍ଗିପାରେ |",
"ତୁମର ଚିନ୍ତାଧାରା ତୁମ ଜୀବନକୁ ବନାଇପାରେ କିମ୍ବା ଭାଙ୍ଗିପାରେ |",
"ପ୍ରେରଣା ହେଉଛି ସେହି ଜିନିଷ ଯାହା ଆମକୁ ଆମର ଲକ୍ଷ୍ୟ ଆଡକୁ ଗତି କରେ |",
"ପ୍ରେରଣା ହେଉଛି ସେହି ଜିନିଷ ଯାହା ଆମକୁ ଆମର ଲକ୍ଷ୍ୟ ଆଡକୁ ଗତି କରେ |",
"ପ୍ରେରଣା ହେଉଛି ସେହି ଜିନିଷ ଯାହା ଆମକୁ ଆମର ଲକ୍ଷ୍ୟ ଆଡକୁ ଗତି କରେ |",
"ପ୍ରେରଣା ହେଉଛି ସେହି ଜିନିଷ ଯାହା ଆମକୁ ଆମର ଲକ୍ଷ୍ୟ ଆଡକୁ ଗତି କରେ |",
"ପ୍ରେରଣା ହେଉଛି ସେହି ଜିନିଷ ଯାହା ଆମକୁ ଆମର ଲକ୍ଷ୍ୟ ଆଡକୁ ଗତି କରେ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଚାବିକାଠି, କେବେ ହାର ମାନ ନାହିଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଚାବିକାଠି, କେବେ ହାର ମାନ ନାହିଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଚାବିକାଠି, କେବେ ହାର ମାନ ନାହିଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଚାବିକାଠି, କେବେ ହାର ମାନ ନାହିଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଚାବିକାଠି, କେବେ ହାର ମାନ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯେଉଁମାନେ କେବେ ହାର ମାନନ୍ତି ନାହିଁ, ସେମାନଙ୍କର କଠିନ ପରିଶ୍ରମ କେବେ ବିଫଳ ହୁଏ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯେଉଁମାନେ କେବେ ହାର ମାନନ୍ତି ନାହିଁ, ସେମାନଙ୍କର କଠିନ ପରିଶ୍ରମ କେବେ ବିଫଳ ହୁଏ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯେଉଁମାନେ କେବେ ହାର ମାନନ୍ତି ନାହିଁ, ସେମାନଙ୍କର କଠିନ ପରିଶ୍ରମ କେବେ ବିଫଳ ହୁଏ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯେଉଁମାନେ କେବେ ହାର ମାନନ୍ତି ନାହିଁ, ସେମାନଙ୍କର କଠିନ ପରିଶ୍ରମ କେବେ ବିଫଳ ହୁଏ ନାହିଁ |",
"ସଫଳତା ଆସେ ଯେଉଁମାନେ କେବେ ହାର ମାନନ୍ତି ନାହିଁ, ସେମାନଙ୍କର କଠିନ ପରିଶ୍ରମ କେବେ ବିଫଳ ହୁଏ ନାହିଁ |",
"ଯୋଗାଯୋଗ ଏବଂ ସହଯୋଗ ସହଜରେ ସମସ୍ୟାର ସମାଧାନ କରିପାରିବ |",
"ଯୋଗାଯୋଗ ଏବଂ ସହଯୋଗ ସହଜରେ ସମସ୍ୟାର ସମାଧାନ କରିପାରିବ |",
"ଯୋଗାଯୋଗ ଏବଂ ସହଯୋଗ ସହଜରେ ସମସ୍ୟାର ସମାଧାନ କରିପାରିବ |",
"ଯୋଗାଯୋଗ ଏବଂ ସହଯୋଗ ସହଜରେ ସମସ୍ୟାର ସମାଧାନ କରିପାରିବ |",
"ଯୋଗାଯୋଗ ଏବଂ ସହଯୋଗ ସହଜରେ ସମସ୍ୟାର ସମାଧାନ କରିପାରିବ |",
"ଜୀବନକୁ ନିଜ ପଥରେ ବଞ୍ଚାନ୍ତୁ, ପ୍ରତ୍ୟେକ ମୁହୂର୍ତ୍ତକୁ ଉପଭୋଗ କରନ୍ତୁ |",
"ଜୀବନକୁ ନିଜ ପଥରେ ବଞ୍ଚାନ୍ତୁ, ପ୍ରତ୍ୟେକ ମୁହୂର୍ତ୍ତକୁ ଉପଭୋଗ କରନ୍ତୁ |",
"ଜୀବନକୁ ନିଜ ପଥରେ ବଞ୍ଚାନ୍ତୁ, ପ୍ରତ୍ୟେକ ମୁହୂର୍ତ୍ତକୁ ଉପଭୋଗ କରନ୍ତୁ |",
"ଜୀବନକୁ ନିଜ ପଥରେ ବଞ୍ଚାନ୍ତୁ, ପ୍ରତ୍ୟେକ ମୁହୂର୍ତ୍ତକୁ ଉପଭୋଗ କରନ୍ତୁ |",
"ଜୀବନକୁ ନିଜ ପଥରେ ବଞ୍ଚାନ୍ତୁ, ପ୍ରତ୍ୟେକ ମୁହୂର୍ତ୍ତକୁ ଉପଭୋଗ କରନ୍ତୁ |",
"ସଫଳତାର ଉଚ୍ଚତାରେ ପହଞ୍ଚିବା ପାଇଁ ତୁମର ସ୍ୱପ୍ନକୁ ଗୋଡ଼ାନ୍ତୁ ଏବଂ କେବେ ବି ଛାଡନ୍ତୁ ନାହିଁ |",
"ସଫଳତାର ଉଚ୍ଚତାରେ ପହଞ୍ଚିବା ପାଇଁ ତୁମର ସ୍ୱପ୍ନକୁ ଗୋଡ଼ାନ୍ତୁ ଏବଂ କେବେ ବି ଛାଡନ୍ତୁ ନାହିଁ |",
"ସଫଳତାର ଉଚ୍ଚତାରେ ପହଞ୍ଚିବା ପାଇଁ ତୁମର ସ୍ୱପ୍ନକୁ ଗୋଡ଼ାନ୍ତୁ ଏବଂ କେବେ ବି ଛାଡନ୍ତୁ ନାହିଁ |",
"ସଫଳତାର ଉଚ୍ଚତାରେ ପହଞ୍ଚିବା ପାଇଁ ତୁମର ସ୍ୱପ୍ନକୁ ଗୋଡ଼ାନ୍ତୁ ଏବଂ କେବେ ବି ଛାଡନ୍ତୁ ନାହିଁ |",
"ସଫଳତାର ଉଚ୍ଚତାରେ ପହଞ୍ଚିବା ପାଇଁ ତୁମର ସ୍ୱପ୍ନକୁ ଗୋଡ଼ାନ୍ତୁ ଏବଂ କେବେ ବି ଛାଡନ୍ତୁ ନାହିଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଏକ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଅଂଶ, ଏହାକୁ କେବେବି ଛାଡିବା ଉଚିତ୍ ନୁହେଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଏକ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଅଂଶ, ଏହାକୁ କେବେବି ଛାଡିବା ଉଚିତ୍ ନୁହେଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଏକ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଅଂଶ, ଏହାକୁ କେବେବି ଛାଡିବା ଉଚିତ୍ ନୁହେଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଏକ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଅଂଶ, ଏହାକୁ କେବେବି ଛାଡିବା ଉଚିତ୍ ନୁହେଁ |",
"ଆତ୍ମବିଶ୍ୱାସ ସଫଳତାର ଏକ ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ଅଂଶ, ଏହାକୁ କେବେବି ଛାଡିବା ଉଚିତ୍ ନୁହେଁ |"
]

for index,value in enumerate(txts):
  _, audio = run_tts(value, 'or', index)
  # print("-------------Done-------------------")
"""**Output**"""

print("Data writing to 10gb_gpu_odia_output.csv")
# Create a DataFrame from the data dictionary
df = pd.DataFrame(data)

# Write the DataFrame to a CSV file
df.to_csv("10gb_gpu_odia_output.csv", index=False, encoding="utf-8")

print("Data written to 10gb_gpu_odia_output.csv")