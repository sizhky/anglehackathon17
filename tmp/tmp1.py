import sys
sys.path.insert(0, '/home/angle/hackathon/captioner')

import imagecaptioner_small

print(imagecaptioner_small.get_captions('/home/angle/hackathon/query/img.jpg'))
