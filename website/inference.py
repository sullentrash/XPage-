from PIL import Image
import torch
import torch.nn as nn
from torchvision import transforms, models

def infer(path_to_model, path_to_image):
  model = models.vit_b_32()
  model.heads = nn.Sequential(nn.Linear(768,256),
                              nn.ReLU(),
                              nn.Dropout(p=0.5),
                              nn.Linear(256,2),
                              nn.LogSoftmax(dim=1))
  model.load_state_dict(torch.load(path_to_model))
  model.eval()
  transform = transforms.Compose([
                  transforms.Resize(224),
                  transforms.CenterCrop(224),
                  transforms.ToTensor(),
                  transforms.Normalize([0.485,0.456,0.406],
                                        [0.229,0.224,0.225])
  ])
  dict_labels = {0:'cat', 1:'dog'}
  inv_normalize = transforms.Normalize(mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
                                      std=[1/0.229, 1/0.224, 1/0.225])
  im = Image.open(path_to_image)
  im = transform(im)
  preds = model(im.reshape(1, 3, 224, 224))
  predicted = torch.max(preds.data,1)[1]
  label = dict_labels[predicted.item()]
  im = inv_normalize(im).permute(1, 2, 0)
  return im, label