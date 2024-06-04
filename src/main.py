import os
from PIL import Image
import torch
from torchvision import transforms, models
#from torchvision.models.resnet import ResNet18_Weights


import pytest

class imageData:
    def __init__(self, DIR):
        self.dir = DIR

    def LoadImages(self):
        imgs = []
        for file in os.listdir(self.dir):
            if file.endswith('.jpg') or file.endswith('.png'):
                imgs.append(Image.open(os.path.join(self.dir, file)))
        return imgs

def test_imgData_fake():
    loader = imageData("../images/")
    images = loader.LoadImages()
    assert(len(images) == 3)

def test_imgData():
    loader = imageData("../images/")
    images = loader.LoadImages()
    assert(len(images) == 2)


class imgProcess:
    def __init__(self, size):
        self.s = size

    def resize_and_GRAY(self, img_list):
        p_images = []
        for img in img_list:
            t = transforms.Compose([
                transforms.Resize((self.s, self.s)),
                transforms.Grayscale(num_output_channels = 3),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                    0.229, 0.224, 0.225
                ])
            ])
            p_images.append(t(img))
        return p_images



class predictor:
    def __init__(self):
        self.mdl = models.resnet18(weights=ResNet18_Weights.DEFAULT)
        self.mdl.eval()

    def Predict_Img(self, processed_images):
        results = []
        for img_tensor in processed_images:
            pred = self.mdl(img_tensor.unsqueeze(0))
            results.append(torch.argmax(pred, dim= 1).item())
        return results




if __name__ == '__main__':
    loader = imageData('images/')
    images = loader.LoadImages()

    processor = imgProcess(256)
    processed_images = processor.resize_and_GRAY(images)

    pred = predictor()
    results = pred.Predict_Img(processed_images)
    print(results)