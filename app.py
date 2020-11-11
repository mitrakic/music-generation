from flask import Flask, render_template, redirect, url_for, flash, session, request
from random import randint
from pydub import AudioSegment
from pydub.playback import play
import random
from PIL import Image
from numpy import asarray
import numpy

app = Flask(__name__)
app.secret_key = 's3cr3t'
app.config.from_object('config')

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            print(file)
            path = "./static/" + file.filename
            file.save(path)
            play_song(path)
    return render_template("home.html")

def load_files():
    
    # load in files and normalize to 4 measures
    bass = (AudioSegment.from_wav("./1/bass.wav") * 2) - 4
    clav = (AudioSegment.from_wav("./1/clav.wav") * 2) - 3
    drums = (AudioSegment.from_wav("./1/drums.wav") * 4) - 3
    flute = AudioSegment.from_wav("./1/flute.wav") - 2
    synth = (AudioSegment.from_wav("./1/synth.wav") * 4)
    #print(len(bass), len(clav), len(drums), len(flute), len(synth))

    clav2 = (AudioSegment.from_wav("./2/clavi.wav") * 2) - 2
    clav3 = AudioSegment.from_wav("./2/clavi2.wav") - 2
    drums2 = (AudioSegment.from_wav("./2/drums.wav") * 2) - 3
    flute2 = AudioSegment.from_wav("./2/flute.wav") - 2
    synth2 = AudioSegment.from_wav("./2/synth.wav") - 1
    synth3 = AudioSegment.from_wav("./2/synth_alt.wav") - 1
    #print(len(clav2), len(clav3), len(drums2), len(flute2), len(synth2), len(synth3))

    #create combinations
    c1 = [bass, clav, drums, flute, synth]
    c2 = [bass, clav2, drums2, flute2, synth2]
    c3 = [bass, clav2, drums2, flute, synth3]
    c4 = [bass, clav3, drums2, flute2, synth2]
    c5 = [bass, clav2, drums, flute, synth3]
    c6 = [bass, clav, drums, flute, synth]
    c7 = [bass, clav2, drums, flute2, synth2]
    c8 = [bass, clav3, drums2, flute, synth3]

    combinations = [c1, c2, c3, c4, c5, c6, c7, c8]
    
    return combinations

def load_speeches(seed1, seed2, seed3):
    folders = ["arbenz", "armas", "paris", "larrykramer", "vox"]
    files = list()
    index = (int(seed1) + int(seed2) + int(seed3)) % 5
    for i in range(1, 6):
        folder = folders[index]
        if folder == "paris":
            files.append(AudioSegment.from_wav("./speeches/" + folders[index] + "/" + str(i) + ".wav")+8)
        elif folder == "vox":
            files.append(AudioSegment.from_wav("./speeches/" + folders[index] + "/" + str(i) + ".wav")+5)
        else:
            files.append(AudioSegment.from_wav("./speeches/" + folders[index] + "/" + str(i) + ".wav")+5)
        #play(files[i-1].reverse())
    return files

def create_song(combinations, speeches, seed1, seed2, seed3):
    random.seed(seed1)
    
    #introduction
    introduction = AudioSegment.silent(duration=0)
    intro_length = random.randint(2, 3)
    print(intro_length)
    last = set()
    current = set()
    for i in range(intro_length):
        combination = combinations[random.randint(0, 7)]
        current = last.copy()
        curr = AudioSegment.silent(duration=9600)
        for e in combination:
            if e not in current:
                if random.random() > (1.2 / (i+2)):
                    current.add(e)
        for e in last:
            if random.random() < seed1 / 500:
                current.remove(e)
        if len(current) == 0:
            current.add(flute)
        last = current.copy()
        for e in current:
            curr = curr.overlay(e, loop=True)
        if random.random() < seed2 / 200:
            curr -= 3
            curr = curr.overlay(speeches[random.randint(0, 4)], loop=False)
            print("speech")
            #play(curr)
        print(i, current)
        introduction += curr
    introduction = introduction.fade_in(len(introduction))
    #play(introduction)
    
    #middle
    random.seed(seed2)
    middle = AudioSegment.silent(duration=0)
    middle_num_sections = random.randint(5, 8)
    print("Num sections: ", middle_num_sections)
    for i in range(middle_num_sections):
        combination = combinations[random.randint(0, 7)]
        section_length = random.randint(1, 4)
        print("Section: ", i, "Length: ", section_length)
        section = AudioSegment.silent(duration=0)
        for j in range(section_length):
            prev_length = len(current)
            current = set()
            curr = AudioSegment.silent(duration=9600)
            for e in combination:
                eee = e
                if random.random() < seed2 / 500:
                    eee = eee.pan((random.random()*2)-1)
                if random.random() < seed3 / 550:
                    eee = eee.reverse()
                if random.random() > (1.2 / (prev_length+1)):
                    current.add(eee)
            if len(current) == 0:
                current.add(synth2)
            for e in current:
                curr = curr.overlay(e, loop=True)
            if random.random() < seed3 / 350:
                curr -= 5
                curr = curr.overlay(speeches[random.randint(0, 4)], loop=False)
                print("speech")
            elif random.random() < seed3 / 550:
                curr -= 5
                curr = curr.overlay(speeches[random.randint(0, 4)].reverse(), loop=False)
                print("speech reversed")
            print("Section: ", i, "Segment: ", j, "Inst: ", len(current))
            section += curr
        middle += section
    #play(middle)
    
    #outro
    outro = AudioSegment.silent(duration=0)
    outro_length = random.randint(1, 3)
    print(outro_length)
    current = set()
    for i in range(outro_length):
        current = last.copy()
        curr = AudioSegment.silent(duration=9600)
        for e in combinations[0]:
            if e not in current:
                if random.random() > (1.2 / (i+2)):
                    current.add(e)
        for e in last:
            if random.random() < seed1 / 500:
                current.remove(e)
        if len(current) == 0:
            current.add(flute2)
        last = current.copy()
        for e in current:
            curr = curr.overlay(e, loop=True)
        if random.random() < seed1 / 175:
            curr -= 3
            curr = curr.overlay(speeches[random.randint(0, 4)], loop=False)
            print("speech")
        print(i, current)
        outro += curr
    outro = outro.fade_out(len(outro))
    
    return introduction + middle + outro

def play_song(image):
    image = Image.open(image)
    data = numpy.mean(asarray(image), axis=(0,1))
    print(data)
    song = create_song(load_files(), load_speeches(data[0], data[1], data[2]), data[0], data[1], data[2])
    play(song)


if __name__ == '__main__':
    app.run(port=5000)

