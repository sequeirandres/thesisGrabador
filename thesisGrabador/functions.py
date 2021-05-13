
# functions for files proccess

# Delete Files 
def deleteFiles(directoryPath):
    for the_file in os.listdir(directoryPath):
        file_path = os.path.join(directoryPath, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #Elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

# Save Files 
def saveFile(frames, NameFile , Sample_size):
    wf = wave.open(NameFile,'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(Sample_size)
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    print('Save File [' ,NameFile ,'] Done!' )
