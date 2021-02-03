cpdef list pixel_coord_fast(double xres, double yres, double ulx, double uly, double[:, :] pixel_coordinates_x, double[:, :] pixel_coordinates_y):
     # set the variable extension types
     cdef double xp, yp
     cdef int x, y, 
     
     h = pixel_coordinates_x.shape[0]
     w = pixel_coordinates_x.shape[1]
     

      # loop over the image
     for y in range(0, h):
         for x in range(0, w):
             # calculate coordinate
              xp = ulx + (x * xres)
              yp = uly + (y * yres)
              pixel_coordinates_x[y, x] = xp
              pixel_coordinates_y[y, x] = yp



     # die beiden arrays stacken
     test = [pixel_coordinates_y, pixel_coordinates_x]
     return test

