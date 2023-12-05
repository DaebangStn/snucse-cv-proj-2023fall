import numpy as np
import cv2

class DLT:
    def __init__(self, world_coords, image_coords):
        self._world_coords = world_coords
        self._image_coords = image_coords

    def normalize(self, nd, x):
        x = np.asarray(x)
        m, s = np.mean(x, 0), np.std(x)
        if nd == 2:
            Tr = np.array([[s, 0, m[0]], [0, s, m[1]], [0, 0, 1]])
        else:
            Tr = np.array([[s, 0, 0, m[0]], [0, s, 0, m[1]], [0, 0, s, m[2]], [0, 0, 0, 1]])
            
        Tr = np.linalg.inv(Tr)
        x = np.dot( Tr, np.concatenate( (x.T, np.ones((1,x.shape[0]))) ) )
        x = x[0:nd, :].T

        return Tr, x

    def calib(self):
        
        nd = 3
        
        # Converting all variables to numpy array
        world_coords = np.asarray(self._world_coords)
        image_coords = np.asarray(self._image_coords)

        n = world_coords.shape[0]

        # Validating the parameters:
        if image_coords.shape[0] != n:
            raise ValueError('Object (%d points) and image (%d points) have different number of points.' %(n, image_coords.shape[0]))

        if (world_coords.shape[1] != 3):
            raise ValueError('Incorrect number of coordinates (%d) for %dD DLT (it should be %d).' %(world_coords.shape[1],nd,nd))

        if (n < 6):
            raise ValueError('%dD DLT requires at least %d calibration points. Only %d points were entered.' %(nd, 2*nd, n))
            
        # Normalize the data to improve the DLT quality (DLT is dependent of the system of coordinates).
        # This is relevant when there is a considerable perspective distortion.
        # normalize: mean position at origin and mean distance equals to 1 at each direction.
        Tworld, worldn = self.normalize(nd, world_coords)
        Tuv, uvn = self.normalize(2, image_coords)

        A = []

        for i in range(n):
            x, y, z = worldn[i, 0], worldn[i, 1], worldn[i, 2]
            u, v = uvn[i, 0], uvn[i, 1]
            A.append( [x, y, z, 1, 0, 0, 0, 0, -u * x, -u * y, -u * z, -u] )
            A.append( [0, 0, 0, 0, x, y, z, 1, -v * x, -v * y, -v * z, -v] )

        # Convert A to array
        A = np.asarray(A) 

        # Find the 11 parameters:
        U, S, V = np.linalg.svd(A)

        # The parameters are in the last line of Vh and normalize them
        L = V[-1, :] / V[-1, -1]

        # Camera projection matrix
        H = L.reshape(3, nd + 1)

        # Denormalize
        # pinv: Moore-Penrose pseudo-inverse of a matrix, generalized inverse of a matrix using its SVD
        H = np.dot( np.dot( np.linalg.pinv(Tuv), H ), Tworld )
        H = H / H[-1, -1]
        
        # Intrinsic, Extrinsic parameter decomposition
        out = cv2.decomposeProjectionMatrix(H)
        K = out[0]
        R = out[1]
        T = out[2]

        # Mean error of the DLT (mean residual of the DLT transformation in units of camera coordinates):
        uv2 = np.dot( H, np.concatenate( (world_coords.T, np.ones((1, world_coords.shape[0]))) ) ) 
        uv2 = uv2 / uv2[2, :] 
        # Mean distance:
        err = np.sqrt( np.mean(np.sum( (uv2[0:2, :].T - image_coords)**2, 1)) ) 

        return H, K, R, T