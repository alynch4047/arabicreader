# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main3.ui'
#
# Created: Fri Sep 10 12:09:46 2004
#      by: The PyQt User Interface Compiler (pyuic) 3.11
#
# WARNING! All changes made in this file will be lost!


from qt import *

# Import our custom widget.
from lineeditdrag import *
from lineeditarabic import *

image0_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x10\x00\x00\x00\x10" \
  "\x08\x06\x00\x00\x00\x1f\xf3\xff\x61\x00\x00\x02" \
  "\xea\x49\x44\x41\x54\x78\x9c\x25\xd0\x5b\x6e\x1b" \
  "\x55\x1c\x80\xf1\xef\x9c\x39\x73\x73\x1c\x27\x76" \
  "\x62\x27\xa1\x85\xb4\x06\x0a\x2a\x42\x42\x05\x09" \
  "\xc4\x06\x78\x65\x05\xac\x83\x1d\xb0\x10\xf6\x80" \
  "\xfa\x52\x89\x05\x94\x08\x50\x53\x51\x85\xe0\xd8" \
  "\x69\x2e\xb6\x13\x5f\xe7\xe2\x99\x39\x73\xfe\x3c" \
  "\x64\x07\xdf\xf7\x53\xc3\x51\x21\x49\xe2\xc8\x73" \
  "\x47\x18\x29\xaa\x4a\xd8\x6c\x84\xad\x2d\x4d\x23" \
  "\xd6\xd4\xb5\x90\xa6\x0e\x00\xcf\x83\x28\xd2\x58" \
  "\x2b\x74\x3a\x86\x8b\xc1\x6b\xa5\x06\xc3\x42\x6a" \
  "\x2b\xac\xd6\x35\x55\x29\x38\x81\x46\xac\x31\xbe" \
  "\xc2\x37\x8a\xc5\xc2\x52\x56\x33\xd2\xc5\xaf\x54" \
  "\x55\xc9\x4e\xfb\x07\x82\xf8\x4b\x8e\x0e\x02\x82" \
  "\x40\x61\x5c\x2d\x28\x05\x5a\x2b\xc2\x48\xe1\x69" \
  "\xa8\x6b\x28\x0b\x47\x14\x7a\x20\x0b\xe6\xb7\x3f" \
  "\xd3\x6e\xfd\x4e\x66\x1b\x8c\xaf\xfe\xa0\xf7\xe8" \
  "\x17\xb4\xf7\x19\x49\xe6\xd0\xe3\xdb\x13\x25\x02" \
  "\x69\x5a\xe3\x69\xc8\x32\x87\x20\x68\x4f\x51\x3b" \
  "\xc8\xb3\x53\x1a\xe1\x6b\xda\xad\x35\x9d\xdd\x3b" \
  "\xda\xad\x37\xac\x97\xbf\xe1\x44\x88\x42\x8d\xee" \
  "\xf6\x5e\x48\x55\x09\xbe\xaf\xa8\xec\x43\x0d\x80" \
  "\x73\x82\xad\x84\xa8\xf1\x09\x79\xf1\x8c\xa2\xf4" \
  "\xd1\x1a\x9c\x84\xf8\xc6\x43\x23\x58\x2b\x98\xf9" \
  "\xdc\x22\xc0\x62\x59\x13\x85\x8a\x28\xd2\xac\xd6" \
  "\x0e\xad\x20\xd3\x0e\xe8\xa2\xc3\x9f\xf8\x77\x98" \
  "\xe0\x79\x42\x14\x7f\x4b\xf7\xe0\x47\x9c\x28\x44" \
  "\x40\x9d\xfc\x99\x4a\x55\x09\x79\xee\xa8\x6b\xb0" \
  "\xf6\x01\xd2\x78\xe0\x6a\xc1\x0f\x34\x4a\x59\x44" \
  "\x12\x02\x5f\xa3\xd4\x16\xf9\x46\xb3\xb7\x67\x08" \
  "\x03\x85\xc9\x33\xc7\x7c\x9e\x82\x32\xec\xee\x86" \
  "\xd4\xb5\x80\x13\x8a\xa2\xa6\x11\x1b\xb2\xcc\xe2" \
  "\x1b\x45\x10\xee\xe2\x04\xc4\x41\x10\x3c\x7c\x2e" \
  "\x96\x35\xba\xd9\x14\xe6\xb3\x25\xb3\xbb\x15\xef" \
  "\xde\x4d\xd1\x5a\x10\xa9\x79\x3f\xba\x67\x53\x38" \
  "\xf2\xdc\x32\x19\x2f\xa8\x6b\xcb\x7f\xe7\x53\x6a" \
  "\x2b\x8c\x6f\x97\x28\x14\x3b\x3b\x1e\xc6\x56\x25" \
  "\x9f\x3e\xeb\xf1\xf6\x74\x42\x23\xf6\x38\x3f\x1b" \
  "\x13\x46\x01\xab\xd5\x86\xd5\x2a\x63\xb5\xc8\x08" \
  "\x43\xc3\xf8\x66\x4d\x96\x56\x8c\x86\xf7\x4c\x26" \
  "\x2b\xf6\xf7\x63\xd6\x49\x85\xb9\xb9\x5e\x32\x9b" \
  "\x57\x58\x5b\xa3\x94\xc1\xda\x9a\x6e\x2b\xa4\x2a" \
  "\x2a\xd6\xcb\x14\x63\x14\x83\xf3\x1b\xbe\xfb\xfe" \
  "\x98\x46\x23\x26\x8e\x0d\x87\x87\x7b\x0c\x07\x63" \
  "\xbe\x7a\xf1\x01\x46\x7b\x8a\xe9\x64\xc5\xd7\xdf" \
  "\x3c\x21\x49\x72\xca\x12\x4e\x5e\x0f\xf8\xfc\xf9" \
  "\x21\x69\x52\x61\x3c\x8f\x6e\x6f\x9b\x8b\xc1\x3d" \
  "\x7f\xff\x75\xcd\xde\x7e\x4c\x10\x78\x1c\x1d\xb5" \
  "\x98\x8c\x57\x98\x64\x5d\xd2\x6c\x86\x9c\xbe\xb9" \
  "\x26\x8e\x23\x9c\x68\xfa\x1f\xf7\x68\x6e\x35\xf0" \
  "\x74\x41\xb1\xd9\xd0\x6a\x85\x3c\xed\xb7\xe8\x74" \
  "\x42\x82\xd0\x67\x76\x9f\x11\x46\x86\xb2\x74\x98" \
  "\xb2\x7a\x10\x4f\x53\x8b\xe7\x79\x5c\x0c\x17\xf4" \
  "\xfb\x5d\x96\xcb\x94\x64\xbd\x41\x04\xf2\x3c\xc3" \
  "\xb9\x92\xb3\xb3\x7b\x6c\xe5\x78\xfe\x45\x8f\xab" \
  "\xcb\x05\xc7\xc7\x1f\xa1\x5e\xbe\x1c\xca\xe3\x0f" \
  "\x3b\x64\x69\xc1\xe5\xe5\x9a\xe5\xb2\xa6\x77\xd0" \
  "\xe4\x9f\xb7\xb7\x6c\x35\x43\x6c\x55\xf0\xe8\xf1" \
  "\x36\x77\xd3\x84\x27\x4f\xdb\x68\xad\xb9\x1c\xcd" \
  "\x30\xbe\x8f\x6f\x14\xea\xd5\xab\xf7\x32\x9f\x67" \
  "\x04\x81\xe6\xf0\xa8\x8b\xd6\x1e\xf3\x59\x82\xe7" \
  "\x07\xb4\xb6\x03\x04\xc7\xf5\xd5\x9c\xd6\xb6\x61" \
  "\x3a\x4d\xe9\xf5\x9a\x74\x3a\x31\xa3\xd1\x8a\x7e" \
  "\xbf\xcd\xff\x94\x85\x98\xd5\xa1\xf8\x01\xc3\x00" \
  "\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
image2_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
  "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
  "\x7f\x49\x44\x41\x54\x78\x9c\xed\x95\x51\x0a\x00" \
  "\x21\x08\x44\x75\xd9\xdb\x04\x1e\xc0\xe8\xfa\x5e" \
  "\xcb\xfd\xda\x85\x2d\x4b\x11\xfa\x6b\x20\x28\xa3" \
  "\x57\x0c\x53\xa1\x88\xc0\x0e\xdd\x7d\x81\x99\x35" \
  "\xb2\x50\x44\x70\x35\x7f\x59\x45\x55\x9d\x36\x00" \
  "\x00\x22\x72\x0f\x60\x82\x3d\x11\x91\x0b\x1f\xac" \
  "\x88\xa8\x94\xf2\xf5\x99\x59\x2d\x5b\x52\xe0\x5a" \
  "\xeb\x6f\x6c\xc1\x53\xe0\xd6\xda\x50\xeb\xe1\x29" \
  "\x30\xe2\x32\x10\x39\xf0\x9b\x0c\x6f\xb3\x54\x2a" \
  "\x22\x3a\xe0\x03\x3e\xe0\x85\xcc\x2b\x1d\x79\x0b" \
  "\x3c\xe1\xae\x3f\x6f\x9b\x15\x0f\x6d\x54\x33\xaf" \
  "\x8c\x7f\xa5\x08\x00\x00\x00\x00\x49\x45\x4e\x44" \
  "\xae\x42\x60\x82"
image3_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
  "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
  "\xae\x49\x44\x41\x54\x78\x9c\xb5\x94\x51\x0e\xc3" \
  "\x20\x0c\x43\x6d\xb4\x53\x71\xb6\x69\x1f\xd3\xce" \
  "\xe6\x6b\xb1\x8f\x51\x35\xa2\x19\x23\x5a\xf0\x4f" \
  "\x44\x2b\x5e\x2c\x03\xa1\x24\xec\x50\xd9\x42\xdd" \
  "\x09\xbe\x45\x37\xd4\x5a\x9b\x5d\x4b\xe2\xf8\x5f" \
  "\x12\x43\xe0\x63\x93\xd7\x48\x12\x6d\x53\x66\x1d" \
  "\x9e\x85\x4a\x62\x4a\xc6\x63\x3c\x40\xcf\xf8\x57" \
  "\x6e\x51\x28\x00\x10\x40\x6b\x0d\x00\xda\xb1\x04" \
  "\xb9\xc6\x9d\x19\xe8\x87\x77\x42\x01\xf6\x4e\xbc" \
  "\x7c\x8f\x34\x2f\xc6\x78\xb0\xce\x55\x3c\xc7\x6b" \
  "\x75\x2e\x37\xe3\x68\xd6\x9e\xdc\x8c\x2d\xf4\xf5" \
  "\x8c\x01\xef\x8f\x4f\x75\x33\xfe\x17\x6a\x1e\x48" \
  "\x2e\xf4\xe2\x38\x0b\x6a\xc0\xb9\xd0\xd3\x6a\x57" \
  "\x16\x14\x30\x83\x3e\x13\x0a\xac\xde\xf6\x2f\x9a" \
  "\xcd\x8a\xb4\x79\x3c\xea\x0d\x05\x19\x70\xcd\x5b" \
  "\x32\xcc\x0a\x00\x00\x00\x00\x49\x45\x4e\x44\xae" \
  "\x42\x60\x82"
image4_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x12\x00\x00\x00\x12" \
  "\x08\x06\x00\x00\x00\x56\xce\x8e\x57\x00\x00\x01" \
  "\xd0\x49\x44\x41\x54\x78\x9c\xad\x93\x31\x8b\x13" \
  "\x41\x14\xc7\x7f\xbb\x0a\xd7\x05\x6c\x6c\x32\x07" \
  "\x29\x4e\x02\x87\x20\xa4\x09\x1e\x88\x8b\x58\xc8" \
  "\x29\xb9\xb3\xd6\x3e\xb5\x22\x84\xec\x17\xc8\x37" \
  "\x49\xa9\x55\x3a\x51\xc4\x6f\x90\xa0\x55\x84\xd3" \
  "\xec\x59\x44\x39\xb9\xc5\x9d\x24\xe7\xce\x7b\x16" \
  "\x97\x09\x31\x1b\x13\x0b\xff\xf0\xd8\xb7\xf3\xe6" \
  "\xfd\xe7\xb7\xb3\xbc\xa0\x16\xdc\x06\xe0\xe8\xe4" \
  "\xf3\x8e\xa2\x04\x84\xa4\x08\x01\x21\x8a\x30\xae" \
  "\x1c\xce\x3e\x31\xe4\xe9\xc9\x70\x47\x10\x42\x42" \
  "\xce\x11\x42\xae\x20\x08\xdf\x2a\x4f\x66\x21\x10" \
  "\x78\xa3\x71\x79\xa4\x00\x7b\x7b\x7b\x6c\xd2\x70" \
  "\x38\x04\xe0\x34\x39\xdd\x05\xd2\x67\xc1\x8b\x34" \
  "\xf4\x45\x63\x8c\x76\x3a\x1d\x8d\xa2\x48\x55\x55" \
  "\x5d\x7e\xa1\xf9\xcc\xea\x2f\x9b\xea\xc5\xcf\x33" \
  "\x9d\x9d\x8f\x75\x7a\xf6\x55\x27\xdf\xbf\x68\x14" \
  "\x45\xda\x6a\xb5\xd4\x18\xa3\xc0\x3e\x50\x02\xb8" \
  "\xba\x7a\xa2\x8a\xe3\xe5\xdb\xd7\xbc\x19\xff\xf8" \
  "\x63\xfd\xde\xf5\x6b\x3c\xbc\xb5\x0f\x40\x9e\xe7" \
  "\x7e\x79\x17\x48\x81\x74\x61\xe4\x8b\x2a\x8e\xc7" \
  "\x77\xee\x72\x2c\x39\xea\xe6\xb1\x94\x03\x38\xe7" \
  "\x7c\x5b\xa9\x40\xe4\x8b\x2a\xc2\xab\xf7\xef\xd6" \
  "\x12\x1d\xde\xbc\xb1\x6a\xb4\x50\x81\x08\x75\x1c" \
  "\x1f\x1c\x70\x34\x27\x91\x15\xaa\x95\x4f\x2b\x1a" \
  "\x39\xe7\xa8\xd7\xeb\xdc\x7f\xf0\xa8\xb0\x69\x59" \
  "\xd5\x6a\x75\x3b\x91\x88\x50\xab\xd5\x10\x11\x44" \
  "\x04\x55\x5d\xe4\xfe\xdd\x39\x87\x88\x6c\x26\xf2" \
  "\x0d\xfd\x7e\xff\xaf\x44\x95\x4a\x05\x55\xdd\x4c" \
  "\xa4\xaa\x0c\x06\x03\xba\xdd\x2e\x59\x96\x61\xad" \
  "\xc5\x5a\x4b\xbb\xdd\xa6\xd1\x68\xe0\x9c\xa3\xd7" \
  "\xeb\x51\x2e\x97\xb7\x13\x01\x64\x59\x46\xb3\xd9" \
  "\x04\x20\x8e\x63\x00\x26\x93\xc9\xa2\xbe\xf5\x8e" \
  "\x3c\xb2\xb5\x16\xb8\x1c\x17\x9f\x4f\xa7\xd3\x85" \
  "\xd1\xd6\xbf\xe6\x37\x5a\x6b\x89\xe3\x18\x6b\x2d" \
  "\x59\x96\x15\x8c\xd6\xdd\x51\x30\x7f\x1a\x63\xcc" \
  "\xc8\x2f\xae\x0e\xae\x1f\xd4\x65\x25\x49\xf2\x1c" \
  "\xf8\x08\x7c\x00\x12\x6f\x54\x02\x0c\x97\xb3\x53" \
  "\x2a\x74\xad\x57\x0a\x8c\x80\x04\x48\x83\xa5\x42" \
  "\x69\x29\xfe\xd5\xc8\xc7\xff\xd3\x6f\x90\xc5\x44" \
  "\x58\x4e\xaf\x63\x27\x00\x00\x00\x00\x49\x45\x4e" \
  "\x44\xae\x42\x60\x82"
image5_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x12\x00\x00\x00\x12" \
  "\x08\x06\x00\x00\x00\x56\xce\x8e\x57\x00\x00\x02" \
  "\x9c\x49\x44\x41\x54\x78\x9c\x8d\xd4\xcf\x4b\x14" \
  "\x61\x1c\xc7\xf1\xf7\xee\x8c\x31\x56\xb8\x8a\x1a" \
  "\x4d\x14\x78\x48\xa8\xa0\x83\x42\xd1\xce\x4d\xea" \
  "\xb0\x6e\x5d\x0a\x91\x9a\x42\xc8\xb5\x4b\x20\x04" \
  "\xfe\x05\x21\x1e\x8a\xa4\xc0\x24\xb0\x1f\x10\x94" \
  "\x12\xc5\x1e\x82\x3c\x6c\xea\x21\x2c\x8d\x90\x82" \
  "\x88\x81\x12\x36\x0c\xdc\xd2\xc5\xd9\x6a\x9c\x7d" \
  "\x90\x71\xbf\x1d\xda\x4d\xd1\x44\xbf\x30\x0c\x3c" \
  "\x3f\x5e\x7c\x9e\x67\xbe\x4c\x88\x4d\xca\x8e\x45" \
  "\xa5\x50\x28\x20\xc0\x93\xd4\xdb\x08\xb0\x08\x2c" \
  "\x6f\xb6\x6f\x1d\x52\xaa\xd1\xfb\x5d\x62\xc7\xa2" \
  "\x62\xc7\xa2\x02\x54\x00\xda\x96\x11\x7f\x61\x56" \
  "\x64\x49\x56\x1e\x11\xf1\x67\x3e\x89\x1d\x6b\xd8" \
  "\x3a\x68\xc7\x1a\x44\x7c\x7f\x05\xf1\x7d\x91\x5f" \
  "\xbe\xf8\x73\xb3\xe2\xcf\x4c\xc9\xec\xab\x7b\x02" \
  "\x08\x60\x02\x9a\xbe\x16\xb0\x2c\x4b\xea\x2a\x84" \
  "\xc7\x83\x2f\x56\x06\x83\x3c\x04\x90\x0f\x72\x80" \
  "\x42\x01\xce\x17\xa7\x34\xdb\x00\x8c\x87\xd7\x22" \
  "\xed\x89\x76\x00\x5c\x95\x21\xaf\x14\x79\xcf\x85" \
  "\x40\x91\x57\x39\x08\x14\xca\x73\x51\x5f\xdf\x73" \
  "\x3c\xd1\x0b\xd0\x51\xda\xab\xad\x46\x2e\x27\x2e" \
  "\x93\x1a\x49\x91\x68\x3e\x84\xa9\xe5\xf0\xfc\x79" \
  "\x0c\xa3\x0a\xcf\x77\xd1\x03\x85\xf2\x3c\x58\xca" \
  "\x71\xa5\x37\x49\x7d\x5d\x80\xf3\x39\x3b\x04\xbc" \
  "\x03\x16\xb4\xd5\x49\x74\x5d\xa7\x7e\x7f\x3d\xa9" \
  "\xc9\x34\x2d\x9d\x57\x89\x37\xee\xa3\x56\xfb\x06" \
  "\x41\x40\xb0\xb4\x8c\xca\x3a\x78\xfe\x77\x3a\xba" \
  "\xae\x71\xfb\xc6\x51\x3c\x57\x6f\x71\xa6\xb3\x37" \
  "\x01\x4f\x2b\x25\xd1\x75\x1d\x15\x28\xf4\xb0\x4e" \
  "\xed\x9e\x5a\xda\x2e\xb4\x91\x1c\xff\xc8\xd9\xce" \
  "\xeb\xfc\x2e\xd4\x50\x15\xfe\x4a\x76\x2e\x4b\x47" \
  "\x77\x92\xc7\x03\x8d\xf4\x0f\xa4\x49\x0e\x3b\x17" \
  "\x8b\x07\x9a\x0f\x59\x96\x25\xc3\xcf\x87\x89\x54" \
  "\x47\xc8\x64\x32\xa4\x5e\xa6\x28\x2b\x94\x91\x2f" \
  "\xe4\x8b\x17\x0d\x86\x61\x30\x36\x3e\xc6\x83\xbb" \
  "\x0f\x68\xbf\xd4\x4e\xee\xdb\x04\x07\x8f\x9c\xa1" \
  "\xa7\xbb\x07\xe0\x00\x90\x0e\x59\x96\x25\x7d\xb7" \
  "\xfa\x30\x74\x83\xaa\xdd\x55\x6c\xdf\xb6\x9d\x48" \
  "\x75\x04\x37\xe3\xf2\xec\xc5\x33\xc2\xe1\x30\x6e" \
  "\xd6\x05\x40\x29\xf5\x0f\x77\xa6\x1d\x06\x87\x06" \
  "\x01\x4e\x02\xe3\x3a\x80\xe3\x38\x98\xb5\xe6\xdf" \
  "\x85\x3a\x30\x03\x66\x8d\x49\xeb\xe9\xd6\x7f\x49" \
  "\xfb\xef\xf4\x63\xe8\x06\x2a\x50\xa4\xa7\xd3\x64" \
  "\xe6\x33\xa5\xef\xb4\x03\xd0\x42\xc5\xee\xfc\x09" \
  "\x60\x9f\xb3\x89\xc7\xe2\x98\xa6\x49\xe5\xce\x4a" \
  "\x42\x65\x21\xca\xcb\xca\x89\xec\x8a\x60\x9a\x26" \
  "\x00\xe7\xed\xf3\xe4\xe6\x73\xb8\x9e\xcb\xc4\xe4" \
  "\x04\x40\x2b\x30\x02\x10\x2e\x76\x67\x33\xd0\x52" \
  "\xec\x56\xb1\xcf\xd9\xf2\xe8\xe1\x23\x19\x1d\x1e" \
  "\x95\xa9\x37\x53\x82\x20\xaf\xdf\xbc\x96\xa6\x13" \
  "\x4d\x12\x3d\x16\x2d\x75\x75\x02\x88\x17\xc3\x50" \
  "\xc2\x2a\x80\x4a\x60\xef\x86\x68\x6a\x74\x2d\x72" \
  "\xaa\x18\x42\x0b\xb1\xbe\xc2\xc0\xce\x55\xef\xc3" \
  "\xc5\x7b\x78\xba\x6a\x4d\x07\xf0\x03\x98\x02\xe6" \
  "\x80\xe5\xff\x41\x5b\x41\x17\x81\x0f\x25\x04\x60" \
  "\x33\x68\x23\xb4\xc0\x9a\x1f\xdc\x1f\x77\xb4\x56" \
  "\xeb\x8c\x7f\x39\xe6\x00\x00\x00\x00\x49\x45\x4e" \
  "\x44\xae\x42\x60\x82"
image6_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
  "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
  "\x93\x49\x44\x41\x54\x78\x9c\xed\x94\x3d\x0e\x80" \
  "\x20\x0c\x46\xa9\xf1\x54\x8c\xc4\x63\x19\x07\xc2" \
  "\xb1\x48\xc7\x5e\x0b\x27\xb0\x22\x60\x83\xb2\xf1" \
  "\x2d\x24\xd0\x3e\xfa\x07\x40\x44\x6a\x84\x96\x21" \
  "\xd4\x09\xe6\x5a\xf3\x0d\xf4\x18\xf6\xa3\x6c\x4c" \
  "\x64\x40\x0a\x06\x3e\x15\x5a\x63\x90\x38\xd5\x2e" \
  "\xd0\x1a\x43\x3c\x4b\x11\xa3\xbf\xa0\x2d\x47\xbe" \
  "\x72\xbb\x3c\xa8\x54\xe3\x98\x7e\x2b\x5d\x22\x03" \
  "\x25\x58\x29\xd3\xae\xe6\xb5\x22\xfd\x04\xce\xe1" \
  "\xbf\x82\xdf\x1a\xdd\x05\x96\x4c\x4f\x02\x3b\x2b" \
  "\x73\x92\x8e\x64\x75\x8e\x9d\x55\xca\x6c\xf2\x07" \
  "\x91\xeb\x56\x0a\xde\x90\xda\xeb\x93\x0a\xe6\x7f" \
  "\x3c\xc1\x0f\x9d\x5b\xa7\x46\x08\x49\x60\xf5\x0a" \
  "\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82"
image7_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x12\x00\x00\x00\x12" \
  "\x08\x06\x00\x00\x00\x56\xce\x8e\x57\x00\x00\x02" \
  "\x20\x49\x44\x41\x54\x78\x9c\x7d\x93\x31\x6b\xdb" \
  "\x40\x18\x86\x1f\xeb\x54\xd2\x36\x36\x4e\x48\x6c" \
  "\x48\x36\x43\xa7\x42\x41\x81\x6c\x5d\x8a\xe8\x50" \
  "\x92\x74\x71\x17\x43\xfa\x37\x5a\x53\xda\xa1\x90" \
  "\x60\xba\x79\xf7\x90\xa9\x43\x3a\x97\x92\x4c\xa6" \
  "\x5b\x57\x67\xf1\xa4\xc1\x1d\x9a\x88\x82\x0b\xae" \
  "\xec\xf8\x74\x77\xb2\x3a\xd8\x72\xed\xc8\xf6\x0b" \
  "\xc7\xe9\xee\x7b\xef\xd1\x7b\x1f\x5c\xa6\x52\xa9" \
  "\xc4\x2c\xd1\xf9\xf9\x79\x1e\x18\x00\x51\x1c\xc7" \
  "\xcf\xa4\x94\x96\x31\x26\x33\xeb\xc9\xe5\x72\xdf" \
  "\x81\xc8\x06\xa8\xd5\x6a\x29\x48\xbd\x5e\xc7\x75" \
  "\xdd\x5e\xb3\xd9\xdc\x05\x7e\x4b\x29\x2d\xcf\xf3" \
  "\xd6\xc3\x30\x14\x77\xac\x79\xa0\x67\x27\xab\x52" \
  "\xa9\x34\x57\x15\x42\x70\xf9\xed\x2b\x2f\x0e\x5f" \
  "\x5e\x37\x9b\xcd\xdd\xc1\x60\x20\xc2\x30\x14\x52" \
  "\xca\xbb\x20\x01\x64\xac\x65\xd7\x02\x78\xfb\xee" \
  "\x3d\x00\xae\xeb\x5e\x5f\x5d\x5d\x6d\x6a\xad\x97" \
  "\xfa\xed\x45\x9b\x6a\x18\xf0\xe9\xe3\x1b\xfc\x3f" \
  "\x12\xaf\xdd\xe2\xf9\xd1\x2b\x8a\xc5\xe2\x97\xa4" \
  "\x7e\x7c\x7c\xfc\x3a\x97\xcb\x29\xdb\xb6\x47\xc9" \
  "\x5e\xea\x0f\x6a\x18\x10\xab\x00\x13\xde\xb2\x79" \
  "\xaf\x47\x2c\x6f\x00\x28\x97\xcb\xd4\x6a\x35\x0a" \
  "\x85\x02\xf5\x7a\xfd\xb3\xef\xfb\x59\x63\x8c\xb5" \
  "\x10\x34\x0b\x89\x54\xc0\x28\xec\x93\x51\x01\x00" \
  "\x3b\x3b\x3b\x94\x4a\x25\x84\x10\x5c\x5c\x5c\xd0" \
  "\x68\x34\xce\x7c\xdf\xcf\x26\x0c\x6b\x15\x24\x52" \
  "\x43\x32\x26\x4c\x5d\xbd\x5a\xad\x02\xd0\x68\x34" \
  "\xce\x80\x4d\xc0\x9a\xf6\x68\x11\x24\x52\x01\x8c" \
  "\xd4\xff\xc4\x4a\x71\x72\x72\x42\xb7\xdb\xa5\xdd" \
  "\x6e\x73\x70\x70\x00\xf0\x08\xb8\x99\x26\x5a\x04" \
  "\x89\xc2\x21\x56\x3c\x4e\xa4\xb5\x46\x29\x85\x52" \
  "\x8a\xb5\xb5\x35\x82\x20\x48\x8e\x3e\x98\x26\xba" \
  "\xe9\xb4\xf9\xa5\x6f\x89\xcd\x80\x38\x1c\x82\xe9" \
  "\x33\x32\x12\xc2\x3e\xb1\x19\x27\x32\xc6\x4c\x41" \
  "\xc9\x98\x95\x0d\xf0\xd4\x3d\x4a\xf5\x61\x56\x8e" \
  "\xe3\xcc\x25\xd2\x5a\x13\x45\xd1\x3c\xe8\xf4\xf4" \
  "\xf4\x70\x6f\x6f\xef\x49\x10\x04\xd9\xd9\x82\xe7" \
  "\x79\x1f\xca\xe5\x32\x1b\x1b\x1b\x68\xad\xa7\x89" \
  "\x12\x60\x0a\xb4\xbd\xbd\xad\x1c\xc7\xf9\x29\xa5" \
  "\xb4\xef\x80\xd8\xdf\xdf\x27\x9f\xcf\xcf\x25\x49" \
  "\xbe\x53\x20\x21\x44\xbc\xb5\xb5\x25\x17\xbc\x21" \
  "\x3a\x9d\x4e\x0a\xb2\x34\xd1\xaa\xde\xb8\xae\xbb" \
  "\xaa\x8c\xe3\x38\xb4\x5a\x2d\x00\x32\x8c\x5f\x6f" \
  "\x7e\x32\xcf\x6a\x1d\x78\x0c\x3c\x9c\xf8\x96\xe9" \
  "\x2f\xf0\x23\x31\x88\x05\x66\x0b\xb8\x3f\x99\x57" \
  "\x81\x22\x60\xf0\x0f\x77\xb0\x5d\xa0\x9c\x27\x1e" \
  "\x65\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60" \
  "\x82"
image8_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x16\x00\x00\x00\x16" \
  "\x08\x06\x00\x00\x00\xc4\xb4\x6c\x3b\x00\x00\x00" \
  "\xec\x49\x44\x41\x54\x78\x9c\xb5\x95\x4d\x0e\x83" \
  "\x20\x10\x85\xdf\x98\x9e\x6a\x12\x37\xbd\x96\xc4" \
  "\x45\x83\xd7\xea\xa6\xc9\x5c\x6b\xba\x40\x2d\xc8" \
  "\x50\xd0\xd2\x97\x98\x09\x3f\xf3\xcd\x13\x04\x49" \
  "\x44\xf0\x0f\xdd\xbe\x0d\x32\xb3\x1e\xfb\x44\x84" \
  "\x5a\xc0\xb4\x39\xb6\x20\x00\xa0\x51\x2f\x15\x90" \
  "\x56\xb1\xa1\x15\x6a\xb5\x37\x59\xf9\x04\x40\x01" \
  "\xc0\x3f\x3c\x00\x07\xc0\xc3\xcd\x6e\x07\xc5\x2e" \
  "\xe3\xb6\x35\x3f\x76\x4e\x00\xf4\x38\x49\x5e\xf5" \
  "\x0d\xe5\x91\x33\x78\x0c\x1e\x42\x08\x83\x21\x9e" \
  "\x51\x39\x6f\xfd\x2a\x7c\x32\x89\x47\x6e\x04\xa7" \
  "\x79\x06\xf8\x33\x18\xbf\xde\xb9\x98\x6a\xb0\x2b" \
  "\x5f\x89\xa9\xd6\xcd\x2b\xc3\xdd\x9c\x27\xd9\x4a" \
  "\x37\xcf\x5c\xe3\xa3\x13\xd5\xa9\x88\x23\x5a\xa0" \
  "\x3a\x65\x87\x27\x5b\xe3\x12\x9c\x68\xc9\xa0\x71" \
  "\xc1\x00\x5f\x54\xe4\x4e\xcd\x8e\x6b\xae\x2d\x78" \
  "\x37\xc7\x47\x78\x17\xc7\x56\xd1\x9f\x1d\x5b\x05" \
  "\x89\x96\xbe\x6b\xdc\xcd\xb1\xa5\xdd\xc0\x7a\xd1" \
  "\x6b\xf9\xf1\x7a\x56\x80\x57\xaa\xfd\xf3\x98\x9f" \
  "\x85\xeb\xfd\xbb\xaa\xe0\xab\x7a\x03\x0d\x36\xe3" \
  "\xe7\x26\xe8\xd8\x99\x00\x00\x00\x00\x49\x45\x4e" \
  "\x44\xae\x42\x60\x82"
image9_data = \
  "\x89\x50\x4e\x47\x0d\x0a\x1a\x0a\x00\x00\x00\x0d" \
  "\x49\x48\x44\x52\x00\x00\x00\x12\x00\x00\x00\x12" \
  "\x08\x06\x00\x00\x00\x56\xce\x8e\x57\x00\x00\x03" \
  "\xea\x49\x44\x41\x54\x78\x9c\x75\x94\x5b\x6c\x53" \
  "\x05\x18\xc7\x7f\xe7\xf4\xb0\xb5\x6b\xb7\x76\x5d" \
  "\x4b\x3b\xd8\xd8\xd6\x0d\x6c\xd4\x69\x18\x08\x01" \
  "\x46\xc0\xc5\x0c\xc2\x83\xf0\x60\x00\x45\x44\x13" \
  "\x1e\xbc\x3c\xf8\x0e\x3e\xf0\x20\x2f\x46\x49\x8c" \
  "\xfa\x24\x72\x09\x91\x98\x30\x12\x09\x28\x90\x85" \
  "\xc2\x83\xdc\xd4\x31\x1c\x97\x75\x20\x29\xec\x74" \
  "\x5d\x57\xd8\xe5\xf4\x76\x4e\xcf\xd5\x07\x26\x09" \
  "\x8b\xfe\x9f\xbe\xa7\x5f\xfe\xdf\xe5\xff\x09\xcc" \
  "\x6a\xe7\xce\xf7\x1a\x15\x45\x09\xd7\xd7\xd7\x27" \
  "\xf2\x85\x42\xc3\xe4\x93\x27\xcc\x8f\x44\x70\xbb" \
  "\xdd\x5c\xbd\x72\x79\x69\x2c\x16\x9b\xea\xef\xef" \
  "\x1f\xe5\x7f\x24\x01\x6c\xe8\xdd\x18\x13\x1d\xe7" \
  "\x9b\xe6\x96\x96\x4d\xeb\xdf\xe8\x61\xf1\x4b\x9d" \
  "\xb8\x7d\x75\x54\x54\x95\x54\x32\x49\x45\xd3\x06" \
  "\x0d\x5d\xbb\xd2\xd3\xd3\xf3\x61\x22\x91\xb8\x0d" \
  "\x38\x73\x41\xc2\xd6\xad\x5b\x1d\xcb\xb2\x58\xd5" \
  "\xbd\x96\x2d\x3b\x76\x10\x0b\x87\x48\x9b\x30\xa9" \
  "\x59\x28\xba\x85\x28\x89\x44\x45\x83\x4b\xc7\x8f" \
  "\x71\xa2\xaf\x0f\xcb\x32\x5f\x4e\x24\x2e\xde\x9d" \
  "\x0b\x13\xdd\x6e\x37\xfe\xfa\x10\x6f\x6e\x7f\x9b" \
  "\xf6\x70\x08\x01\x88\xba\x1c\x1c\x43\x43\x9e\x9a" \
  "\xe6\xfa\x83\x47\x24\xc6\xa6\x58\xbe\xe5\x2d\x16" \
  "\x77\xb4\x63\x54\x8c\xb5\x5d\x5d\x5d\x1e\x40\x78" \
  "\x1e\xe4\xf1\xf0\xce\xae\x77\xa9\x09\x04\x90\x4b" \
  "\x3a\x00\x13\x9a\xce\x13\x55\xc7\x06\x6c\xd1\xc5" \
  "\x40\x2a\xcd\x95\x69\x83\x8d\xef\xef\x66\xcd\x9a" \
  "\x55\x5f\x78\x3c\x9e\x26\x40\x7c\x6e\x46\xc9\xe1" \
  "\x24\x2d\xad\x31\x34\x4b\x64\x3c\x5f\x46\x77\x6c" \
  "\x46\x66\x54\x72\x9a\x4e\x4e\x33\x19\x2d\x18\xa4" \
  "\xd2\x19\x1a\x03\x3e\x96\xb5\x2f\x61\x60\xf0\x66" \
  "\xed\xd0\xd0\x50\x08\x90\x01\xed\xdf\x16\x45\x80" \
  "\x72\x45\xa5\x6c\x54\x78\x5c\x29\x73\x3d\x57\x60" \
  "\x7c\x16\x22\xab\x3a\x99\xcc\x28\xa5\x09\x19\x15" \
  "\xd0\xd5\x12\x33\xca\x0c\x85\x42\x21\x0c\x54\x3d" \
  "\xe7\x28\x1e\x7f\x81\xbf\xef\xde\xa5\x69\x75\x84" \
  "\x74\xb1\x42\x49\x37\xa8\x98\x36\x59\xc3\xe1\xe1" \
  "\x44\x16\xe5\xfe\x1d\x6a\x42\x61\xba\x1a\xa3\xdc" \
  "\xbb\x7c\x01\x7f\x9d\xdf\xf0\xf9\x7c\xf3\x8a\xc5" \
  "\xa2\x38\x3b\xa7\xa7\x8e\x74\x43\xe7\xeb\x2f\xbf" \
  "\x42\x49\x8d\xd0\x16\x89\x90\x53\x66\x18\x1a\x95" \
  "\x19\xbe\x73\x13\x65\xf8\x2f\x6c\x6f\x80\xcd\xaf" \
  "\xf7\xb2\x32\x30\x8f\x13\x47\x0e\x33\x3c\xf2\xe0" \
  "\x5a\xb1\x54\x29\xcf\x5d\xbf\x6b\xc5\x8a\x15\xfb" \
  "\x96\x2f\x5f\xc6\x6f\xe7\xcf\xb2\x3a\xde\x4e\x47" \
  "\x5b\x07\x0b\xc3\x41\x62\xcd\x4d\xbc\xf2\x62\x27" \
  "\xbb\xba\x5f\x63\x89\xfa\x98\x3d\x9f\x7c\xc4\xe5" \
  "\x6b\x83\x1c\xd8\xb3\xb8\xc5\xd4\xa7\xae\xde\x4b" \
  "\xa9\x83\x80\xfe\x0c\x14\x8b\xc5\xf6\x75\x77\x77" \
  "\x33\x33\xa3\x70\xf4\x87\x43\x4c\x3e\xce\xb2\xc8" \
  "\xe3\xa6\x49\xb2\xa9\x9e\x90\x49\x9c\x3b\xc3\xf1" \
  "\xef\x0f\x32\xf0\xfb\x45\x7e\x3a\xb0\x92\xcd\xbb" \
  "\xfb\xb8\x70\xee\xd0\x26\xa1\x3a\x7e\x6d\x7c\x3c" \
  "\x9d\x02\x6c\x00\x49\x10\x04\xda\xda\xda\x08\x04" \
  "\x02\x04\x1b\x82\x64\x33\x19\xce\xff\x78\x94\x87" \
  "\xb2\xcc\xc2\x68\x14\xb1\xba\x9a\x05\x41\x89\x05" \
  "\xeb\x03\x64\xf2\x75\x9c\x3e\x7d\x89\x83\xc7\x53" \
  "\xac\x5b\xb7\xfe\x54\x3c\x1e\xff\x20\x99\x4c\x9e" \
  "\x04\x8a\x92\x20\x08\xd4\xd6\xd6\x12\x8d\x46\xf0" \
  "\xd7\xd5\x90\x1e\x7d\x44\x66\x6c\x8c\xa5\xaf\x2e" \
  "\xc1\xd4\x2b\xf8\x7c\x5e\xaa\x5d\x06\x72\x2a\xc7" \
  "\xc9\x5f\x6f\x31\x91\xcf\x51\x2e\xab\xec\xdf\xff" \
  "\x39\x7b\xf7\x7e\x76\x38\x9f\xcf\xcf\xcf\x64\x32" \
  "\x47\x5c\x9d\x9d\x9d\xfb\x7a\x7b\x7b\x09\x05\x7c" \
  "\xd4\x54\xb9\xf0\xd5\xcc\xa3\xce\xe7\x26\xe8\xf7" \
  "\x32\xbf\xa1\x96\x80\x4f\xa2\xc1\xef\x45\x2d\x59" \
  "\x5c\xfa\x63\x02\xad\x5c\xb6\x06\x6f\xdf\x12\x1b" \
  "\xc3\x11\x36\x6c\xe8\x65\x2c\x9d\xe9\x36\x2d\x73" \
  "\x4c\x04\x10\x04\x01\x49\xb4\xf1\xd6\x54\x11\x69" \
  "\xf0\xd3\xd6\x1c\xa1\xa3\x25\x42\xc7\xa2\x08\xb1" \
  "\xe6\x08\x8b\x1a\xeb\x59\x10\xf2\x53\x2e\x97\x19" \
  "\x1a\x1a\xbc\xaa\xe5\x0b\x66\xdf\xa9\x9f\xc9\x66" \
  "\x73\x6c\xdb\xbe\xcd\xd3\xd4\xd4\xfc\xad\xe4\x38" \
  "\x4f\xb3\x67\x99\x1a\x8e\xa9\xe2\x12\x4c\xbc\x55" \
  "\x22\x96\xe0\xc2\x92\x5c\xd8\x86\x88\x63\x3a\x78" \
  "\xaa\x1d\x24\x49\x02\xf8\xa5\x58\x2c\x5a\xd3\xca" \
  "\xf4\xba\x33\xe7\xce\x52\xe5\x72\x71\xe3\xc6\xc0" \
  "\xd3\x37\x92\x95\x93\x64\x65\xb0\xcd\x32\x8e\xa1" \
  "\xe2\x18\x2a\xb6\xa9\x3e\xab\x1d\x43\xc5\xe5\x58" \
  "\x88\xa2\x08\x90\xb9\x77\x7f\xe4\x3b\x51\x14\x4b" \
  "\x8a\xa2\x6c\x0a\x06\x43\xb4\xb6\xb6\x1e\x93\x04" \
  "\x41\xe0\xe3\x4f\xf7\xcc\xbd\xaf\xff\x94\x20\x08" \
  "\xcc\xe6\xeb\x4f\xdb\xb6\xd3\x53\x93\x93\x7d\x38" \
  "\x8e\xb7\x54\x2a\xc9\xff\x00\x02\xdf\xce\x39\x6e" \
  "\xaf\x00\x2c\x00\x00\x00\x00\x49\x45\x4e\x44\xae" \
  "\x42\x60\x82"

class MainEntry(QMainWindow):
  def __init__(self,parent = None,name = None,fl = 0):
    QMainWindow.__init__(self,parent,name,fl)
    self.statusBar()

    self.image0 = QPixmap()
    self.image0.loadFromData(image0_data,"PNG")
    self.image2 = QPixmap()
    self.image2.loadFromData(image2_data,"PNG")
    self.image3 = QPixmap()
    self.image3.loadFromData(image3_data,"PNG")
    self.image4 = QPixmap()
    self.image4.loadFromData(image4_data,"PNG")
    self.image5 = QPixmap()
    self.image5.loadFromData(image5_data,"PNG")
    self.image6 = QPixmap()
    self.image6.loadFromData(image6_data,"PNG")
    self.image7 = QPixmap()
    self.image7.loadFromData(image7_data,"PNG")
    self.image8 = QPixmap()
    self.image8.loadFromData(image8_data,"PNG")
    self.image9 = QPixmap()
    self.image9.loadFromData(image9_data,"PNG")
    if not name:
      self.setName("frmMainEntry")

    self.setMinimumSize(QSize(21,181))
    f = QFont(self.font())
    f.setFamily("Bitstream Cyberbit")
    self.setFont(f)
    self.setIcon(self.image0)

    self.setCentralWidget(QWidget(self,"qt_central_widget"))

    self.frmToolbar = QFrame(self.centralWidget(),"frmToolbar")
    self.frmToolbar.setGeometry(QRect(0,0,731,50))
    self.frmToolbar.setFrameShape(QFrame.StyledPanel)
    self.frmToolbar.setFrameShadow(QFrame.Raised)

    self.lblOrderBy = QLabel(self.frmToolbar,"lblOrderBy")
    self.lblOrderBy.setGeometry(QRect(540,10,63,29))
    self.lblOrderBy.setFocusPolicy(QLabel.NoFocus)

    self.pbFirst = QPushButton(self.frmToolbar,"pbFirst")
    self.pbFirst.setGeometry(QRect(11,6,46,37))
    self.pbFirst.setSizePolicy(QSizePolicy(0,0,0,0,self.pbFirst.sizePolicy().hasHeightForWidth()))

    self.pbLast = QPushButton(self.frmToolbar,"pbLast")
    self.pbLast.setGeometry(QRect(63,6,42,37))
    self.pbLast.setSizePolicy(QSizePolicy(0,0,0,0,self.pbLast.sizePolicy().hasHeightForWidth()))

    self.pbReveal = QPushButton(self.frmToolbar,"pbReveal")
    self.pbReveal.setGeometry(QRect(238,6,57,37))
    self.pbReveal.setSizePolicy(QSizePolicy(0,0,0,0,self.pbReveal.sizePolicy().hasHeightForWidth()))

    self.pbSearch = QPushButton(self.frmToolbar,"pbSearch")
    self.pbSearch.setGeometry(QRect(301,6,54,37))
    self.pbSearch.setSizePolicy(QSizePolicy(0,0,0,0,self.pbSearch.sizePolicy().hasHeightForWidth()))

    self.cmbOrderBy = QComboBox(0,self.frmToolbar,"cmbOrderBy")
    self.cmbOrderBy.setGeometry(QRect(405,10,120,30))

    self.pbNext = QPushButton(self.frmToolbar,"pbNext")
    self.pbNext.setGeometry(QRect(185,6,47,37))
    self.pbNext.setSizePolicy(QSizePolicy(0,0,0,0,self.pbNext.sizePolicy().hasHeightForWidth()))
    self.pbNext.setAutoRepeat(1)

    self.pbPrevious = QPushButton(self.frmToolbar,"pbPrevious")
    self.pbPrevious.setGeometry(QRect(111,6,68,37))
    self.pbPrevious.setSizePolicy(QSizePolicy(0,0,0,0,self.pbPrevious.sizePolicy().hasHeightForWidth()))
    self.pbPrevious.setAutoRepeat(1)

    self.tabVocab = QTabWidget(self.centralWidget(),"tabVocab")
    self.tabVocab.setGeometry(QRect(0,49,730,520))

    self.tab = QWidget(self.tabVocab,"tab")

    self.pbClose = QPushButton(self.tab,"pbClose")
    self.pbClose.setGeometry(QRect(580,490,97,37))

    self.leId = QLineEdit(self.tab,"leId")
    self.leId.setGeometry(QRect(579,10,60,36))
    self.leId.setPaletteForegroundColor(QColor(0,0,0))
    self.leId.setPaletteBackgroundColor(QColor(211,205,204))
    self.leId.setFocusPolicy(QLineEdit.NoFocus)
    self.leId.setReadOnly(1)

    self.pbUnicode = QPushButton(self.tab,"pbUnicode")
    self.pbUnicode.setGeometry(QRect(180,10,103,37))

    self.leMeaning = QLineEdit(self.tab,"leMeaning")
    self.leMeaning.setGeometry(QRect(400,210,230,36))
    leMeaning_font = QFont(self.leMeaning.font())
    leMeaning_font.setPointSize(14)
    self.leMeaning.setFont(leMeaning_font)

    self.leJidhr1 = lineeditarabic(self.tab,"leJidhr1")
    self.leJidhr1.setGeometry(QRect(451,4,39,40))
    self.leJidhr1.setMinimumSize(QSize(0,33))
    leJidhr1_font = QFont(self.leJidhr1.font())
    leJidhr1_font.setPointSize(20)
    self.leJidhr1.setFont(leJidhr1_font)
    self.leJidhr1.setFocusPolicy(lineeditarabic.StrongFocus)

    self.leJidhr2 = lineeditarabic(self.tab,"leJidhr2")
    self.leJidhr2.setGeometry(QRect(407,4,38,40))
    self.leJidhr2.setMinimumSize(QSize(0,33))
    leJidhr2_font = QFont(self.leJidhr2.font())
    leJidhr2_font.setPointSize(20)
    self.leJidhr2.setFont(leJidhr2_font)

    self.leJidhr3 = lineeditarabic(self.tab,"leJidhr3")
    self.leJidhr3.setGeometry(QRect(362,4,39,40))
    self.leJidhr3.setMinimumSize(QSize(0,33))
    leJidhr3_font = QFont(self.leJidhr3.font())
    leJidhr3_font.setPointSize(20)
    self.leJidhr3.setFont(leJidhr3_font)

    self.leJidhr4 = lineeditarabic(self.tab,"leJidhr4")
    self.leJidhr4.setGeometry(QRect(317,4,39,40))
    self.leJidhr4.setMinimumSize(QSize(0,33))
    leJidhr4_font = QFont(self.leJidhr4.font())
    leJidhr4_font.setPointSize(20)
    self.leJidhr4.setFont(leJidhr4_font)

    self.leIsmP = lineeditarabic(self.tab,"leIsmP")
    self.leIsmP.setGeometry(QRect(216,62,159,36))
    leIsmP_font = QFont(self.leIsmP.font())
    leIsmP_font.setPointSize(20)
    self.leIsmP.setFont(leIsmP_font)

    self.leIsmS = lineeditarabic(self.tab,"leIsmS")
    self.leIsmS.setGeometry(QRect(465,63,159,36))
    leIsmS_font = QFont(self.leIsmS.font())
    leIsmS_font.setPointSize(20)
    self.leIsmS.setFont(leIsmS_font)

    self.leFilMa = lineeditarabic(self.tab,"leFilMa")
    self.leFilMa.setGeometry(QRect(464,110,159,36))
    leFilMa_font = QFont(self.leFilMa.font())
    leFilMa_font.setPointSize(20)
    self.leFilMa.setFont(leFilMa_font)

    self.leFilMu = lineeditarabic(self.tab,"leFilMu")
    self.leFilMu.setGeometry(QRect(192,110,183,36))
    leFilMu_font = QFont(self.leFilMu.font())
    leFilMu_font.setPointSize(20)
    self.leFilMu.setFont(leFilMu_font)

    self.leMasdar = lineeditarabic(self.tab,"leMasdar")
    self.leMasdar.setGeometry(QRect(18,110,142,36))
    leMasdar_font = QFont(self.leMasdar.font())
    leMasdar_font.setPointSize(20)
    self.leMasdar.setFont(leMasdar_font)

    self.leExample = lineeditarabic(self.tab,"leExample")
    self.leExample.setGeometry(QRect(235,262,395,36))
    leExample_font = QFont(self.leExample.font())
    leExample_font.setPointSize(20)
    self.leExample.setFont(leExample_font)

    self.leHarf = lineeditarabic(self.tab,"leHarf")
    self.leHarf.setGeometry(QRect(465,161,159,36))
    leHarf_font = QFont(self.leHarf.font())
    leHarf_font.setPointSize(20)
    self.leHarf.setFont(leHarf_font)

    self.lblId = QLineEdit(self.tab,"lblId")
    self.lblId.setGeometry(QRect(650,11,50,36))
    self.lblId.setPaletteBackgroundColor(QColor(238,238,230))
    self.lblId.setBackgroundOrigin(QLineEdit.WindowOrigin)
    lblId_font = QFont(self.lblId.font())
    lblId_font.setPointSize(16)
    self.lblId.setFont(lblId_font)
    self.lblId.setFocusPolicy(QLineEdit.NoFocus)
    self.lblId.setFrameShape(QLineEdit.NoFrame)
    self.lblId.setFrameShadow(QLineEdit.Raised)
    self.lblId.setReadOnly(1)

    self.lblJidhr = QLineEdit(self.tab,"lblJidhr")
    self.lblJidhr.setGeometry(QRect(510,11,50,36))
    self.lblJidhr.setPaletteBackgroundColor(QColor(238,238,230))
    lblJidhr_font = QFont(self.lblJidhr.font())
    lblJidhr_font.setPointSize(16)
    self.lblJidhr.setFont(lblJidhr_font)
    self.lblJidhr.setFocusPolicy(QLineEdit.NoFocus)
    self.lblJidhr.setFrameShape(QLineEdit.NoFrame)
    self.lblJidhr.setReadOnly(1)

    self.lblFilMu = QLineEdit(self.tab,"lblFilMu")
    self.lblFilMu.setGeometry(QRect(390,111,60,36))
    self.lblFilMu.setPaletteBackgroundColor(QColor(238,238,230))
    lblFilMu_font = QFont(self.lblFilMu.font())
    lblFilMu_font.setPointSize(16)
    self.lblFilMu.setFont(lblFilMu_font)
    self.lblFilMu.setFocusPolicy(QLineEdit.NoFocus)
    self.lblFilMu.setFrameShape(QLineEdit.NoFrame)
    self.lblFilMu.setReadOnly(1)

    self.lblFilMa = QLineEdit(self.tab,"lblFilMa")
    self.lblFilMa.setGeometry(QRect(650,111,60,36))
    self.lblFilMa.setPaletteBackgroundColor(QColor(238,238,230))
    lblFilMa_font = QFont(self.lblFilMa.font())
    lblFilMa_font.setPointSize(16)
    self.lblFilMa.setFont(lblFilMa_font)
    self.lblFilMa.setFocusPolicy(QLineEdit.NoFocus)
    self.lblFilMa.setFrameShape(QLineEdit.NoFrame)
    self.lblFilMa.setReadOnly(1)

    self.lblHarf = QLineEdit(self.tab,"lblHarf")
    self.lblHarf.setGeometry(QRect(650,161,60,36))
    self.lblHarf.setPaletteBackgroundColor(QColor(238,238,230))
    lblHarf_font = QFont(self.lblHarf.font())
    lblHarf_font.setPointSize(16)
    self.lblHarf.setFont(lblHarf_font)
    self.lblHarf.setFocusPolicy(QLineEdit.NoFocus)
    self.lblHarf.setFrameShape(QLineEdit.NoFrame)
    self.lblHarf.setReadOnly(1)

    self.lblMeaning = QLineEdit(self.tab,"lblMeaning")
    self.lblMeaning.setGeometry(QRect(646,211,60,36))
    self.lblMeaning.setPaletteBackgroundColor(QColor(238,238,230))
    lblMeaning_font = QFont(self.lblMeaning.font())
    lblMeaning_font.setPointSize(16)
    self.lblMeaning.setFont(lblMeaning_font)
    self.lblMeaning.setFocusPolicy(QLineEdit.NoFocus)
    self.lblMeaning.setFrameShape(QLineEdit.NoFrame)
    self.lblMeaning.setReadOnly(1)

    self.lblExample = QLineEdit(self.tab,"lblExample")
    self.lblExample.setGeometry(QRect(650,261,60,36))
    self.lblExample.setPaletteBackgroundColor(QColor(238,238,230))
    lblExample_font = QFont(self.lblExample.font())
    lblExample_font.setPointSize(16)
    self.lblExample.setFont(lblExample_font)
    self.lblExample.setFocusPolicy(QLineEdit.NoFocus)
    self.lblExample.setFrameShape(QLineEdit.NoFrame)
    self.lblExample.setReadOnly(1)

    self.lblMasdar = QLineEdit(self.tab,"lblMasdar")
    self.lblMasdar.setGeometry(QRect(90,60,70,36))
    self.lblMasdar.setPaletteBackgroundColor(QColor(238,238,230))
    lblMasdar_font = QFont(self.lblMasdar.font())
    lblMasdar_font.setPointSize(16)
    self.lblMasdar.setFont(lblMasdar_font)
    self.lblMasdar.setFocusPolicy(QLineEdit.NoFocus)
    self.lblMasdar.setFrameShape(QLineEdit.NoFrame)
    self.lblMasdar.setReadOnly(1)

    self.lblIsmP = QLineEdit(self.tab,"lblIsmP")
    self.lblIsmP.setGeometry(QRect(390,61,70,36))
    self.lblIsmP.setPaletteBackgroundColor(QColor(238,238,230))
    lblIsmP_font = QFont(self.lblIsmP.font())
    lblIsmP_font.setPointSize(16)
    self.lblIsmP.setFont(lblIsmP_font)
    self.lblIsmP.setFocusPolicy(QLineEdit.NoFocus)
    self.lblIsmP.setFrameShape(QLineEdit.NoFrame)
    self.lblIsmP.setReadOnly(1)

    self.lblIsmS = QLineEdit(self.tab,"lblIsmS")
    self.lblIsmS.setGeometry(QRect(650,61,70,36))
    self.lblIsmS.setPaletteBackgroundColor(QColor(238,238,230))
    lblIsmS_font = QFont(self.lblIsmS.font())
    lblIsmS_font.setPointSize(16)
    self.lblIsmS.setFont(lblIsmS_font)
    self.lblIsmS.setFocusPolicy(QLineEdit.NoFocus)
    self.lblIsmS.setFrameShape(QLineEdit.NoFrame)
    self.lblIsmS.setReadOnly(1)

    self.pbAdd = QPushButton(self.tab,"pbAdd")
    self.pbAdd.setGeometry(QRect(250,421,96,37))

    self.pbExtraRevision = QPushButton(self.tab,"pbExtraRevision")
    self.pbExtraRevision.setGeometry(QRect(480,420,152,37))

    self.pbDelete = QPushButton(self.tab,"pbDelete")
    self.pbDelete.setGeometry(QRect(361,421,97,37))

    self.lbBooks = QListBox(self.tab,"lbBooks")
    self.lbBooks.setGeometry(QRect(9,175,178,280))
    self.lbBooks.setSelectionMode(QListBox.Multi)

    self.bgRevision = QButtonGroup(self.tab,"bgRevision")
    self.bgRevision.setGeometry(QRect(234,313,400,80))

    self.rbReviseArabic = QRadioButton(self.bgRevision,"rbReviseArabic")
    self.rbReviseArabic.setGeometry(QRect(20,10,120,34))

    self.rbShowBoth = QRadioButton(self.bgRevision,"rbShowBoth")
    self.rbShowBoth.setEnabled(1)
    self.rbShowBoth.setGeometry(QRect(290,10,106,34))

    self.rbReviseEnglish = QRadioButton(self.bgRevision,"rbReviseEnglish")
    self.rbReviseEnglish.setGeometry(QRect(155,8,120,34))

    self.checkBox3 = QCheckBox(self.bgRevision,"checkBox3")
    self.checkBox3.setGeometry(QRect(260,50,130,25))
    self.tabVocab.insertTab(self.tab,QString(""))

    self.tab_2 = QWidget(self.tabVocab,"tab_2")

    self.frame4 = QFrame(self.tab_2,"frame4")
    self.frame4.setGeometry(QRect(-2,1,726,82))
    self.frame4.setFrameShape(QFrame.StyledPanel)
    self.frame4.setFrameShadow(QFrame.Raised)

    self.textLabel1 = QLabel(self.frame4,"textLabel1")
    self.textLabel1.setGeometry(QRect(18,13,50,29))

    self.cbPubPrint1 = QCheckBox(self.frame4,"cbPubPrint1")
    self.cbPubPrint1.setGeometry(QRect(257,51,89,24))

    self.cbPubPrint2 = QCheckBox(self.frame4,"cbPubPrint2")
    self.cbPubPrint2.setGeometry(QRect(422,50,89,24))

    self.lePubKalima1 = QLineEdit(self.frame4,"lePubKalima1")
    self.lePubKalima1.setGeometry(QRect(419,9,159,36))
    self.lePubKalima1.setBackgroundOrigin(QLineEdit.AncestorOrigin)
    lePubKalima1_font = QFont(self.lePubKalima1.font())
    lePubKalima1_font.setPointSize(14)
    self.lePubKalima1.setFont(lePubKalima1_font)
    self.lePubKalima1.setFocusPolicy(QLineEdit.NoFocus)
    self.lePubKalima1.setReadOnly(1)

    self.lePubKalima2 = QLineEdit(self.frame4,"lePubKalima2")
    self.lePubKalima2.setGeometry(QRect(250,9,159,36))
    self.lePubKalima2.setBackgroundOrigin(QLineEdit.WindowOrigin)
    lePubKalima2_font = QFont(self.lePubKalima2.font())
    lePubKalima2_font.setPointSize(14)
    self.lePubKalima2.setFont(lePubKalima2_font)
    self.lePubKalima2.setFocusPolicy(QLineEdit.NoFocus)
    self.lePubKalima2.setReadOnly(1)

    self.lePubKalima3 = QLineEdit(self.frame4,"lePubKalima3")
    self.lePubKalima3.setGeometry(QRect(80,9,159,36))
    self.lePubKalima3.setBackgroundOrigin(QLineEdit.ParentOrigin)
    lePubKalima3_font = QFont(self.lePubKalima3.font())
    lePubKalima3_font.setPointSize(14)
    self.lePubKalima3.setFont(lePubKalima3_font)
    self.lePubKalima3.setFocusPolicy(QLineEdit.NoFocus)
    self.lePubKalima3.setReadOnly(1)

    self.frame5 = QFrame(self.tab_2,"frame5")
    self.frame5.setGeometry(QRect(509,244,203,180))
    self.frame5.setFrameShape(QFrame.StyledPanel)
    self.frame5.setFrameShadow(QFrame.Raised)

    self.pbAddSection = QPushButton(self.frame5,"pbAddSection")
    self.pbAddSection.setGeometry(QRect(19,54,159,37))

    self.pbDeleteSection = QPushButton(self.frame5,"pbDeleteSection")
    self.pbDeleteSection.setGeometry(QRect(19,97,159,37))

    self.leSectionName = QLineEdit(self.frame5,"leSectionName")
    self.leSectionName.setGeometry(QRect(19,12,159,36))

    self.frame6 = QFrame(self.tab_2,"frame6")
    self.frame6.setGeometry(QRect(510,100,203,134))
    self.frame6.setFrameShape(QFrame.StyledPanel)
    self.frame6.setFrameShadow(QFrame.Raised)

    self.pbAddToSection = QPushButton(self.frame6,"pbAddToSection")
    self.pbAddToSection.setGeometry(QRect(16,9,170,37))

    self.pbRemoveFromSection = QPushButton(self.frame6,"pbRemoveFromSection")
    self.pbRemoveFromSection.setGeometry(QRect(16,52,170,37))

    self.lbSectionWords = QListBox(self.tab_2,"lbSectionWords")
    self.lbSectionWords.setGeometry(QRect(257,97,239,365))

    self.lvSections = QListView(self.tab_2,"lvSections")
    self.lvSections.addColumn(self.__tr("Section"))
    self.lvSections.setGeometry(QRect(7,95,233,364))
    self.lvSections.setSizePolicy(QSizePolicy(7,5,0,0,self.lvSections.sizePolicy().hasHeightForWidth()))
    lvSections_font = QFont(self.lvSections.font())
    lvSections_font.setFamily("Sans")
    lvSections_font.setPointSize(8)
    self.lvSections.setFont(lvSections_font)
    self.tabVocab.insertTab(self.tab_2,QString(""))

    self.tab_3 = QWidget(self.tabVocab,"tab_3")

    self.splitter2 = QSplitter(self.tab_3,"splitter2")
    self.splitter2.setGeometry(QRect(276,132,418,36))
    self.splitter2.setOrientation(QSplitter.Horizontal)

    self.lblInformDND = QLabel(self.tab_3,"lblInformDND")
    self.lblInformDND.setGeometry(QRect(248,329,318,29))

    self.leLayoutSectionName = QLineEdit(self.tab_3,"leLayoutSectionName")
    self.leLayoutSectionName.setGeometry(QRect(445,34,246,36))
    self.leLayoutSectionName.setAlignment(QLineEdit.AlignRight)

    self.leLayoutKalima3 = lineeditdrag(self.tab_3,"leLayoutKalima3")
    self.leLayoutKalima3.setGeometry(QRect(195,141,233,31))

    self.leLayoutKalima5 = lineeditdrag(self.tab_3,"leLayoutKalima5")
    self.leLayoutKalima5.setGeometry(QRect(187,185,244,31))

    self.leLayoutKalima7 = lineeditdrag(self.tab_3,"leLayoutKalima7")
    self.leLayoutKalima7.setGeometry(QRect(188,229,244,31))

    self.leLayoutKalima9 = lineeditdrag(self.tab_3,"leLayoutKalima9")
    self.leLayoutKalima9.setGeometry(QRect(190,269,244,31))

    self.leLayoutKalima2 = lineeditdrag(self.tab_3,"leLayoutKalima2")
    self.leLayoutKalima2.setGeometry(QRect(440,95,247,31))

    self.leLayoutKalima4 = lineeditdrag(self.tab_3,"leLayoutKalima4")
    self.leLayoutKalima4.setGeometry(QRect(442,143,244,31))

    self.leLayoutKalima6 = lineeditdrag(self.tab_3,"leLayoutKalima6")
    self.leLayoutKalima6.setGeometry(QRect(445,186,244,31))

    self.leLayoutKalima8 = lineeditdrag(self.tab_3,"leLayoutKalima8")
    self.leLayoutKalima8.setGeometry(QRect(444,230,244,31))

    self.leLayoutKalima10 = lineeditdrag(self.tab_3,"leLayoutKalima10")
    self.leLayoutKalima10.setGeometry(QRect(444,269,244,31))

    self.leLayoutKalima1 = lineeditdrag(self.tab_3,"leLayoutKalima1")
    self.leLayoutKalima1.setGeometry(QRect(191,96,238,31))
    self.tabVocab.insertTab(self.tab_3,QString(""))

    self.fileNewAction = QAction(self,"fileNewAction")
    self.fileNewAction.setIconSet(QIconSet(self.image2))
    self.fileOpenAction = QAction(self,"fileOpenAction")
    self.fileOpenAction.setIconSet(QIconSet(self.image3))
    self.fileSaveAction = QAction(self,"fileSaveAction")
    self.fileSaveAction.setIconSet(QIconSet(self.image4))
    self.fileSaveAsAction = QAction(self,"fileSaveAsAction")
    self.filePrintAction = QAction(self,"filePrintAction")
    self.filePrintAction.setIconSet(QIconSet(self.image5))
    self.fileExitAction = QAction(self,"fileExitAction")
    self.editUndoAction = QAction(self,"editUndoAction")
    self.editUndoAction.setIconSet(QIconSet())
    self.editRedoAction = QAction(self,"editRedoAction")
    self.editRedoAction.setIconSet(QIconSet(self.image6))
    self.editCutAction = QAction(self,"editCutAction")
    self.editCutAction.setIconSet(QIconSet())
    self.editCopyAction = QAction(self,"editCopyAction")
    self.editCopyAction.setIconSet(QIconSet(self.image7))
    self.editPasteAction = QAction(self,"editPasteAction")
    self.editPasteAction.setIconSet(QIconSet(self.image8))
    self.editFindAction = QAction(self,"editFindAction")
    self.editFindAction.setIconSet(QIconSet(self.image9))
    self.helpContentsAction = QAction(self,"helpContentsAction")
    self.helpIndexAction = QAction(self,"helpIndexAction")
    self.helpAboutAction = QAction(self,"helpAboutAction")
    self.fileBooks = QAction(self,"fileBooks")
    self.filePreferences = QAction(self,"filePreferences")
    self.fileSearchAction = QAction(self,"fileSearchAction")
    self.fileSearchAction.setIconSet(QIconSet(self.image9))


    self.toolBar = QToolBar(QString(""),self,Qt.DockTop)

    self.fileSaveAction.addTo(self.toolBar)
    self.filePrintAction.addTo(self.toolBar)
    self.editFindAction.addTo(self.toolBar)


    self.menubar = QMenuBar(self,"menubar")

    self.menubar.setGeometry(QRect(0,0,743,28))

    self.fileMenu = QPopupMenu(self)
    self.fileSaveAction.addTo(self.fileMenu)
    self.fileBooks.addTo(self.fileMenu)
    self.filePreferences.addTo(self.fileMenu)
    self.fileMenu.insertSeparator()
    self.filePrintAction.addTo(self.fileMenu)
    self.fileSearchAction.addTo(self.fileMenu)
    self.fileMenu.insertSeparator()
    self.fileExitAction.addTo(self.fileMenu)
    self.menubar.insertItem(QString(""),self.fileMenu,2)

    self.editMenu = QPopupMenu(self)
    self.editUndoAction.addTo(self.editMenu)
    self.editRedoAction.addTo(self.editMenu)
    self.editMenu.insertSeparator()
    self.editCutAction.addTo(self.editMenu)
    self.editCopyAction.addTo(self.editMenu)
    self.editPasteAction.addTo(self.editMenu)
    self.editMenu.insertSeparator()
    self.editFindAction.addTo(self.editMenu)
    self.menubar.insertItem(QString(""),self.editMenu,3)

    self.helpMenu = QPopupMenu(self)
    self.helpContentsAction.addTo(self.helpMenu)
    self.helpIndexAction.addTo(self.helpMenu)
    self.helpMenu.insertSeparator()
    self.helpAboutAction.addTo(self.helpMenu)
    self.menubar.insertItem(QString(""),self.helpMenu,4)


    self.languageChange()

    self.resize(QSize(743,662).expandedTo(self.minimumSizeHint()))
    self.clearWState(Qt.WState_Polished)

    self.connect(self.fileNewAction,SIGNAL("activated()"),self.fileNew)
    self.connect(self.fileOpenAction,SIGNAL("activated()"),self.fileOpen)
    self.connect(self.fileSaveAction,SIGNAL("activated()"),self.fileSave)
    self.connect(self.fileSaveAsAction,SIGNAL("activated()"),self.fileSaveAs)
    self.connect(self.filePrintAction,SIGNAL("activated()"),self.filePrint)
    self.connect(self.fileExitAction,SIGNAL("activated()"),self.fileExit)
    self.connect(self.editUndoAction,SIGNAL("activated()"),self.editUndo)
    self.connect(self.editRedoAction,SIGNAL("activated()"),self.editRedo)
    self.connect(self.editCutAction,SIGNAL("activated()"),self.editCut)
    self.connect(self.editCopyAction,SIGNAL("activated()"),self.editCopy)
    self.connect(self.editPasteAction,SIGNAL("activated()"),self.editPaste)
    self.connect(self.editFindAction,SIGNAL("activated()"),self.editFind)
    self.connect(self.helpIndexAction,SIGNAL("activated()"),self.helpIndex)
    self.connect(self.helpContentsAction,SIGNAL("activated()"),self.helpContents)
    self.connect(self.helpAboutAction,SIGNAL("activated()"),self.helpAbout)
    self.connect(self.pbFirst,SIGNAL("clicked()"),self.kalimaFirst)
    self.connect(self.pbLast,SIGNAL("clicked()"),self.kalimaLast)
    self.connect(self.pbPrevious,SIGNAL("clicked()"),self.kalimaPrevious)
    self.connect(self.pbNext,SIGNAL("clicked()"),self.kalimaNext)
    self.connect(self.pbClose,SIGNAL("clicked()"),self.mainClose)
    self.connect(self.pbSearch,SIGNAL("clicked()"),self.kalimaSearch)
    self.connect(self.rbReviseArabic,SIGNAL("clicked()"),self.rbReviseArabic_clicked)
    self.connect(self.rbReviseEnglish,SIGNAL("clicked()"),self.rbReviseEnglish_clicked)
    self.connect(self.rbShowBoth,SIGNAL("clicked()"),self.rbShowBoth_clicked)
    self.connect(self.pbReveal,SIGNAL("clicked()"),self.pbReveal_clicked)
    self.connect(self.cmbOrderBy,SIGNAL("highlighted(const QString&)"),self.cmbOrderBy_highlighted)
    self.connect(self.cmbOrderBy,SIGNAL("activated(const QString&)"),self.cmbOrderBy_activated)
    self.connect(self.pbUnicode,SIGNAL("clicked()"),self.pbUnicode_clicked)
    self.connect(self.filePreferences,SIGNAL("activated()"),self.filePreferences_activated)
    self.connect(self.fileBooks,SIGNAL("activated()"),self.fileBooks_activated)
    self.connect(self.pbAddSection,SIGNAL("clicked()"),self.pbAddSection_clicked)
    self.connect(self.pbDeleteSection,SIGNAL("clicked()"),self.pbDeleteSection_clicked)
    self.connect(self.lvSections,SIGNAL("selectionChanged(QListViewItem*)"),self.lvSections_selectionChanged)
    self.connect(self.pbAddToSection,SIGNAL("clicked()"),self.pbAddToSection_clicked)
    self.connect(self.pbRemoveFromSection,SIGNAL("clicked()"),self.pbRemoveFromSection_clicked)
    self.connect(self.pbAdd,SIGNAL("clicked()"),self.pbAdd_clicked)
    self.connect(self.pbDelete,SIGNAL("clicked()"),self.pbDelete_clicked)
    self.connect(self.fileSearchAction,SIGNAL("activated()"),self.kalimaSearch)

    self.setTabOrder(self.leJidhr1,self.leJidhr2)
    self.setTabOrder(self.leJidhr2,self.leJidhr3)
    self.setTabOrder(self.leJidhr3,self.leJidhr4)
    self.setTabOrder(self.leJidhr4,self.leIsmS)
    self.setTabOrder(self.leIsmS,self.leIsmP)
    self.setTabOrder(self.leIsmP,self.leFilMa)
    self.setTabOrder(self.leFilMa,self.leFilMu)
    self.setTabOrder(self.leFilMu,self.leMasdar)
    self.setTabOrder(self.leMasdar,self.leHarf)
    self.setTabOrder(self.leHarf,self.leMeaning)
    self.setTabOrder(self.leMeaning,self.leExample)
    self.setTabOrder(self.leExample,self.rbReviseArabic)
    self.setTabOrder(self.rbReviseArabic,self.rbReviseEnglish)
    self.setTabOrder(self.rbReviseEnglish,self.rbShowBoth)
    self.setTabOrder(self.rbShowBoth,self.pbAdd)
    self.setTabOrder(self.pbAdd,self.pbDelete)
    self.setTabOrder(self.pbDelete,self.pbExtraRevision)
    self.setTabOrder(self.pbExtraRevision,self.lbBooks)
    self.setTabOrder(self.lbBooks,self.pbFirst)
    self.setTabOrder(self.pbFirst,self.pbLast)
    self.setTabOrder(self.pbLast,self.pbPrevious)
    self.setTabOrder(self.pbPrevious,self.pbNext)
    self.setTabOrder(self.pbNext,self.pbReveal)
    self.setTabOrder(self.pbReveal,self.pbSearch)
    self.setTabOrder(self.pbSearch,self.cmbOrderBy)
    self.setTabOrder(self.cmbOrderBy,self.pbUnicode)
    self.setTabOrder(self.pbUnicode,self.tabVocab)
    self.setTabOrder(self.tabVocab,self.pbClose)
    self.setTabOrder(self.pbClose,self.leId)
    self.setTabOrder(self.leId,self.lblId)
    self.setTabOrder(self.lblId,self.lblJidhr)
    self.setTabOrder(self.lblJidhr,self.lblIsmS)
    self.setTabOrder(self.lblIsmS,self.lblIsmP)
    self.setTabOrder(self.lblIsmP,self.lblMasdar)
    self.setTabOrder(self.lblMasdar,self.lblFilMa)
    self.setTabOrder(self.lblFilMa,self.lblFilMu)
    self.setTabOrder(self.lblFilMu,self.lblMeaning)
    self.setTabOrder(self.lblMeaning,self.lblExample)
    self.setTabOrder(self.lblExample,self.cbPubPrint1)
    self.setTabOrder(self.cbPubPrint1,self.cbPubPrint2)
    self.setTabOrder(self.cbPubPrint2,self.pbAddSection)
    self.setTabOrder(self.pbAddSection,self.pbDeleteSection)
    self.setTabOrder(self.pbDeleteSection,self.leSectionName)
    self.setTabOrder(self.leSectionName,self.pbAddToSection)
    self.setTabOrder(self.pbAddToSection,self.pbRemoveFromSection)
    self.setTabOrder(self.pbRemoveFromSection,self.lbSectionWords)
    self.setTabOrder(self.lbSectionWords,self.lvSections)
    self.setTabOrder(self.lvSections,self.leLayoutSectionName)


  def languageChange(self):
    self.setCaption(self.__tr("Vocabulary Database"))
    self.lblOrderBy.setText(self.__tr("Order By"))
    self.pbFirst.setText(self.__tr("&First"))
    self.pbLast.setText(self.__tr("&Last"))
    self.pbReveal.setText(self.__tr("&Reveal"))
    QToolTip.add(self.pbReveal,self.__tr("Reveal meaning/arabic"))
    self.pbSearch.setText(self.__tr("&Search"))
    self.cmbOrderBy.clear()
    self.cmbOrderBy.insertItem(self.__tr("Id"))
    self.cmbOrderBy.insertItem(self.__tr("Kalima"))
    self.cmbOrderBy.insertItem(self.__tr("Meaning"))
    self.cmbOrderBy.insertItem(self.__tr("Jidhr"))
    self.pbNext.setText(self.__tr("&Next"))
    self.pbPrevious.setText(self.__tr("&Previous"))
    self.pbClose.setText(self.__tr("&Close"))
    self.pbUnicode.setText(self.__tr("Unicode?"))
    self.lblId.setText(self.__tr("Id"))
    self.lblJidhr.setText(self.__tr("Jidhr"))
    self.lblFilMu.setText(self.__tr("Mudari`"))
    self.lblFilMa.setText(self.__tr("Madi"))
    self.lblHarf.setText(self.__tr("Harf"))
    self.lblMeaning.setText(self.__tr("Meaning"))
    self.lblExample.setText(self.__tr("Example"))
    self.lblMasdar.setText(self.__tr("Masdar"))
    self.lblIsmP.setText(self.__tr("Ism P"))
    self.lblIsmS.setText(self.__tr("Ism S"))
    self.pbAdd.setText(self.__tr("&Add"))
    self.pbAdd.setAccel(self.__tr("Alt+A"))
    self.pbExtraRevision.setText(self.__tr("&Extra Revision"))
    self.pbExtraRevision.setAccel(self.__tr("Alt+E"))
    QToolTip.add(self.pbExtraRevision,self.__tr("Extra revision"))
    self.pbDelete.setText(self.__tr("&Delete"))
    self.pbDelete.setAccel(self.__tr("Alt+D"))
    self.lbBooks.clear()
    self.lbBooks.insertItem(self.__tr("QiSaS"))
    self.lbBooks.insertItem(self.__tr("Ghunya"))
    self.lbBooks.insertItem(self.__tr("raHeeq"))
    self.lbBooks.insertItem(self.__tr("minhaaj"))
    self.bgRevision.setTitle(QString.null)
    self.rbReviseArabic.setText(self.__tr("Revise Arabic"))
    self.rbShowBoth.setText(self.__tr("Show Both"))
    self.rbReviseEnglish.setText(self.__tr("Revise English"))
    self.checkBox3.setText(self.__tr("Revise again"))
    self.tabVocab.changeTab(self.tab,self.__tr("Enter/Revise"))
    self.textLabel1.setText(self.__tr("Kalima"))
    self.cbPubPrint1.setText(self.__tr("Print"))
    self.cbPubPrint2.setText(self.__tr("Print"))
    self.pbAddSection.setText(self.__tr("&New Section"))
    self.pbDeleteSection.setText(self.__tr("Delete Section"))
    self.pbAddToSection.setText(self.__tr("&Add to Section"))
    self.pbRemoveFromSection.setText(self.__tr("&Remove From Section"))
    self.lvSections.header().setLabel(0,self.__tr("Section"))
    self.tabVocab.changeTab(self.tab_2,self.__tr("Sections"))
    self.lblInformDND.setText(self.__tr("drag and drop each word to its correct position"))
    self.tabVocab.changeTab(self.tab_3,self.__tr("Section Layout"))
    self.fileNewAction.setText(self.__tr("New"))
    self.fileNewAction.setMenuText(self.__tr("&New"))
    self.fileNewAction.setAccel(self.__tr("Ctrl+N"))
    self.fileOpenAction.setText(self.__tr("Open"))
    self.fileOpenAction.setMenuText(self.__tr("&Open..."))
    self.fileOpenAction.setAccel(self.__tr("Ctrl+O"))
    self.fileSaveAction.setText(self.__tr("Save"))
    self.fileSaveAction.setMenuText(self.__tr("&Save"))
    self.fileSaveAction.setAccel(self.__tr("Ctrl+S"))
    self.fileSaveAsAction.setText(self.__tr("Save As"))
    self.fileSaveAsAction.setMenuText(self.__tr("Save &As..."))
    self.fileSaveAsAction.setAccel(QString.null)
    self.filePrintAction.setText(self.__tr("Print"))
    self.filePrintAction.setMenuText(self.__tr("&Print..."))
    self.filePrintAction.setAccel(self.__tr("Ctrl+P"))
    self.fileExitAction.setText(self.__tr("Exit"))
    self.fileExitAction.setMenuText(self.__tr("E&xit"))
    self.fileExitAction.setAccel(QString.null)
    self.editUndoAction.setText(self.__tr("Undo"))
    self.editUndoAction.setMenuText(self.__tr("&Undo"))
    self.editUndoAction.setAccel(self.__tr("Ctrl+Z"))
    self.editRedoAction.setText(self.__tr("Redo"))
    self.editRedoAction.setMenuText(self.__tr("&Redo"))
    self.editRedoAction.setAccel(self.__tr("Ctrl+Y"))
    self.editCutAction.setText(self.__tr("Cut"))
    self.editCutAction.setMenuText(self.__tr("&Cut"))
    self.editCutAction.setAccel(self.__tr("Ctrl+X"))
    self.editCopyAction.setText(self.__tr("Copy"))
    self.editCopyAction.setMenuText(self.__tr("C&opy"))
    self.editCopyAction.setAccel(self.__tr("Ctrl+C"))
    self.editPasteAction.setText(self.__tr("Paste"))
    self.editPasteAction.setMenuText(self.__tr("&Paste"))
    self.editPasteAction.setAccel(self.__tr("Ctrl+V"))
    self.editFindAction.setText(self.__tr("Find"))
    self.editFindAction.setMenuText(self.__tr("&Find..."))
    self.editFindAction.setAccel(self.__tr("Ctrl+F"))
    self.helpContentsAction.setText(self.__tr("Contents"))
    self.helpContentsAction.setMenuText(self.__tr("&Contents..."))
    self.helpContentsAction.setAccel(QString.null)
    self.helpIndexAction.setText(self.__tr("Index"))
    self.helpIndexAction.setMenuText(self.__tr("&Index..."))
    self.helpIndexAction.setAccel(QString.null)
    self.helpAboutAction.setText(self.__tr("About"))
    self.helpAboutAction.setMenuText(self.__tr("&About"))
    self.helpAboutAction.setAccel(QString.null)
    self.fileBooks.setText(self.__tr("Books..."))
    self.fileBooks.setMenuText(self.__tr("Books..."))
    self.filePreferences.setText(self.__tr("Preferences..."))
    self.filePreferences.setMenuText(self.__tr("Preferences..."))
    self.fileSearchAction.setText(self.__tr("Search..."))
    self.fileSearchAction.setMenuText(self.__tr("Search..."))
    self.toolBar.setLabel(self.__tr("Tools"))
    if self.menubar.findItem(2):
      self.menubar.findItem(2).setText(self.__tr("&File"))
    if self.menubar.findItem(3):
      self.menubar.findItem(3).setText(self.__tr("&Edit"))
    if self.menubar.findItem(4):
      self.menubar.findItem(4).setText(self.__tr("&Help"))


  def fileNew(self):
    print("MainEntry.fileNew(): Not implemented yet")
  def fileOpen(self):
    print("MainEntry.fileOpen(): Not implemented yet")
  def fileSave(self):
    print("MainEntry.fileSave(): Not implemented yet")
  def fileSaveAs(self):
    print("MainEntry.fileSaveAs(): Not implemented yet")
  def filePrint(self):
    print("MainEntry.filePrint(): Not implemented yet")
  def fileExit(self):
    print("MainEntry.fileExit(): Not implemented yet")
  def editUndo(self):
    print("MainEntry.editUndo(): Not implemented yet")
  def editRedo(self):
    print("MainEntry.editRedo(): Not implemented yet")
  def editCut(self):
    print("MainEntry.editCut(): Not implemented yet")
  def editCopy(self):
    print("MainEntry.editCopy(): Not implemented yet")
  def editPaste(self):
    print("MainEntry.editPaste(): Not implemented yet")
  def editFind(self):
    print("MainEntry.editFind(): Not implemented yet")
  def helpIndex(self):
    print("MainEntry.helpIndex(): Not implemented yet")
  def helpContents(self):
    print("MainEntry.helpContents(): Not implemented yet")
  def helpAbout(self):
    print("MainEntry.helpAbout(): Not implemented yet")
  def kalimaFirst(self):
    print("MainEntry.kalimaFirst(): Not implemented yet")
  def kalimaLast(self):
    print("MainEntry.kalimaLast(): Not implemented yet")
  def kalimaPrevious(self):
    print("MainEntry.kalimaPrevious(): Not implemented yet")
  def kalimaNext(self):
    print("MainEntry.kalimaNext(): Not implemented yet")
  def pbClose_clicked(self):
    print("MainEntry.pbClose_clicked(): Not implemented yet")
  def mainClose(self):
    print("MainEntry.mainClose(): Not implemented yet")
  def kalimaAdd(self):
    print("MainEntry.kalimaAdd(): Not implemented yet")
  def kalimaDelete(self):
    print("MainEntry.kalimaDelete(): Not implemented yet")
  def kalimaSearch(self):
    print("MainEntry.kalimaSearch(): Not implemented yet")
  def rbReviseArabic_clicked(self):
    print("MainEntry.rbReviseArabic_clicked(): Not implemented yet")
  def rbReviseEnglish_clicked(self):
    print("MainEntry.rbReviseEnglish_clicked(): Not implemented yet")
  def rbShowBoth_clicked(self):
    print("MainEntry.rbShowBoth_clicked(): Not implemented yet")
  def pbReveal_clicked(self):
    print("MainEntry.pbReveal_clicked(): Not implemented yet")
  def cmbOrderBy_highlighted(self,a0):
    print("MainEntry.cmbOrderBy_highlighted(const QString&): Not implemented yet")
  def cmbOrderBy_activated(self,a0):
    print("MainEntry.cmbOrderBy_activated(const QString&): Not implemented yet")
  def pbUnicode_clicked(self):
    print("MainEntry.pbUnicode_clicked(): Not implemented yet")
  def filePreferences_activated(self):
    print("MainEntry.filePreferences_activated(): Not implemented yet")
  def fileBooks_activated(self):
    print("MainEntry.fileBooks_activated(): Not implemented yet")
  def pbAddSection_clicked(self):
    print("MainEntry.pbAddSection_clicked(): Not implemented yet")
  def pbDeleteSection_clicked(self):
    print("MainEntry.pbDeleteSection_clicked(): Not implemented yet")
  def lvSectionView_selectionChanged(self,a0):
    print("MainEntry.lvSectionView_selectionChanged(QListViewItem*): Not implemented yet")
  def lvSections_selectionChanged(self,a0):
    print("MainEntry.lvSections_selectionChanged(QListViewItem*): Not implemented yet")
  def pbAddToSection_clicked(self):
    print("MainEntry.pbAddToSection_clicked(): Not implemented yet")
  def pbRemoveFromSection_clicked(self):
    print("MainEntry.pbRemoveFromSection_clicked(): Not implemented yet")
  def pbAdd_clicked(self):
    print("MainEntry.pbAdd_clicked(): Not implemented yet")
  def pbDelete_clicked(self):
    print("MainEntry.pbDelete_clicked(): Not implemented yet")
  def __tr(self,s,c = None):
    return qApp.translate("MainEntry",s,c)
