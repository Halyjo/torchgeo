#!/usr/bin/env python3

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import hashlib
import os

import numpy as np
import rasterio
from rasterio.crs import CRS
from rasterio.transform import Affine

SIZE = 32

np.random.seed(0)

years = [2011, 2019]

wkt = """
PROJCS["Albers Conical Equal Area",
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.0174532925199433,AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]],
    PROJECTION["Albers_Conic_Equal_Area"],
    PARAMETER["latitude_of_center",23],
    PARAMETER["longitude_of_center",-96],
    PARAMETER["standard_parallel_1",29.5],
    PARAMETER["standard_parallel_2",45.5],
    PARAMETER["false_easting",0],
    PARAMETER["false_northing",0],
    UNIT["meters",1],
    AXIS["Easting",EAST],
    AXIS["Northing",NORTH]]
"""


def create_file(path: str, dtype: str) -> None:
    """Create the testing file."""
    profile = {
        'driver': 'GTiff',
        'dtype': dtype,
        'count': 1,
        'crs': CRS.from_wkt(wkt),
        'transform': Affine(30.0, 0.0, -2493045.0, 0.0, -30.0, 3310005.0),
        'height': SIZE,
        'width': SIZE,
        'compress': 'lzw',
        'predictor': 2,
    }

    allowed_values = [0, 11, 12, 21, 22, 23, 24, 31, 41, 42, 43, 52, 71, 81, 82, 90, 95]

    Z = np.random.choice(allowed_values, size=(SIZE, SIZE))

    with rasterio.open(path, 'w', **profile) as src:
        src.write(Z, 1)


if __name__ == '__main__':
    for year in years:
        filename = os.path.join(
            'tests', 'data', 'nlcd', 'Annual_NLCD_LndCov_{}_CU_C1V0.tif'
        ).format(year)
        create_file(filename, dtype='int8')

        # Compute checksums
        with open(filename, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
            print(f'{filename}: {md5}')
