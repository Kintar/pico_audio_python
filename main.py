def int_le(b):
    v = 0
    for i in range(len(b)):
        v |= b[i] << (i * 8)
    return v


class WavData:
    bitDepth = 16
    sampleRate = 44100
    data = None
    blocSize = 0

    def load(self, fileObject):
        id = f.read(4)
        f.read(4) # file length, skip it
        dataFormat = f.read(4)
        if id != b'RIFF' or dataFormat != b'WAVE':
            err = f"Not a valid WAV file: {id}, {dataFormat}"
            raise ValueError(err)

        blocId = f.read(4) # data format block specifier
        if blocId != b'fmt ':
            err = f"Invalid format block: {blocId}"
            raise ValueError(err)
        
        blockSize = int_le(f.read(4))
        fmtBlock = f.read(blockSize)
        
        self.dataFmt = int_le(fmtBlock[0:2])
        self.channels = int_le(fmtBlock[2:4])
        self.sampleRate = int_le(fmtBlock[4:8])
        self.bytePerSec = int_le(fmtBlock[8:12])
        
        self.bitDepth = int_le(fmtBlock[14:16])


wavdata = WavData()
with open("hum.wav", "rb") as f:
    wavdata.load(f)

print(f"{wavdata.sampleRate}Hz at {wavdata.bitDepth} bits.")