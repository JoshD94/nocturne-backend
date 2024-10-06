from openai import OpenAI
from midiutil import MIDIFile
from midi2audio import FluidSynth


api_key = "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"
client = OpenAI(api_key=api_key)


mood = 'sad'
genre = 'classical'


def generate_midi(mood, genre, duration):
    system_prompt = f"Generate a melody in note format \
    that I can convert to a MIDI file. Do not respond with any additional text, \
    only the code. Don't assign the dictionary to a variable, \
    and don't add any additional text. The format should be a list of dictionaries where each dictionary \
    represents a note, with keys: 'note' (MIDI note number), 'start_time' (in beats), \
    'duration' (in beats), and 'velocity' (0-127). The format should start and end with brackets [], and an example output is as shown: \
    [ \
    {{'note': 60, 'start_time': 0.0, 'duration': 0.5, 'velocity': 100}}, \
    {{'note': 62, 'start_time': 0.5, 'duration': 0.5, 'velocity': 100}}, \
    {{'note': 64, 'start_time': 1.0, 'duration': 0.5, 'velocity': 100}}, \
    ] \
    "
    selected_genre = genre[random.randint(0, len(genre))]
    user_prompt = f"Generate me a MIDI song with a mood: {mood}, the \
    genre should {selected_genre}, and the duration of the song should be {duration}."

    name_prompt = f'Generate a one word name for the song, given that \
            the mood is {mood} and the genre are these {selected_genre}. Only output this \
            one word.'

    completion = client.chat.completions.create(
    # gpt-4o-mini or gpt-4o
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": user_prompt
        }
            ]
        )
    
    name = client.chat.completions.create(model="gpt-4o", messages=[
        {"role": "system", "content": "Only output one word based on the user's input"},
        {
            "role": "user",
            "content": name_prompt
        }
            ]
        )
    
    print((completion.choices[0].message.content, name.choices[0].message.content))
    return (completion.choices[0].message.content, name.choices[0].message.content)




def create_midi(midi_format, file_name):
    # Create a new MIDI file with 1 track
    MyMIDI = MIDIFile(1)

    # General parameters for the MIDI file
    track = 0  # Track number
    channel = 0  # MIDI channel (0-15, where 0 is usually the default)
    tempo = 120  # Tempo in BPM (beats per minute)
    MyMIDI.addTempo(track, 0, tempo)  # Add tempo to the track starting at time 0
    
    midi_format = eval(midi_format.strip())

    for note_info in midi_format:
        note = note_info["note"]  # MIDI note number (e.g., 60 for C4)
        start_time = note_info["start_time"]  # Start time in beats
        duration = note_info["duration"]  # Duration in beats
        velocity = note_info["velocity"]  # Velocity (volume/intensity) of the note

        # Add the note to the MIDI file
        MyMIDI.addNote(track, channel, note, start_time, duration, velocity)

    with open(file_name + '.mid', "wb") as output_file:
        MyMIDI.writeFile(output_file)
    
    fs = FluidSynth()
    midi_file = file_name + '.mid'
    wav_file = file_name + '.wav'
    fs.midi_to_audio(midi_file, wav_file)  
    return file_name + '.wav'

    

# generated_midi = generate_midi('sad',['classical'], 10)
# midi_file = create_midi(generated_midi[0], generated_midi[1])

# TODO: make code blocks different
# print()
# print(completion.choices[0].message.content)
# legacy api key: sk-3w1nHSB3v-Qo1YOft0ZjzZ_82GZCrqJWsntXzxTAvPT3BlbkFJPOfvPtYRp-wfC3qAvG1cd6II6vYbdpqfzqwhN_01kA
# project api key: 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
