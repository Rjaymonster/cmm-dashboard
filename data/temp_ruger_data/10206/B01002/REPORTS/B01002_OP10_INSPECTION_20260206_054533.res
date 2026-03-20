------------------------------------------------------------------------------------------
06-Feb-2026 05:45                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3899    0.3850   -0.0050   +0.0050    0.0049 ---+--*
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3474    0.3500   -0.0050   +0.0050   -0.0026 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3119    0.3090   -0.0050   +0.0000    0.0029 ---+-->      0.0029
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2128    0.2100                        0.0028
Z-axis                 -2.5551   -2.5510                       -0.0041
TruePosition2D          0.0099                        0.0088              +-->      0.0011
Diameter                0.1573    0.1575   -0.0010   +0.0010   -0.0002 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4392    0.4400                       -0.0008
Y-axis                 -0.0851   -0.0842                       -0.0009
TruePosition2D          0.0025                        0.0154              *---
Diameter                0.1344    0.1360   -0.0050   +0.0050   -0.0016 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4091    3.4060   -0.0050   +0.0050    0.0031 ---+-*-
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2509    0.2500   -0.0050   +0.0050    0.0009 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3144    0.3140   -0.0020   +0.0020    0.0004 ---+*--
------------------------------------------------------------------------------------------
ADJUST T1H BY 0.0054
 
ADJUST MACRO #503 BY -0.0027
ADJUST MACRO #504 BY 0.0040
Duration 1 mins 54 secs              FAIL in:8 out:2                         End of Report
==========================================================================================

