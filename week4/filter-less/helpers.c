#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale

void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Go to each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Calculate the sum of values RGB channels
            int RGB_SUM = image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue;
            // Calculate the average of values of RGB channels
            float RGB_AVERAGE = (float) RGB_SUM / 3;

            // Round it to the nearest integer
            RGB_AVERAGE = round(RGB_AVERAGE);

            // Make all RGB channels equal to their average to make grey color
            image[i][j].rgbtRed = image[i][j].rgbtGreen = image[i][j].rgbtBlue = RGB_AVERAGE;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    // Go to each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Use the formula to get the correct values of RGB channels to make sepia color
            float sepiaRed = image[i][j].rgbtRed * .393 + image[i][j].rgbtGreen * .769 + 
                             image[i][j].rgbtBlue * .189;
            float sepiaGreen = image[i][j].rgbtRed * .349 + image[i][j].rgbtGreen * .686 + 
                               image[i][j].rgbtBlue * .168;
            float sepiaBlue = image[i][j].rgbtRed * .272 + image[i][j].rgbtGreen * .534 + 
                              image[i][j].rgbtBlue * .131;

            // Put new RGB values in an array.
            float *RGBT[] = {&sepiaRed, &sepiaGreen, &sepiaBlue};
            for (int k = 0; k < 3; k++)
            {
                if (*RGBT[k] > 255)
                {
                    *RGBT[k] = 255;
                }
            }

            // convert RGB values with the new ones.
            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtGreen = round(sepiaGreen);
            image[i][j].rgbtBlue = round(sepiaBlue);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])

{
    // Go to each pixel in the left side of the image
    for (int i = 0; i < height; i++)
    {

        for (int j = 0; j < width / 2; j++)
        {
            // Swap the ith pixel from the left with ith pixel from the right
            RGBTRIPLE pixel = image[i][j];

            image[i][j] = image[i][width - j - 1];

            image[i][width - j - 1] = pixel;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])

{
    // Make a copy of image
    RGBTRIPLE blur_image[height][width];

    // Go to each pixel in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)

        {
            // Make an array of 9 elements for pixels within 1 row and colomn of the pixel 
            // (forming a 3*3 square)
            RGBTRIPLE neighbor_pixels[9];

            // Number of neighbor pixels so far
            int pixel_count = 0;

            // Go to each neighbor pixel
            for (int k = 0; k < 3; k++)
            {
                for (int l = 0; l < 3; l++)
                {
                    // Row of neigbor pixel
                    int pixel_row = i - 1 + k;

                    // Colomn of neighbor pixel
                    int pixel_colomn = j - 1 + l;

                    // Make sure neighbor pixel exists in the image
                    if (pixel_row >= 0 && pixel_row < height && pixel_colomn >= 0 && 
                        pixel_colomn < width)
                    {
                        // Put neighbor pixel int the array.
                        neighbor_pixels[pixel_count] = image[pixel_row][pixel_colomn];

                        // Increase number of neighbor pixels by one
                        pixel_count++;
                    }
                }
            }
            // Declare sums of each RGB channel of neighbor pixels
            float red_sum, green_sum, blue_sum;
            red_sum = green_sum = blue_sum = 0;

            for (int k = 0; k < pixel_count; k++)
            {
                red_sum += neighbor_pixels[k].rgbtRed;
                green_sum += neighbor_pixels[k].rgbtGreen;
                blue_sum += neighbor_pixels[k].rgbtBlue;
            }

            // Calculate average of values of each RGB channel of neighbor pixels
            float red_average = red_sum / pixel_count;
            float green_average = green_sum / pixel_count;
            float blue_average = blue_sum / pixel_count;

            // // Round them to nearest integer.
            blur_image[i][j].rgbtRed = round(red_average);
            blur_image[i][j].rgbtGreen = round(green_average);
            blur_image[i][j].rgbtBlue = round(blue_average);
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = blur_image[i][j];
        }
    }

    return;
}