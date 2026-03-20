------------------------------------------------------------------------------------------
28-Jan-2026 02:02                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3838    0.3850   -0.0050   +0.0050   -0.0012 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3475    0.3500   -0.0050   +0.0050   -0.0025 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3098    0.3090   -0.0050   +0.0000    0.0008 ---+-->      0.0008
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2097    0.2100                       -0.0003
Z-axis                 -2.5492   -2.5510                        0.0018
TruePosition2D          0.0036                        0.0094              +*--
Diameter                0.1579    0.1575   -0.0010   +0.0010    0.0004 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4332    0.4400                       -0.0068
Y-axis                 -0.0880   -0.0842                       -0.0038
TruePosition2D          0.0155                        0.0152              +-->      0.0003
Diameter                0.1342    0.1360   -0.0050   +0.0050   -0.0018 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4031    3.4060   -0.0050   +0.0050   -0.0029 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2480    0.2500   -0.0050   +0.0050   -0.0020 --*+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3122    0.3140   -0.0020   +0.0020   -0.0018 *--+---
------------------------------------------------------------------------------------------
ADJUST T1H BY 0.0032
 
ADJUST MACRO #501 BY 0.0067
ADJUST MACRO #502 BY -0.0039
Duration 41 mins 48 secs             FAIL in:8 out:2                         End of Report
==========================================================================================

