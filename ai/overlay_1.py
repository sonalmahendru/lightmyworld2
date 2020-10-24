import argparse

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import cv2
from scipy import ndimage

from torchvision import models
import torch
import torchvision.transforms as T

def overlay_transparent(background, overlay, x, y):

    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype = overlay.dtype) * 255
            ],
            axis = 2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y:y+h, x:x+w] = (1.0 - mask) * background[y:y+h, x:x+w] + mask * overlay_image

    return background

def extract_x_y(x1, y1, x2, y2, xc, yc):
    
    all_x = np.linspace(x1, x2, int((x2-x1)/xc))
    all_y = np.linspace(y1, y2, int((y2-11)/yc))

    all_x_y = []
    for j in all_y:
        x_1 = int(all_x[0])
        x_ = int(all_x[-1])
        y_ = int(j)
        all_x_y.append((x_,y_))
        all_x_y.append((x_1,y_))

    for j in all_x:
        x_ = int(j)
        y_1 = int(all_y[0])
        y_ = int(all_y[-1])

        all_x_y.append((x_,y_))
        all_x_y.append((x_,y_1))

    return list(set(all_x_y))

def main(args):
    dlab = models.segmentation.deeplabv3_resnet101(pretrained=1)
    
    img = Image.open(args.image_path).convert('RGB')
    
    trf = T.Compose([T.ToTensor(), 
                    T.Normalize(mean = [0.485, 0.456, 0.406], 
                                std = [0.229, 0.224, 0.225])])

    inp = trf(img).unsqueeze(0)
    
    with torch.no_grad():
        dlab.eval()
        out = dlab(inp)['out']
        om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
    
    om_01 = np.zeros_like(om).astype(np.uint8)
    om_01[om==20] = 1

    ind = np.nonzero(om_01.any(axis=0))[0]
 
    x1, x2 = ind[0], ind[-1]

    ind = np.nonzero(om_01.any(axis=1))[0]
    y1, y2 = ind[0], ind[-1]

    if args.save_bb0x:
        bbox_1 = cv2.rectangle(np.asarray(img).copy(), (x1, y1), (x2, y2), (255,0,0), 2)
        cv2.imwrite(bbox_1, args.bbox_path)
    
    s_img = cv2.imread(args.overlay_image_path, -1)
    s_img = cv2.resize(s_img, (0,0), fx=0.1, fy=0.1)
    
    xc = s_img.shape[0]
    yc = s_img.shape[1]
    
    all_x_y = extract_x_y(x1, y1, x2, y2, xc, yc)
    
    l_img = np.asarray(img).copy()
    
    for i in all_x_y:
        x = i[0]
        y = i[1]
        l_img = overlay_transparent(l_img, s_img, max(0, x-int(xc/2)), max(0, y-int(yc/2)))
        
    if args.save_final_image:
        cv2.imwrite(args.final_path, l_img)
     
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_path', type=str, default=None,
                        help='path of image to test')
    parser.add_argument('--overlay_image_path', type=str, default=None,
                        help='path of overlay image')
    parser.add_argument('--save_bb0x', type=bool, default=False,
                        help='Want to save the bbox')
    parser.add_argument('--bbox_path', type=str, default=None,
                        help='path of bbox image')
    parser.add_argument('--save_final_image', type=bool, default=True,
                        help='Want to save the final image')
    parser.add_argument('--final_path', type=str, default=None,
                        help='path of final image')
    args = parser.parse_args()
    print(args)
    main(args)
