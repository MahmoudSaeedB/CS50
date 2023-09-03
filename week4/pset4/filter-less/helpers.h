#include "bmp.h"


// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width]);

// Swap two variabls
void swap(int *x, int *y);

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width]);



// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width]);

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width]);
