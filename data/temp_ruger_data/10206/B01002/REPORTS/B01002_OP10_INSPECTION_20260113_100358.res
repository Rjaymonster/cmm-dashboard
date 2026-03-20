------------------------------------------------------------------------------------------
13-Jan-2026 10:03                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3804    0.3850   -0.0050   +0.0050   -0.0046 *--+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3437    0.3500   -0.0050   +0.0050   -0.0063 <--+---     -0.0013
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3033    0.3090   -0.0050   +0.0050   -0.0057 <--+---     -0.0007
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2097    0.2100                       -0.0003
Z-axis                 -2.5412   -2.5510                        0.0098
TruePosition2D          0.0197                        0.0087              +-->      0.0109
Diameter                0.1572    0.1575   -0.0010   +0.0010   -0.0003 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4394    0.4400                       -0.0006
Y-axis                 -0.0728   -0.0842                        0.0114
TruePosition2D          0.0228                        0.0183              +-->      0.0045
Diameter                0.1373    0.1360   -0.0050   +0.0050    0.0013 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4074    3.4060   -0.0050   +0.0050    0.0014 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2546    0.2500   -0.0050   +0.0050    0.0046 ---+--*
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3137    0.3140   -0.0020   +0.0020   -0.0003 ---*---
------------------------------------------------------------------------------------------
ADJUST MACRO #503 BY 0.0002
ADJUST MACRO #504 BY 0.0098
ADJUST MACRO #501 BY 0.0006
ADJUST MACRO #502 BY 0.0112
Duration 1 mins 31 secs              FAIL in:6 out:4                         End of Report
==========================================================================================

