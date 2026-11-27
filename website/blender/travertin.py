"""Eigene Travertin-Textur (kachelbar, 1024): beiger Grund, waagrechte Adern, feine Poren. Aufruf: python3 travertin.py"""
import numpy as np, os
from PIL import Image
rng = np.random.default_rng(3); N = 1024
def rauschen(sx, sy, oktaven=5):
    out = np.zeros((N, N), np.float32); amp = 1.0
    for o in range(oktaven):
        fx, fy = sx * 2 ** o, sy * 2 ** o
        g = rng.standard_normal((fy, fx)).astype(np.float32)
        b = np.array(Image.fromarray(g).resize((N, N), Image.BICUBIC)) if False else None
        # kachelbar: Fourier-Interpolation über ein periodisches Gitter
        F = np.zeros((N, N), np.complex64); k = np.fft.fft2(g)
        F[:fy // 2, :fx // 2] = k[:fy // 2, :fx // 2]; F[-(fy // 2):, :fx // 2] = k[-(fy // 2):, :fx // 2]
        F[:fy // 2, -(fx // 2):] = k[:fy // 2, -(fx // 2):]; F[-(fy // 2):, -(fx // 2):] = k[-(fy // 2):, -(fx // 2):]
        r = np.real(np.fft.ifft2(F)); r /= r.std() + 1e-6
        out += r * amp; amp *= 0.55
    return out / out.std()
adern = rauschen(2, 24)            # stark gestreckt: waagrechte Schichten
wolke = rauschen(4, 4)
schicht = np.sin(adern * 2.2) * 0.5 + 0.5
hell = 0.9 + 0.025 * wolke - 0.05 * schicht ** 3
poren = rng.random((N, N)) < 0.0035
poren = np.array(Image.fromarray((poren * 255).astype(np.uint8)).resize((N, N)).filter(__import__('PIL.ImageFilter', fromlist=['x']).GaussianBlur(1.2))) / 255.0
hell -= poren * 0.22
basis = np.array([232, 220, 200], np.float32) / 255
farbe = np.clip(hell[..., None] * basis * np.array([1.0, 1.0, 0.97]), 0, 1)
Image.fromarray((farbe * 255).astype(np.uint8)).save(os.path.join(os.path.dirname(__file__), 'assets', 'texturen', 'travertin', 'diff.jpg'), quality=92)
print('travertin ok')
