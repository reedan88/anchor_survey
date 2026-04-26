#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author Andrew Reed
@brief Implementation of Art Newhall's MATLAB survey software

Coordinate system:
- All functions work with local x/y coordinates in meters, except where
  noted (dms_to_dd, latlon_to_xy, xy_to_latlon handle lat/lon in degrees)
- The local coordinate system uses a flat-earth approximation valid for
  small areas (< ~10 km)
- X-axis: East (longitude variation scaled by cos(lat))
- Y-axis: North (latitude variation)
- Earth radius: 6,371,000 m

"""
from __future__ import annotations

import numpy as np
from typing import Union, Tuple, Optional


def dms_to_dd(degrees: Union[int, float, np.ndarray], 
              minutes: Union[int, float, np.ndarray], 
              seconds: Union[int, float, np.ndarray], 
              direction: Optional[Union[str, np.ndarray]] = None) -> Union[float, np.ndarray]:
    """
    Convert degrees, minutes, seconds to decimal degrees.
    
    Parameters
    ----------
    degrees : int, float, or array-like
        Degrees component (can be negative for south/west).
    minutes : int, float, or array-like
        Minutes component.
    seconds : int, float, or array-like
        Seconds component.
    direction : str or array-like, optional
        Direction ('N', 'S' for latitude; 'E', 'W' for longitude).
        If None, uses sign of degrees to determine direction.
    
    Returns
    -------
    float or np.ndarray
        Decimal degrees. Returns scalar if all inputs are scalars.
    """
    if direction is None:
        # First, check the sign on the degrees to determine direction
        direction = np.where(np.asarray(degrees) < 0, 'S', 'W')
    # Convert inputs to numpy arrays (this also handles scalars)
    degrees = np.asarray(degrees, dtype=float)
    minutes = np.asarray(minutes, dtype=float)
    seconds = np.asarray(seconds, dtype=float)
    direction = np.asarray(direction)

    # Compute decimal degrees
    dd = degrees + minutes / 60 + seconds / 3600

    # Apply negative sign for south/west
    mask = np.isin(direction, ['S', 'W'])
    dd = np.where(mask, -dd, dd)

    # Return scalar if input was scalar
    if (np.isscalar(degrees) and np.isscalar(minutes)
            and np.isscalar(seconds) and np.isscalar(direction)):
        return float(dd)
    return dd


def latlon_to_xy(lat: Union[float, np.ndarray], 
                 lon: Union[float, np.ndarray], 
                 ref_lat: float, 
                 ref_lon: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Convert latitude and longitude to local x, y coordinates in meters
    relative to a reference latitude and longitude.
    
    Uses a flat-earth approximation valid for small areas (< ~10 km).
    
    Parameters
    ----------
    lat : float or array-like
        Latitude(s) in decimal degrees.
    lon : float or array-like
        Longitude(s) in decimal degrees.
    ref_lat : float
        Reference latitude in decimal degrees.
    ref_lon : float
        Reference longitude in decimal degrees.
    
    Returns
    -------
    x : np.ndarray
        X coordinates in meters (east from reference).
    y : np.ndarray
        Y coordinates in meters (north from reference).
    """
    # Approximate conversion factors
    R = 6371000  # Earth radius in meters
    dlat = np.radians(lat - ref_lat)
    dlon = np.radians(lon - ref_lon)
    x = R * dlon * np.cos(np.radians(ref_lat))
    y = R * dlat
    return x, y


def xy_to_latlon(x: Union[float, np.ndarray], 
                  y: Union[float, np.ndarray], 
                  ref_lat: float, 
                  ref_lon: float) -> Tuple[float, float]:
    """
    Convert local x,y coordinates back to latitude and longitude.
    
    Inverse of latlon_to_xy(). Uses flat-earth approximation.
    
    Parameters
    ----------
    x : float or array-like
        Local x coordinate(s) in meters (east from reference).
    y : float or array-like
        Local y coordinate(s) in meters (north from reference).
    ref_lat : float
        Reference latitude in decimal degrees.
    ref_lon : float
        Reference longitude in decimal degrees.
    
    Returns
    -------
    lat : float or np.ndarray
        Latitude(s) in decimal degrees.
    lon : float or np.ndarray
        Longitude(s) in decimal degrees.
    """
    R = 6371000  # Earth radius in meters
    dlat = y / R
    dlon = x / (R * np.cos(np.radians(ref_lat)))
    lat = ref_lat + np.degrees(dlat)
    lon = ref_lon + np.degrees(dlon)
    return lat, lon


def calculate_anchor_position(x: np.ndarray, 
                               y: np.ndarray, 
                               d: np.ndarray, 
                               tol: float = 0.01, 
                               max_iter: int = 100) -> Tuple[float, float, int]:
    """
    Calculate anchor position using iterative least-squares (Gauss-Newton method).
    
    Solves for the anchor position that minimizes the sum of squared residuals
    between measured horizontal ranges and distances from the estimated anchor
    to each station.
    
    Parameters
    ----------
    x : np.ndarray
        Ship/station x positions in meters.
    y : np.ndarray
        Ship/station y positions in meters.
    d : np.ndarray
        Horizontal ranges from ship to anchor in meters.
    tol : float, optional
        Tolerance for convergence in meters (default: 0.01).
    max_iter : int, optional
        Maximum number of iterations (default: 100).
    
    Returns
    -------
    xi : float
        Estimated anchor x position in meters.
    yi : float
        Estimated anchor y position in meters.
    iterations : int
        Number of iterations performed.
    """
    # Initial guess for anchor position
    xi = np.mean(x)
    yi = np.mean(y)
    xx = [1.0, 1.0]

    for iteration in range(max_iter):
        # Calculate distances from estimated anchor to ship positions
        A = [2 * (x-xi),  2 * (y-yi)]
        b = (x-xi)**2 + (y-yi)**2 - d**2

        # Solve linear system to get residuals
        xx, residuals, rank, s = np.linalg.lstsq(np.transpose(A),
                                                 b, rcond=None)

        # Update positions
        xi = xi + xx[0]
        yi = yi + xx[1]

        # Check for convergence
        if np.linalg.norm(xx) < tol:
            break

    return xi, yi, iteration


def rms_error(p: Tuple[float, float], 
            x: np.ndarray, 
            y: np.ndarray, 
            dist: np.ndarray) -> float:
    """
    Calculate the RMS error between calculated and measured distances.
    
    Parameters
    ----------
    p : tuple
        Anchor position (xi, yi) in meters.
    x : np.ndarray
        Station x positions in meters.
    y : np.ndarray
        Station y positions in meters.
    dist : np.ndarray
        Measured distances from stations to anchor in meters.
    
    Returns
    -------
    float
        Root mean square error in meters.
    """
    xi, yi = p
    r = np.sqrt((x - xi)**2 + (y - yi)**2)
    return np.sqrt(np.mean((r - dist)**2))


def calculate_fallback(anchor_x: float, 
                        anchor_y: float, 
                        drop_x: float, 
                        drop_y: float) -> float:
    """
    Calculate the fallback distance from the drop position
    to the surveyed anchor position.
    
    Parameters
    ----------
    anchor_x : float
        Anchor x position in meters (local coordinates).
    anchor_y : float
        Anchor y position in meters (local coordinates).
    drop_x : float
        Drop point x position in meters (local coordinates).
    drop_y : float
        Drop point y position in meters (local coordinates).
    
    Returns
    -------
    float
        Fallback distance in meters.
    """
    fallback = np.sqrt((anchor_x - drop_x)**2 + (anchor_y - drop_y)**2)
    return fallback


def validate_survey_input(x: np.ndarray, y: np.ndarray, d: np.ndarray) -> None:
    """
    Validate survey input data for anchor position calculation.
    
    Parameters
    ----------
    x : np.ndarray
        Station x positions in meters.
    y : np.ndarray
        Station y positions in meters.
    d : np.ndarray
        Horizontal ranges in meters.
    
    Raises
    ------
    ValueError
        If input data is invalid or insufficient.
    """
    if len(x) < 3:
        raise ValueError("At least 3 stations are required for triangulation")
    
    if len(x) != len(y) or len(x) != len(d):
        raise ValueError("x, y, and d arrays must have the same length")
    
    if np.any(d <= 0):
        raise ValueError("All horizontal ranges must be positive")
    
    # Check for degenerate geometry (collinear stations)
    if len(x) >= 3:
        # Simple check: if all stations are nearly collinear
        # (area of triangle is near zero)
        area = 0.5 * abs(x[0]*(y[1]-y[2]) + x[1]*(y[2]-y[0]) + x[2]*(y[0]-y[1]))
        if area < 1.0:  # Less than 1 square meter
            import warnings
            warnings.warn("Stations appear to be nearly collinear. Results may be unreliable.")
