"""## Inference Code"""

import sys
sys.path.append('vakyansh-tts')


from tts_infer.tts import TextToMel, MelToWav
from tts_infer.transliterate import XlitEngine
from tts_infer.num_to_word_on_sent import normalize_nums

import re
from scipy.io.wavfile import write
device = 'cpu'

text_to_mel = TextToMel(glow_model_dir='vakyansh-tts/tts_infer/translit_models/hindi/glow_ckp', device=device)
mel_to_wav = MelToWav(hifi_model_dir='vakyansh-tts/tts_infer/translit_models/hindi/hifi_ckp', device=device)

def translit(text, lang):
    reg = re.compile(r'[a-zA-Z]')
    engine = XlitEngine(lang)
    words = [engine.translit_word(word, topk=1)[lang][0] if reg.match(word) else word for word in text.split()]
    updated_sent = ' '.join(words)
    return updated_sent

def run_tts(text, lang,index):
    text = text.replace('।', '.') # only for hindi models
    text_num_to_word = normalize_nums(text, lang) # converting numbers to words in lang
    text_num_to_word_and_transliterated = translit(text_num_to_word, lang) # transliterating english words to lang

    mel = text_to_mel.generate_mel(text_num_to_word_and_transliterated)
    audio, sr = mel_to_wav.generate_wav(mel)
    write(filename=f'temp{index}.wav', rate=sr, data=audio) # for saving wav file, if needed
    return (sr, audio)

txts = ["सूरज पहाड़ों के पीछे डूबता है, और पूरे परिदृश्य में एक गर्म नारंगी चमक बिखेरता है","शहर के मध्य में, जीवन ऊर्जा से भर जाता है क्योंकि लोग अपने गंतव्यों की ओर जल्दी जाते हैं","पत्तों के बीच से सरसराती हुई हल्की हवा जंगल में एक सुखद धुन पैदा करती है।","जैसे ही लहरें किनारे से टकराती हैं, सीगल नमकीन हवा में खूबसूरती से उड़ते हैं।","बेकरी से ताज़ी पकी हुई ब्रेड की सुगंध राहगीरों को लुभाती है।","रात के आकाश में तारे टिमटिमाते हैं, जिससे ब्रह्मांड की विशालता का पता चलता है।","अराजकता के बीच, मौन का एक क्षण मन में स्पष्टता लाता है।","किताब के पन्ने धीमी फुसफुसाहट के साथ घूमते हैं और कल्पना की दुनिया को उजागर करते हैं।","बारिश की बूंदें खिड़की के शीशे पर लयबद्ध तरीके से थपकती हैं, जिससे घर के अंदर एक आरामदायक माहौल बन जाता है।","पार्क में बच्चों के खेलने की आवाज़ें गूँजती हैं, जिनमें जवानी का आनंद होता है।"]
for i in range(len(txts)):
  _, audio = run_tts(txts[i], 'hi',i)

"""## Results"""

import IPython.display as ipd
ipd.Audio('temp.wav')