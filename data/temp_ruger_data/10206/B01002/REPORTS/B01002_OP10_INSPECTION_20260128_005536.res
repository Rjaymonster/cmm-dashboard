------------------------------------------------------------------------------------------
28-Jan-2026 00:55                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3834    0.3850   -0.0050   +0.0050   -0.0016 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3465    0.3500   -0.0050   +0.0050   -0.0035 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3069    0.3090   -0.0050   +0.0000   -0.0021 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2095    0.2100                       -0.0005
Z-axis                 -2.5448   -2.5510                        0.0062
TruePosition2D          0.0125                        0.0093              +-->      0.0032
Diameter                0.1578    0.1575   -0.0010   +0.0010    0.0003 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4335    0.4400                       -0.0065
Y-axis                 -0.0882   -0.0842                       -0.0040
TruePosition2D          0.0153                        0.0156              +--*
Diameter                0.1346    0.1360   -0.0050   +0.0050   -0.0014 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4129    3.4060   -0.0050   +0.0050    0.0069 ---+-->      0.0019
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2479    0.2500   -0.0050   +0.0050   -0.0021 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3120    0.3140   -0.0020   +0.0020   -0.0020 *--+---
------------------------------------------------------------------------------------------
ADJUST T3H BY -0.0069
 
ADJUST MACRO #503 BY 0.0005
ADJUST MACRO #504 BY -0.0062
Duration 2 mins 33 secs              FAIL in:8 out:2                         End of Report
==========================================================================================

