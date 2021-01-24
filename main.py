import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import lil_matrix as lil_matrix
from scipy.sparse import linalg as linalg

# Read in background and penguin images
bg = plt.imread('bg_small.jpeg')
bg_mask = plt.imread('bg_small_mask.jpeg')[:, :, 0]/255
penguin = plt.imread('penguin_small.jpeg')
penguin_mask = plt.imread('penguin_small_mask.jpeg')[:, :, 0]/255


# Convert them from integers [0, 256) to floats [0, 1).
bg = bg / 255
penguin = penguin / 255

# Display images to make sure they're correct
# plt.imshow(bg)
# plt.show()

# plt.imshow(bg_mask, cmap='gray')
# plt.show()

# plt.imshow(penguin)
# plt.show()

# plt.imshow(penguin_mask, cmap='gray')
# plt.show()

# Big Idea 1: Images as Data and Indexing into Images

# We can get the dimensions of the penguin image array
# Which will tell us the height, width, and number of channels this image has
print('Penguin dimensions are: ', penguin.shape)

# NOTE: Python stores arrays in row-major order 
# (row by row, rather than column by column.)
# The first dimension is the height of the image.
# This means we need to index using the y index first, then the x index.
# In other words, index into the penguin image using penguin[y, x]

# We can index into the first pixel of the penguin image:
print('Penguin first pixel is: ', penguin[0, 0])

# or the last pixel, using standard python list indexing notation:
print('Penguin last pixel is: ', penguin[-1, -1])

''' 
Given the mask image, return a list of x,y coordinates 
that correspond to white pixels of mask (in order)
'''
def get_mask_coords(mask):
  mask_coords = np.where(mask > 0.1)
  y_coords = mask_coords[0]
  x_coords = mask_coords[1]
  return list(list(c) for c in zip(x_coords, y_coords))

'''
Return the pixel value of image at coordinate x, y
'''
def xy_to_pixel(x, y, image):
  pixel = image[y, x]
  return pixel

def store_pixel(pixel, x, y, image):
  image[y, x] = pixel
  # return image

def img_xy_to_mask_idx(x, y, mask):
  mask_coords = np.where(mask > 0.1)
  if len(np.intersect1d(np.where(mask_coords[0] == y)[0], np.where(mask_coords[1] == x)[0])) > 0:
    return np.intersect1d(np.where(mask_coords[0] == y)[0], np.where(mask_coords[1] == x)[0])[0]
  else:
    return -1
  # mask_x = np.array(mask_coords)[:, 0]
  # mask_y = np.array(mask_coords)[:, 1]

  # if len(np.intersect1d(np.where(mask_y == y)[0], np.where(mask_x == x)[0])) > 0:
  #   return np.intersect1d(np.where(mask_y == y)[0], np.where(mask_x == x)[0])[0]
  # else:
  #   return -1

def mask_idx_to_img_xy(idx, mask_coords):
  return mask_coords[idx][0], mask_coords[idx][1]


penguin_mask_coords = get_mask_coords(penguin_mask)
bg_mask_coords = get_mask_coords(bg_mask)

print(len(penguin_mask_coords))
print(len(bg_mask_coords))


# Let's iterate through these two mask coordinate lists together
for i, penguin_mask_coord in enumerate(penguin_mask_coords):

  penguin_x = penguin_mask_coord[0]
  penguin_y = penguin_mask_coord[1]

  # print('a')
  mask_idx = img_xy_to_mask_idx(penguin_x, penguin_y, penguin_mask)
  # print('b')
  # Use the mask_idx to get the corresponding coordinate of the bg_mask

  bg_mask_coord = bg_mask_coords[mask_idx]

  bg_x = bg_mask_coord[0]
  bg_y = bg_mask_coord[1]

  penguin_pixel = xy_to_pixel(penguin_x, penguin_y, penguin)

  store_pixel(penguin_pixel, bg_x, bg_y, bg)

# What does it look like now?
# plt.imshow(bg)
# plt.show() 


def get_grad_to_right(x, y, image):
  pixel = xy_to_pixel(x, y, image)
  pixel_right = xy_to_pixel(x+1, y, image)
  return pixel - pixel_right

def get_grad_to_left(x, y, image):
  pixel = xy_to_pixel(x, y, image)
  pixel_left = xy_to_pixel(x-1, y, image)
  return pixel - pixel_left

def get_grad_to_top(x, y, image):
  pixel = xy_to_pixel(x, y, image)
  pixel_top = xy_to_pixel(x, y-1, image)
  return pixel - pixel_top

def get_grad_to_bottom(x, y, image):
  pixel = xy_to_pixel(x, y, image)
  pixel_bottom = xy_to_pixel(x, y+1, image)
  return pixel - pixel_bottom


N = len(penguin_mask_coords)
result = bg
print(N)


for c in range(3):
  A = lil_matrix((4*N,N)) # solving for N pixels using N 
  b = np.zeros((4*N))

  penguin_channel = penguin[:, :, c]
  bg_channel = bg[:, :, c]

  for i, coord in enumerate(penguin_mask_coords):

    x = coord[0]
    y = coord[1]

    above_constraint_val = get_grad_to_top(x, y, penguin_channel)
    A[i*4 + 0, i] = 1
    above_idx = img_xy_to_mask_idx(x, y-1, penguin_mask)
    if above_idx != -1:
      A[i*4 + 0, above_idx] = -1
    else:
      bg_img_x, bg_img_y = mask_idx_to_img_xy(i, bg_mask_coords)
      bg_pixel_value = xy_to_pixel(bg_img_x, bg_img_y-1, bg_channel)
      above_constraint_val += bg_pixel_value
    b[i*4 + 0] = above_constraint_val

    below_constraint_val = get_grad_to_bottom(x, y, penguin_channel)
    A[i*4 + 1, i] = 1
    below_idx = img_xy_to_mask_idx(x, y+1, penguin_mask)

    if below_idx != -1:
      A[i*4 + 1, below_idx] = -1
    else:
      bg_img_x, bg_img_y = mask_idx_to_img_xy(i, bg_mask_coords)
      print(bg_img_x)
      print(bg_img_y)
      bg_pixel_value = xy_to_pixel(bg_img_x, bg_img_y+1, bg_channel)
      below_constraint_val += bg_pixel_value
    b[i*4 + 1] = below_constraint_val

    left_constraint_val = get_grad_to_left(x, y, penguin_channel)
    A[i*4 + 2, i] = 1
    left_idx = img_xy_to_mask_idx(x-1, y, penguin_mask)
    if left_idx != -1:
      A[i*4 + 2, left_idx] = -1
    else:
      bg_img_x, bg_img_y = mask_idx_to_img_xy(i, bg_mask_coords)
      bg_pixel_value = xy_to_pixel(bg_img_x-1, bg_img_y, bg_channel)
      left_constraint_val += bg_pixel_value
    b[i*4 + 2] = left_constraint_val

    right_constraint_val = get_grad_to_right(x, y, penguin_channel)
    A[i*4 + 3, i] = 1
    right_idx = img_xy_to_mask_idx(x+1, y, penguin_mask)
    if right_idx != -1:
      A[i*4 + 3, right_idx] = -1
    else:
      bg_img_x, bg_img_y = mask_idx_to_img_xy(i, bg_mask_coords)
      bg_pixel_value = xy_to_pixel(bg_img_x+1, bg_img_y, bg_channel)
      right_constraint_val += bg_pixel_value
    b[i*4 + 3] = right_constraint_val

    
  print('Done constructing matrix for c={}'.format(c))

  v = linalg.lsmr(A,b)[0]

  print('Done solving lsqr for c={}'.format(c))

  for j, res_coord in enumerate(zip(np.where(bg_mask > .1)[0], np.where(bg_mask > .1)[1])):
    ry, rx = res_coord
    result[ry, rx, c] = v[j]

  print('Done copying values into result for c={}'.format(c))


plt.imshow(result)
plt.show()