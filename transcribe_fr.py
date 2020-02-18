import sys, re, time, pyperclip
from espeakng import ESpeakNG
esng = ESpeakNG()
esng.voice = 'fr'


# Handles text formatting options
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


def transcribe(chars):
    '''
    Transcribe each chunk of text to IPA
    Remove redundant IPA characters from transcription
    '''
    # (en) and (fr) appears in output of certain words, such as "weekend"
    redundant_regex = r'[ːˈˌ-]|\(en\)|\(fr\)'
    ipa = esng.g2p(chars, ipa=True)
    ipa = re.sub(redundant_regex, '', ipa)
    return ipa
    
    
def print_transcription(text):
    '''
    Split input text to smaller chunks of text by punctuations
    Transcribe each chunk of text and print final output (punctuations included)
    '''
    punctuations = ',.:;!?«»\/\n'
    split_text = re.split(f'([{punctuations}])', text)

    output = ''
    for chars in split_text:
        if chars not in punctuations:
            chars = transcribe(chars)
            output += chars
        elif chars == '\n':
            output += chars
        elif chars in ':;!?«»\/':
            output += (' ' + chars + ' ')
        else:
            output += (chars + ' ')
    output = f'[{output.strip(". ")}]'
    # Copy transcribed IPA to clipboard
    pyperclip.copy(output)
    # Print transcribed IPA to terminal
    print(output)


text = sys.argv[1]
# Print input text in bold
print(color.BOLD + text + color.END, '\n')
# Print transcription in normal font
print_transcription(text)
# Pause for 1 second
time.sleep(1)
# Read text aloud
try:
    esng.say(text, sync=True)  
except KeyboardInterrupt:
    pass