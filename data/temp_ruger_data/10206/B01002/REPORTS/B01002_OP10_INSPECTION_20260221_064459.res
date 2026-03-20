------------------------------------------------------------------------------------------
21-Feb-2026 06:44                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3818    0.3850   -0.0050   +0.0050   -0.0032 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.0421    0.3500   -0.0050   +0.0050   -0.3079 <--+---     -0.3029
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3141    0.3090   -0.0050   +0.0000    0.0051 ---+-->      0.0051
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2099    0.2100                       -0.0001
Z-axis                 -2.5612   -2.5510                       -0.0102
TruePosition2D          0.0205                        0.0080              +-->      0.0125
Diameter                0.1591    0.1575   -0.0010   +0.0010    0.0016 ---+-->      0.0006
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4796    0.4400                        0.0396
Y-axis                 -0.0275   -0.0842                        0.0566
TruePosition2D          0.1383                        0.0120              +-->      0.1263
Diameter                0.1427    0.1360   -0.0050   +0.0050    0.0067 ---+-->      0.0017
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4166    3.4060   -0.0050   +0.0050    0.0106 ---+-->      0.0056
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2530    0.2500   -0.0050   +0.0050    0.0030 ---+-*-
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3142    0.3140   -0.0020   +0.0020    0.0002 ---*---
------------------------------------------------------------------------------------------
ADJUST T11H BY 0.3079
 
ADJUST T3H BY -0.0106
 
ADJUST T1H BY 0.0075
 
T9D IS BAD:PLEASE REPLACE T9 WITH A NEW TOOL
 
==========================================================================================
------------------------------------------------------------------------------------------
21-Feb-2026 06:44                 B01002_OP10_INSPECTION                           Page  2
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
ADJUST MACRO #503 BY 0.0001
ADJUST MACRO #504 BY 0.0102
ADJUST MACRO #501 BY -0.0396
ADJUST MACRO #502 BY 0.0564
Duration 93 mins 56 secs             FAIL in:3 out:7                         End of Report
==========================================================================================

