""" American Football pitch dimensions. """

from dataclasses import dataclass
from typing import Optional

import numpy as np

from .._dimensions_base import BaseDims


valid = ['statsbomb']
size_varies = []


@dataclass
class BaseAmericanFootballDims(BaseDims):
    """ Base dataclass to hold American Football dimensions."""
    boundary_left: float
    boundary_right: float
    boundary_bottom: float
    boundary_top: float
    goal_line_left: float
    goal_line_right: float
    yard_line_minor_size: float
    yard_number_bottom: float # verticalalignment='bottom'
    yard_number_top: float # verticalalignment='top'
    conversion_left: float
    conversion_right: float
    conversion_size: float
    hash_mark_bottom_start: float
    hash_mark_bottom_end: float
    hash_mark_top_start: float
    hash_mark_top_end: float
    hash_mark_size: float
    goal_bottom: float
    goal_top: float
    number_marks: Optional[np.array] = None
    yard_lines_major: Optional[np.array] = None
    yard_lines_minor: Optional[np.array] = None

    def __post_init__(self):
        if self.invert_y:
            self.pitch_extent = np.array([self.left, self.right, self.top, self.bottom])
        else:
            self.pitch_extent = np.array([self.left, self.right, self.bottom, self.top])
        self.standardized_extent = np.array([0, 120, 0, 53.33])
        yard_lines = np.linspace(self.goal_line_left, self.goal_line_right, 101)
        self.number_marks = yard_lines[np.mod(yard_lines, 10) == 0][1:-1]
        self.yard_lines_minor = yard_lines[np.mod(yard_lines, 5) != 0]
        self.yard_lines_major = yard_lines[np.mod(yard_lines, 5) == 0][1:-1]


def statsbomb_dims():
    """ Create 'statsbomb dimensions."""
    return BaseAmericanFootballDims(left=-10, right=110, bottom=53.33, top=0,
                                    boundary_left=-12,
                                    boundary_right=112,
                                    boundary_bottom=55.33,
                                    boundary_top=-2,
                                    pitch_width=53.33, pitch_length=120,
                                    width=53.33, length=120,
                                    invert_y=True, origin_center=False,
                                    aspect=1, aspect_equal=True,
                                    pad_default=4, pad_multiplier=1,
                                    center_width=26.67, center_length=50,
                                    goal_line_left=0, goal_line_right=100,
                                    goal_bottom=26.67+18.5/3,
                                    goal_top=26.67-18.5/3,
                                    yard_number_top=10, yard_number_bottom=43.33,
                                    hash_mark_bottom_start=53.33-8/36,
                                    hash_mark_bottom_end=53.33-32/36,
                                    hash_mark_top_start=8/36,
                                    hash_mark_top_end=32/36,
                                    yard_line_minor_size=2/3, hash_mark_size=2/3,
                                    conversion_left=2, conversion_right=98, conversion_size=3,
                                   )


def create_pitch_dims(pitch_type, pitch_width=None, pitch_length=None):
    """ Create pitch dimensions.

    Parameters
    ----------
    pitch_type : str
        The pitch type used in the plot.
        The supported pitch types are: 'statsbomb'.
    pitch_length : float, default None
        The pitch length in yards. Not used.
    pitch_width : float, default None
        The pitch width in yards. Not used.

    Returns
    -------
    dataclass
        A dataclass holding the pitch dimensions.
    """
    if pitch_type == 'statsbomb':
        return statsbomb_dims()
