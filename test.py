import numpy as np
from label_colors import colorMap
from PIL import Image
from spade.model import Pix2PixModel
from spade.dataset import get_transform
from torchvision.transforms import ToPILImage

'''colors = np.array([[56, 79, 131], [239, 239, 239],
                   [93, 110, 50], [183, 210, 78],
                   [60, 59, 75], [250, 250, 250]])'''
colors = [key['color'] for key in colorMap]
id_list = [key['id'] for key in colorMap]


def semantic(img):
    print("semantic", type(img))
    h, w = img.size
    imrgb = img.convert("RGB")
    pix = list(imrgb.getdata())
    mask = [id_list[colors.index(i)] if i in colors else 156 for i in pix]
    return np.array(mask).reshape(h, w)


def evaluate(labelmap):
    opt = {
        'label_nc': 182,  # num classes in coco model
        'crop_size': 512,
        'load_size': 512,
        'aspect_ratio': 1.0,
        'isTrain': False,
        'checkpoints_dir': 'app',
        'which_epoch': 'latest',
        'use_gpu': False
    }
    model = Pix2PixModel(opt)
    model.eval()
    image = Image.fromarray(np.array(labelmap).astype(np.uint8))
    transform_label = get_transform(opt, method=Image.NEAREST, normalize=False)
    # transforms.ToTensor in transform_label rescales image from [0,255] to [0.0,1.0]
    # lets rescale it back to [0,255] to match our label ids
    label_tensor = transform_label(image) * 255.0
    label_tensor[label_tensor == 255] = opt['label_nc']  # 'unknown' is opt.label_nc
    print("label_tensor:", label_tensor.shape)

    # not using encoder, so creating a blank image...
    transform_image = get_transform(opt)
    image_tensor = transform_image(Image.new('RGB', (500, 500)))

    data = {
        'label': label_tensor.unsqueeze(0),
        'instance': label_tensor.unsqueeze(0),
        'image': image_tensor.unsqueeze(0)
    }
    generated = model(data, mode='inference')
    print("generated_image:", generated.shape)

    return generated


def to_image(generated):
    to_img = ToPILImage()
    normalized_img = ((generated.reshape([3, 512, 512]) + 1) / 2.0) * 255.0
    return to_img(normalized_img.byte().cpu())
