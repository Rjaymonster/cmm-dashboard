------------------------------------------------------------------------------------------
06-Feb-2026 20:48                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3855    0.3850   -0.0050   +0.0050    0.0005 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3533    0.3500   -0.0050   +0.0050    0.0033 ---+-*-
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3094    0.3090   -0.0050   +0.0000    0.0004 ---+-->      0.0004
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2092    0.2100                       -0.0008
Z-axis                 -2.5561   -2.5510                       -0.0051
TruePosition2D          0.0103                        0.0094              +-->      0.0009
Diameter                0.1579    0.1575   -0.0010   +0.0010    0.0004 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4334    0.4400                       -0.0066
Y-axis                 -0.0833   -0.0842                        0.0008
TruePosition2D          0.0133                        0.0163              +-*-
Diameter                0.1353    0.1360   -0.0050   +0.0050   -0.0007 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4055    3.4060   -0.0050   +0.0050   -0.0005 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2503    0.2500   -0.0050   +0.0050    0.0003 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3126    0.3140   -0.0020   +0.0020   -0.0014 -*-+---
------------------------------------------------------------------------------------------
ADJUST T1H BY 0.0029
 
ADJUST MACRO #503 BY 0.0007
ADJUST MACRO #504 BY 0.0051
Duration 1 mins 43 secs              FAIL in:8 out:2                         End of Report
==========================================================================================

