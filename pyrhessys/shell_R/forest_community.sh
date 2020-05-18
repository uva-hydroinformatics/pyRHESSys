#!/bin/bash
# define forest community 
r.mapcalc --overwrite expression="evergreen = if(forestFrac>0&&(NLCD==42||NLCD==43),1,null())" 
r.mapcalc --overwrite expression="evergreen_Frac = if(forestFrac>0,if(NLCD==42,1.0,if(NLCD==43,0.5,null())),null())" 
r.mapcalc --overwrite expression="evergreen_LAI = if(forestFrac>0,if(NLCD==42,5.0,if(NLCD==43,3.5,null())),null())" 

r.mapcalc --overwrite expression="decidious = if(forestFrac>0&&(NLCD==41||NLCD==43),2,null())" 
r.mapcalc --overwrite expression="decidious_FFrac = if(forestFrac>0,if(NLCD==41,1.0,if(NLCD==43,0.5,null())),null())" 
r.mapcalc --overwrite expression="decidious_LAI = if(forestFrac>0,if(NLCD==41,4.5,if(NLCD==43,3.0,null())),null())" 

r.mapcalc --overwrite expression="shurb = if(forestFrac>0&&(NLCD==51||NLCD==52),6,null())" 
r.mapcalc --overwrite expression="shurb_FFrac = if(forestFrac>0,if(NLCD==51||NLCD==52,1,null()),null())" 
r.mapcalc --overwrite expression="shurb_LAI = if(forestFrac>0,if(NLCD==51||NLCD==52,3.5,null()),null())" 