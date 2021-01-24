README.md

## Introduction to Computational Photography

Computational Photography is a way of editing and manipulating digital images using computational models.

In simple words, it gives you power of Adobe Photoshop without needing Adobe Photoshop, instead by way of coding.

Applications of Computational Photography:

- Portrait Mode on iPhone
- Panorama
- HDR


### Techniques:

1. **Minutature Faking / Syntehtic Tlt -Shift Photography** :

2. **Image Colorization** : Turn old Black & White photos into colorful photos. Reference Paper "Colorful Image Colorization" by Richard Zhang https://richzhang.github.io/colorization

3. **Image Region Removal / Synthesis** :


## Concepts

### Gradient Domain Blending

Gradient Domain Blending

    - Image Compositing : Seamless Blending of two or more images together to form a new image that looks real. Can you fool people into believing it's real ? light weight deep fake ?

        1. Source Image

        2. Source Mask

        3. Target Image

        4. Target Mask

        
Understanding Image Data : 2D grid of pixels where each pixel is composed of 3 color channels - red, blue and green. Each channel also stores an intensity from 0 to 255 or 0.0f to 1.0f. It is analogous to mixing lights together. e.g Black = rgb(0,0,0) ; White = rgb(255, 255, 255)


Representation of Image Data using Lists/Arrays between these two systems

- Cordinate System : Top Left is [0, 0]. 

- 1 Dimensional Linearized Indices : [0, 1, 2, 3, ......] 



Image Gradients: Gradient is the change in intentisity (color) from one pixel to the next. It can happen in either top-down (y-axis) direction or left-right (x-axis) direction or in both directions at the same time to create a circular gradient.

Change in gradient / color is usually at the edges of objects.


Optimization : Optimize the blending of masked region background to match the target region background pixel by pixel. Optimization is rarely perfect so error in color gets evenly distributed inside the mask.


**Can we blend videos using this approach?** Yes, but it involves dealing with Temporal Consistency

## Acknowledgement:

Special thanks for Vivian for her tutorial on Computational Photography at virtual CCFest 2021. (https://inst.eecs.berkeley.edu/~cs194-26/fa18/upload/files/proj3/cs194-26-afd/)