import torch
from RealESRGAN import RealESRGAN


class SRGAN():
    def __init__(self, scale: int = 2):
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.scale = scale  #@param ["2", "4", "8"] {allow-input: false}
        self._model = RealESRGAN(device, scale=scale)
        self._model.load_weights(f'weights/RealESRGAN_x{str(self.scale)}.pth', download=True)

    def __call__(self, image):
        return self._model.predict(image)
