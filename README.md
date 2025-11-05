# Sport Tracking

This repository contains code and resources for **multi-object tracking in sports analytics** using deep learning techniques. The project leverages *tracking-by-detection* for tracking players, referees, and the ball in football match footage.

## Overview

The tracking module aims to maintain consistent identities for all detected objects across video frames, enabling precise movement and interaction analysis. Each player and referee is assigned a unique tracking ID that persists throughout the sequence, even when they are temporarily out of view (marked as *“not visible”*).

## Dataset

The datasets are **meticulously annotated** with 2D bounding boxes for players, referees, and the ball, including consistent tracking IDs and visibility information.

