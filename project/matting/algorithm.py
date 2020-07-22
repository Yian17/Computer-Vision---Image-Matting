## CSC320 Winter 2018
## Assignment 1
## (c) Kyros Kutulakos
##
## DISTRIBUTION OF THIS CODE ANY FORM (ELECTRONIC OR OTHERWISE,
## AS-IS, MODIFIED OR IN PART), WITHOUT PRIOR WRITTEN AUTHORIZATION
## BY THE INSTRUCTOR IS STRICTLY PROHIBITED. VIOLATION OF THIS
## POLICY WILL BE CONSIDERED AN ACT OF ACADEMIC DISHONESTY

##
## DO NOT MODIFY THIS FILE ANYWHERE EXCEPT WHERE INDICATED
##

# import basic packages
import numpy as np
import scipy.linalg as sp
import cv2 as cv

# If you wish to import any additional modules
# or define other utility functions,
# include them here

#########################################
## PLACE YOUR CODE BETWEEN THESE LINES ##
#########################################

#########################################





#
# The Matting Class
#
# This class contains all methods required for implementing
# triangulation matting and image compositing. Description of
# the individual methods is given below.
#
# To run triangulation matting you must create an instance
# of this class. See function run() in file run.py for an
# example of how it is called
#
class Matting:
    #
    # The class constructor
    #
    # When called, it creates a private dictionary object that acts as a container
    # for all input and all output images of the triangulation matting and compositing
    # algorithms. These images are initialized to None and populated/accessed by
    # calling the the readImage(), writeImage(), useTriangulationResults() methods.
    # See function run() in run.py for examples of their usage.
    #
    def __init__(self):
        self._images = {
            'backA': None,
            'backB': None,
            'compA': None,
            'compB': None,
            'colOut': None,
            'alphaOut': None,
            'backIn': None,
            'colIn': None,
            'alphaIn': None,
            'compOut': None,
        }

    # Return a dictionary containing the input arguments of the
    # triangulation matting algorithm, along with a brief explanation
    # and a default filename (or None)
    # This dictionary is used to create the command-line arguments
    # required by the algorithm. See the parseArguments() function
    # run.py for examples of its usage
    def mattingInput(self):
        return {
            'backA':{'msg':'Image filename for Background A Color','default':None},
            'backB':{'msg':'Image filename for Background B Color','default':None},
            'compA':{'msg':'Image filename for Composite A Color','default':None},
            'compB':{'msg':'Image filename for Composite B Color','default':None},
        }
    # Same as above, but for the output arguments
    def mattingOutput(self):
        return {
            'colOut':{'msg':'Image filename for Object Color','default':['color.tif']},
            'alphaOut':{'msg':'Image filename for Object Alpha','default':['alpha.tif']}
        }
    def compositingInput(self):
        return {
            'colIn':{'msg':'Image filename for Object Color','default':None},
            'alphaIn':{'msg':'Image filename for Object Alpha','default':None},
            'backIn':{'msg':'Image filename for Background Color','default':None},
        }
    def compositingOutput(self):
        return {
            'compOut':{'msg':'Image filename for Composite Color','default':['comp.tif']},
        }

    # Copy the output of the triangulation matting algorithm (i.e., the
    # object Color and object Alpha images) to the images holding the input
    # to the compositing algorithm. This way we can do compositing right after
    # triangulation matting without having to save the object Color and object
    # Alpha images to disk. This routine is NOT used for partA of the assignment.
    def useTriangulationResults(self):
        if (self._images['colOut'] is not None) and (self._images['alphaOut'] is not None):
            self._images['colIn'] = self._images['colOut'].copy()
            self._images['alphaIn'] = self._images['alphaOut'].copy()

    # If you wish to create additional methods for the
    # Matting class, include them here

    #########################################
    ## PLACE YOUR CODE BETWEEN THESE LINES ##
    #########################################

    #########################################

    # Use OpenCV to read an image from a file and copy its contents to the
    # matting instance's private dictionary object. The key
    # specifies the image variable and should be one of the
    # strings in lines 54-63. See run() in run.py for examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # leave the matting instance's dictionary entry unaffected and return
    # False, along with an error message
    def readImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        msg = 'Unsuccessfuly read the image'
        img = cv.imread(fileName)
        if img is not None:
            self._images[key] = img
            success = True
            msg = 'Successfully read the image'


        #########################################
        return success, msg

    # Use OpenCV to write to a file an image that is contained in the
    # instance's private dictionary. The key specifies the which image
    # should be written and should be one of the strings in lines 54-63.
    # See run() in run.py for usage examples
    #
    # The routine should return True if it succeeded. If it did not, it should
    # return False, along with an error message
    def writeImage(self, fileName, key):
        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################
        msg = 'Unsuccessfully write to a file'
        img = self._images[key]

        if img is not None:

            cv.imwrite(fileName, img)
            msg = 'Successfully write to a file'
            success = True




        #########################################
        return success, msg

    # Method implementing the triangulation matting algorithm. The
    # method takes its inputs/outputs from the method's private dictionary
    # ojbect.
    def triangulationMatting(self):
        """
success, errorMessage = triangulationMatting(self)

        Perform triangulation matting. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
        """

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################

        msg = 'Matting inputs invalid'

        back_a = self._images['backA'].astype(np.float32)/255
        back_b = self._images['backB'].astype(np.float32)/255
        comp_a = self._images['compA'].astype(np.float32)/255
        comp_b = self._images['compB'].astype(np.float32)/255

        if not (back_a is None or back_b is None or comp_a is None or comp_b is None):
            if back_a.shape != back_b.shape or comp_a.shape != comp_b.shape or comp_a.shape != back_a.shape:
                msg = 'Size of input doesn not match!'
                return False, msg

            # build C delta = C - Ck
            delta_a = comp_a - back_a
            delta_b = comp_b - back_b

            c_delta = np.dstack((delta_a, delta_b))

            # start to build pseudo-inverse of A where Ax = C_delta

            # build identity part
            i = np.eye(3, 3)
            eye = np.vstack((i, i))

            row, col = back_a.shape[0], back_a.shape[1]
            matrix_i = np.tile(eye, (row, col, 1, 1))

            # build ck column
            col_a = back_a.reshape(row, col, 3, 1)
            col_b = back_b.reshape(row, col, 3, 1)
            col_ab = np.dstack((col_a, col_b))
            col_ab = (-1) * col_ab
            matrix_a = np.concatenate((matrix_i, col_ab), axis=3)

            colo = np.zeros(back_a.shape)
            alpha = np.zeros(back_a.shape[:2])

            for i in range(row):
                for j in range(col):
                    pixel = matrix_a[i][j]
                    sol = np.clip(np.dot(np.linalg.pinv(pixel), c_delta[i][j]), 0.0, 1.0)
                    colo[i, j] = np.array([sol[0], sol[1], sol[2]])
                    alpha[i, j] = sol[3]

            self._images['colOut'] = colo * 255
            self._images['alphaOut'] = alpha * 255

            success = True
            msg = 'successfully done matting'


        #########################################

        return success, msg


    def createComposite(self):
        """
success, errorMessage = createComposite(self)

        Perform compositing. Returns True if successful (ie.
        all inputs and outputs are valid) and False if not. When success=False
        an explanatory error message should be returned.
"""

        success = False
        msg = 'Placeholder'

        #########################################
        ## PLACE YOUR CODE BETWEEN THESE LINES ##
        #########################################

        col_in = self._images['colIn']
        back_in = self._images['backIn']
        alpha_in = self._images['alphaIn']

        msg = "Compositing input required"

        if col_in is not None and back_in is not None and alpha_in is not None:
            if col_in.shape != back_in.shape or back_in.shape != alpha_in.shape:
                msg = 'Input shape does not match'
                return False, msg

            alpha_in = alpha_in / 255.

            #C = Co + (1- a0)ck
            a_prime = 1 - alpha_in
            c = col_in + a_prime * back_in
            self._images['compOut'] = c

            msg = "Successfully composite"
            success = True



        #########################################

        return success, msg
