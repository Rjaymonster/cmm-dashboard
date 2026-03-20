------------------------------------------------------------------------------------------
28-Jan-2026 03:30                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3802    0.3850   -0.0050   +0.0050   -0.0048 *--+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3478    0.3500   -0.0050   +0.0050   -0.0022 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3042    0.3090   -0.0050   +0.0000   -0.0048 *--+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2079    0.2100                       -0.0021
Z-axis                 -2.5482   -2.5510                        0.0028
TruePosition2D          0.0070                        0.0098              +-*-
Diameter                0.1583    0.1575   -0.0010   +0.0010    0.0008 ---+-*-
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4315    0.4400                       -0.0085
Y-axis                 -0.0865   -0.0842                       -0.0023
TruePosition2D          0.0177                        0.0156              +-->      0.0020
Diameter                0.1346    0.1360   -0.0050   +0.0050   -0.0014 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4022    3.4060   -0.0050   +0.0050   -0.0038 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2460    0.2500   -0.0050   +0.0050   -0.0040 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3120    0.3140   -0.0020   +0.0020   -0.0020 <--+---     -0.0000
------------------------------------------------------------------------------------------
ADJUST T7D BY -0.0010
 
ADJUST MACRO #501 BY 0.0085
ADJUST MACRO #502 BY -0.0024
Duration 1 mins 41 secs              FAIL in:8 out:2                         End of Report
==========================================================================================

