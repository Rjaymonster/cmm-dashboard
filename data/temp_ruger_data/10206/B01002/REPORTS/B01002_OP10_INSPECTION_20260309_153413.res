------------------------------------------------------------------------------------------
09-Mar-2026 15:34                 B01002_OP10_INSPECTION                           Page  1
------------------------------------------------------------------------------------------
(in)                    ACTUAL   NOMINAL    LO-TOL    HI-TOL DEVIATION GRAPHIC       ERROR
------------------------------------------------------------------------------------------
INSPECTION ITEM #01 DATUM X TO DATUM A(PAD HEIGHT)
 
Plane:DATUM_A_PLANE--Point:X_CAST_BOLT_BOTTOM_POINT
Length-Xavg             0.3803    0.3850   -0.0050   +0.0050   -0.0047 *--+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #02 DATUM AB THEO INTERSECT TO THE INSIDE CAST WALL
 
Line:DATUM_AB_INTERSECT--Point:CAST_WALL_POINT
Length_Yavg             0.3548    0.3500   -0.0050   +0.0050    0.0048 ---+--*
------------------------------------------------------------------------------------------
INSPECTION ITEM #03 CHARGING HANDLE FRON FACE LOCATION
 
Point:CHARGING_SLOT_FRONT_POINT--Plane:DATUM_C_PLANE
Length-Zavg             0.3069    0.3090   -0.0050   +0.0000   -0.0021 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #04 FIRING PIN RETENTION HOLE SIZE AND LOCATION
 
Circle:FIRING_PIN_RETENTION_HOLE_CIRCLE
X-axis                  0.2081    0.2100                       -0.0019
Z-axis                 -2.5534   -2.5510                       -0.0024
TruePosition2D          0.0061                        0.0089              +-*-
Diameter                0.1574    0.1575   -0.0010   +0.0010   -0.0001 ---*---
------------------------------------------------------------------------------------------
INSPECTION ITEM #05 EXTRACTOR PLUNGER HOLE SIZE AND LOCATION
 
Circle:EXTRACTOR_PIN_CIRCLE
X-axis                  0.4391    0.4400                       -0.0009
Y-axis                 -0.0751   -0.0842                        0.0091
TruePosition2D          0.0183                        0.0179              +-->      0.0003
Diameter                0.1369    0.1360   -0.0050   +0.0050    0.0009 ---+*--
------------------------------------------------------------------------------------------
INSPECTION ITEM #06 OVERALL BOLT LENGTH
 
Plane:DATUM_C_PLANE--Point:BOLT_BACK_POINT
Length-Zavg             3.4096    3.4060   -0.0050   +0.0050    0.0036 ---+-*-
------------------------------------------------------------------------------------------
INSPECTION ITEM #07 CHARGING SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:CHARGING_SLOT_DEPTH_POINT
Length-Xavg             0.2463    0.2500   -0.0050   +0.0050   -0.0037 -*-+---
------------------------------------------------------------------------------------------
INSPECTION ITEM #08 FIRING PIN SLOT DEPTH
 
Plane:DATUM_A_PLANE--Point:FIRING_PIN_SLOT_DEPTH
Length-Xavg             0.3116    0.3140   -0.0020   +0.0020   -0.0024 <--+---     -0.0004
------------------------------------------------------------------------------------------
ADJUST T7D BY -0.0012
 
ADJUST MACRO #501 BY 0.0009
ADJUST MACRO #502 BY 0.0089
Duration 1 mins 52 secs              FAIL in:8 out:2                         End of Report
==========================================================================================

