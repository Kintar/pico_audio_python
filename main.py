def int_le(b: bytes) -> int:
    v = 0
    for i in range(len(b)):
        v |= b[i] << (i * 8)
    return v


class WavData:
    bitDepth = 16
    sampleRate = 44100
    data = None
    blocSize = 0

    def _readBlock(self, fileObject):
        id = f.read(4)
        blockLen = int_le(f.read(4))
        blockData = f.read(blockLen)
        return (id, blockLen, blockData)

    def load(self, fileObject):
        id = f.read(4)
        f.read(4) # file length, skip it
        dataFormat = f.read(4)
        if id != b'RIFF' or dataFormat != b'WAVE':
            err = f"Not a valid WAV file: {id}, {dataFormat}"
            raise ValueError(err)

        (blocId, bLen, data) = self._readBlock(f)
        if blocId != b'fmt ':
            err = f"Invalid format block: {blocId}"
            raise ValueError(err)
        
        self.dataFmt = int_le(data[0:2])
        self.channels = int_le(data[2:4])
        self.sampleRate = int_le(data[4:8])
        self.bytePerSec = int_le(data[8:12])
        
        self.bitDepth = int_le(data[14:16])

        # find the data block
        while True:
            (blocId, _, data) = self._readBlock(f)
            if blocId == b'data':
                self.wavData = data
                break
            
    def convert_depth(self, target):
        if target == self.bitDepth:
            return

        bytesPer = int(self.bitDepth / 8)
        for i in range(0, len(self.wavData), bytesPer):
            v = 0
            for ii in range(bytesPer):
                v |= self.wavData[i+ii] << (ii * 8)
            

wavdata = WavData()
with open("hum.wav", "rb") as f:
    wavdata.load(f)

print(f"{wavdata.sampleRate}Hz at {wavdata.bitDepth} bits. {len(wavdata.wavData)} bytes.")