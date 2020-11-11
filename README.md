# music-generation

This repo contains code that automatically arranges audio tracks. The audio tracks are in folders 1 and 2. Additionally, the songs are mixed with excerpts from important speeches and interviews, contained in the speeches folder. 

Music.ipynb is a Jupyter notebook that allows the user to specify how to arrange the tracks. In the current implementation, the user inputs a photo, and RGB values from this photo are used as the parameters by which the tracks are arranged. 

The programs divides the song into an intro, middle, and outro. The length of each of these, as well as the combination of instruments within each section are determined by the photo input. Effects such as reversal and panning are also configured. Finally, the program overlays excerpts from a certain speech based on the input. 

Users can change the input, tweak the parameters used to make the track, add new parameters to configure additional features, and update the code to use different inputs. app.py, config, and the templates folder represent a Flask App that does the same thing as the Jupyter notebook. To use the app, ensure you have python3 and flask installed, and run "python app.py" from the command line. 

The program also requires that the following python libraries are installed:

pydub
numpy
ffmpeg
simpleaudio
pillow
