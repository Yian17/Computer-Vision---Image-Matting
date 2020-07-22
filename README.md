## Overview

This is a Computer Vision project which investigates the image matting. The program should work for a variety of image formats (tif, jpeg, etc)

## Techiniques
The technique I implemented is based on a paper by Smith and Blinn that appeared in SIGGRAPH'96.

## Tools
FLTK toolkit and FLUID, a program for interactively creating user interfaces.
Online documentation: https://www.fltk.org/documentation.php/doc-1.1/toc.html

## Algorithm
I implemented the triangulation matting algorithm.
The algorithm takes four RGB images as input (Composite 1, Background 1, Composite 2, Background 2) and produces two images as output---a grayscale Alpha Matte, and an RGB Object image.

## Report
A report which invesitgates on the performance of pictures with different conditions: https://cutt.ly/ja2FAqV
