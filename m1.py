import numpy as np
import pyaudio
from numpy.polynomial import Polynomial
from scipy.signal import bilinear, lfilter
import time

CHUNKS = [4096, 9600]
CHUNK = CHUNKS[1]
FORMAT = pyaudio.paInt16
CHANNEL = 1
RATES = [44100, 48000]
RATE = RATES[1]


def A_weighting(fs: float) -> tuple[np.ndarray, np.ndarray]:
    f1 = 20.598997
    f2 = 107.65265
    f3 = 737.86223
    f4 = 12194.217
    a1000 = 1.9997

    nums = Polynomial(((2*np.pi * f4)**2 * 10**(a1000 / 20), 0,0,0,0))
    dens = (
        Polynomial((1, 4*np.pi * f4, (2*np.pi * f4)**2)) *
        Polynomial((1, 4*np.pi * f1, (2*np.pi * f1)**2)) *
        Polynomial((1, 2*np.pi * f3)) *
        Polynomial((1, 2*np.pi * f2))
    )
    return bilinear(nums.coef, dens.coef, fs)


def rms_flat(a: np.ndarray) -> float:
    return np.sqrt(a.dot(a) / len(a))


class Meter:
    def __init__(self) -> None:
        self.pa = pyaudio.PyAudio()
        self.stream = self.pa.open(
            format=FORMAT,
            channels=CHANNEL,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )
        self.numerator, self.denominator = A_weighting(RATE)
        self.max_decibel = 0

    def __enter__(self) -> 'Meter':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()

    def listen(self: int) -> float:
        block = self.stream.read(CHUNK)
        decoded_block = np.frombuffer(block, dtype=np.int16)
        y = lfilter(self.numerator, self.denominator, decoded_block)
        new_decibel = 20*np.log10(rms_flat(y))
        self.max_decibel = max(self.max_decibel, new_decibel)
        return new_decibel

    def run(self) -> None:
        t_end = time.time() + 10
        while time.time() < t_end:
            new_decibel = self.listen()
            self.update(new_decibel)
            
    def update(self, new_decibel: float) -> None:
        print("Decibels:",new_decibel)


def main() -> None:
    meter = Meter()
    meter.run()
    print("Max Decibels: ", meter.max_decibel)


if __name__ == '__main__':
    main()