# Parámetros generales 

CHUNK = 2
# FORMAT = pyaudio.paInt16
FORMAT = pyaudio.paInt16                # tipo de codificacion
CHANNELS = 2                            # cantidad de canales
RATE = 44100                            # frecuencia de muentreo 
RECORD_SECONDS = 10                     # tiempo de grabacion, se ajusta segun los requerimientos 
WAVE_OUTPUT_FILENAME = "measurements"   # Nombre por default que los archivos grabados .wav tendran

TIME_FREE = 600 # 10 MINUTOS FREE TO RECORD
SPEED_40 = 20  # cm/s 

MODE_SCAN = 'scan'
MODE_LISEN ='lisen'