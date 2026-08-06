import cv2 # OpenCV for image processing
import numpy as np # NumPy for array manipulation
from pathlib import Path # For handling file paths in a cross-platform way


class TryOnEngine:
    def __init__(self):
        self.clothes_folder = Path(__file__).parent.parent / 'frontend' / 'static' / 'shirts'

        self.cloth_defs = {
            'tshirt1': {
                'label': 'Red T-Shirt',
                'filename': 'tshirt1.png',
                'scale': 2.2,
                'y_offset': 0.22   
            },
            'white': {
                'label': 'White T-Shirt',
                'filename': 'white.png',
                'scale': 2.2,
                'y_offset': 0.08
            },
            'black': {
                'label': 'Black T-Shirt',
                'filename': 'black.png',
                'scale': 2.2,
                'y_offset': 0.08
            },
            'kurti1': {
                'label': 'Green Kurti',
                'filename': 'kurti1.png',
                'scale': 2.0,
                'y_offset': 0.12
            },
            'kurti2': {
                'label': 'Yellow Kurti',
                'filename': 'kurti2.png',
                'scale': 2.0,
                'y_offset': 0.12
            },
            'kurti3': {
                'label': 'Cream Kurti',
                'filename': 'kurti3.png',
                'scale': 2.0,
                'y_offset': 0.12
            }
        }

        self.images = self._load_clothes()

    def _load_clothes(self):
        images = {}

        for key, info in self.cloth_defs.items():
            path = self.clothes_folder / info['filename']
            image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)

            if image is None:
                print(f"Missing image: {path}")
                continue

            if image.shape[2] == 3:
                alpha = np.ones(
                    (image.shape[0], image.shape[1], 1),
                    dtype=np.uint8
                ) * 255
                image = np.concatenate([image, alpha], axis=2)

            images[key] = image

        return images

    def list_clothes(self):
        return [
            {
                'id': key,
                'label': info['label'],
                'filename': info['filename']
            }
            for key, info in self.cloth_defs.items()
            if key in self.images
        ]

    def apply_tryon(self, frame, cloth_key, pose):
        if cloth_key not in self.images:
            return frame

        required = [
            'left_shoulder',
            'right_shoulder',
            'left_hip',
            'right_hip'
        ]

        if not all(k in pose for k in required):
            return frame

        cloth = self.images[cloth_key].copy()
        config = self.cloth_defs[cloth_key]

        left_shoulder = np.array(pose['left_shoulder'], dtype=np.float32)
        right_shoulder = np.array(pose['right_shoulder'], dtype=np.float32)

        shoulder_center = ((left_shoulder + right_shoulder) / 2).astype(int)
        shoulder_dist = np.linalg.norm(right_shoulder - left_shoulder)

        cloth_h, cloth_w = cloth.shape[:2]

        target_w = int(shoulder_dist * config['scale'])
        aspect_ratio = cloth_h / cloth_w
        target_h = int(target_w * aspect_ratio)

        resized = cv2.resize(
            cloth,
            (target_w, target_h),
            interpolation=cv2.INTER_AREA
        )

        x = int(shoulder_center[0] - target_w / 2)
        y = int(shoulder_center[1] - target_h * config['y_offset'])

        return self._blend(frame, resized, x, y)

    def _blend(self, bg, ov, x, y):
        if ov.shape[2] < 4:
            return bg

        h, w = ov.shape[:2]
        bg_h, bg_w = bg.shape[:2]

        if x >= bg_w or y >= bg_h or x + w <= 0 or y + h <= 0:
            return bg

        x1 = max(x, 0)
        y1 = max(y, 0)
        x2 = min(x + w, bg_w)
        y2 = min(y + h, bg_h)

        ov_x1 = x1 - x
        ov_y1 = y1 - y
        ov_x2 = ov_x1 + (x2 - x1)
        ov_y2 = ov_y1 + (y2 - y1)

        alpha = ov[ov_y1:ov_y2, ov_x1:ov_x2, 3] / 255.0
        rgb = ov[ov_y1:ov_y2, ov_x1:ov_x2, :3]

        region = bg[y1:y2, x1:x2]

        for c in range(3):
            region[:, :, c] = (
                region[:, :, c] * (1 - alpha)
                + rgb[:, :, c] * alpha
            )

        bg[y1:y2, x1:x2] = region

        return bg