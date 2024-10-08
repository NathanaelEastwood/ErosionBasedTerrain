import random
from math import sqrt

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d.axes3d as axes3d
from typing import List
mpl.use("Qt5Agg")


class TerrainPoint:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

class ErosionBasedTerrain:

    def __init__(self, x_length: int, y_length: int, z_length: int, max_peaks: int):
        self.x_length = x_length
        self.y_length = y_length
        self.z_length = z_length
        self.max_peaks = max_peaks

    def generate(self) -> List[TerrainPoint]:
        this = "that"
    def renderLandscape(self, input_data: List[TerrainPoint]):
        terrain_points = self.generateBaseLandscape()

        # Extract x, y, z values
        x_values = np.array([point.x for point in terrain_points])
        y_values = np.array([point.y for point in terrain_points])
        z_values = np.array([point.z for point in terrain_points])

        # Create 2D meshgrid from x_values and y_values
        x_grid, y_grid = np.meshgrid(np.unique(x_values), np.unique(y_values))

        # We assume that z_values are organized in a regular grid corresponding to x_grid and y_grid
        z_grid = np.zeros_like(x_grid)

        # Reorganize z_values into a grid, assuming terrain_points are ordered in a regular grid
        for i, x in enumerate(np.unique(x_values)):
            for j, y in enumerate(np.unique(y_values)):
                # Find the corresponding z value
                idx = (x_values == x) & (y_values == y)
                z_grid[j, i] = z_values[idx][0]  # Assuming there's one z for each (x, y)

        plt.figure(dpi=1200)
        # Set up the 3D plot
        fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))

        # Plot the surface
        ax.plot_surface(x_grid, y_grid, z_grid, cmap=plt.get_cmap('jet'))
        ax.view_init(azim=45, elev=30)
        plt.savefig('filename.pdf')
        plt.show()

    def generateBaseLandscape(self) -> List[TerrainPoint]:
        result = []
        short_side = self.y_length if self.y_length < self.x_length else self.x_length
        peaks = self.generateHighPoints(short_side)
        peaks.append(TerrainPoint(0, 0, 0))
        peaks.append(TerrainPoint(self.x_length, self.y_length, 0))
        for x in range(0, self.x_length):
            for y in range(0, self.y_length):
                current_point = TerrainPoint(x, y, 0)
                closest_points = self.getNClosestPointsFromList(2, current_point, peaks)
                current_point = self.getPointBetweenPoints(closest_points[0], closest_points[1], current_point)
                result.append(current_point)

        return result

    def erode(self, terrain: List[TerrainPoint]) -> List[TerrainPoint]:
        this = "that"

    def generateHighPoints(self, short_side_length: int) -> List[TerrainPoint]:
        edge_distance = 10
        peak_height = self.z_length if self.z_length < short_side_length/3 else short_side_length/3
        result = []
        for i in range(self.max_peaks):
            newPeak = self.generateRandomPoint((0+edge_distance), (self.x_length - edge_distance), (0 - edge_distance), (self.y_length - edge_distance))
            result.append(newPeak)
        return result

    def getPointBetweenPoints(self, point_a: TerrainPoint, point_b: TerrainPoint, result_point: TerrainPoint) -> TerrainPoint:
        distance_from_a = self.getDistanceBetweenPoints(point_a, result_point)
        distance_from_b = self.getDistanceBetweenPoints(point_b, result_point)
        bias = distance_from_a / distance_from_b if distance_from_a / distance_from_b is not None else 0
        result_point.z = (distance_from_a + distance_from_b) * bias

        return result_point

    def getNClosestPointsFromList(self, n: int, search_point: TerrainPoint, list: List[TerrainPoint]) -> List[TerrainPoint]:
        sort = sorted(list, key=lambda point: self.getDistanceBetweenPoints(point, search_point), reverse=False)
        return sort[:n]

    def getDistanceBetweenPoints(self, point_a: TerrainPoint, point_b: TerrainPoint) -> float:
        x_distance = point_a.x - point_b.x
        y_distance = point_a.y - point_b.y
        return sqrt(x_distance**2 + y_distance**2)

    def generateRandomPoint(self, min_x: int, max_x, min_y, max_y) -> TerrainPoint:
        x = random.randint(abs(min_x), abs(max_x))
        y = random.randint(abs(min_y), abs(max_y))
        return TerrainPoint(x, y, 0)

