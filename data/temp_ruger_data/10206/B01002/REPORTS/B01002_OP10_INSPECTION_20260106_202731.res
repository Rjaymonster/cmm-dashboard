------------------------------------------------------------------------------------------
06-Jan-2026 20:27                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3895    0.3850   -0.0050   +0.0050    0.0045 ---+--*
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3496    0.3500   -0.0050   +0.0050   -0.0004 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3055    0.3090   -0.0050   +0.0050   -0.0035 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2109    0.2100                        0.0009
Z-axis                 -2.5457   -2.5510                        0.0053
TruePosition2D          0.0108                        0.0089              +-->      0.0019
Diameter                0.1574    0.1575   -0.0010   +0.0010   -0.0001 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4423    0.4400                        0.0023
Y-axis                 -0.0853   -0.0842                       -0.0012
TruePosition2D          0.0052                        0.0183              +*--
Diameter                0.1373    0.1360   -0.0050   +0.0050    0.0013 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4056    3.4060   -0.0050   +0.0050   -0.0004 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2515    0.2500   -0.0050   +0.0050    0.0015 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3174    0.3140   -0.0020   +0.0020    0.0034 ---+-->      0.0014
------------------------------------------------------------------------------------------
ADJUST MACRO #503 BY -0.0009
ADJUST MACRO #504 BY 0.0053
Duration 3 mins 2 secs               FAIL in:8 out:2                         End of Report
==========================================================================================

