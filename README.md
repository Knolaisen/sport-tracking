# Sport Tracking

This repository contains code and resources for **multi-object tracking in sports analytics** using deep learning techniques. The project leverages *tracking-by-detection* for tracking players, referees, and the ball in football match footage.

## Goals

- Real-time, lightweight detector + tracker\
  Build a compact model and pipeline that runs in real-time on edge hardware Prioritize low latency and small model size while keeping robust detection and identity consistency for live analytics and broadcast-assist use cases.

- High-accuracy offline model for post-game analysis\
  Develop a high-capacity detection and re-identification system optimized for maximum precision and ID persistence across heavy occlusions and long-term camera views. Target tools for detailed tactical analysis and automated event extraction.

## Overview

The tracking module aims to maintain consistent identities for all detected objects across video frames, enabling precise movement and interaction analysis. Each player and referee is assigned a unique tracking ID that persists throughout the sequence, even when they are temporarily out of view (marked as *“not visible”*).

## Dataset

The datasets are **meticulously annotated** with 2D bounding boxes for players, referees, and the ball, including consistent tracking IDs and visibility information.
