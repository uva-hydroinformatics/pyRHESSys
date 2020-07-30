#!/bin/bash
grassCMD='grass'
### setup GRASS dataset
PROJDIR=$1 # full path to the project location;
EPSGCODE=$2 # need to (manually) lookup the EPSG code for NAD83 UTM ##N for the catchment
RESOLUTION=$3 #spatial resolution (meters) of the grids
RHESSysNAME=$4 # e.g., rhessys_baisman10m
GISDBASE="$PROJDIR"/$5
LOCATION_NAME="$RHESSysNAME"
LOCATION="$GISDBASE"/$LOCATION_NAME
MAPSET=PERMANENT

$grassCMD -c $EPSGCODE -e "$LOCATION" 

# define forest community 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen = if(forestFrac>0&&(NLCD==42||NLCD==43),1,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_Frac = if(forestFrac>0,if(NLCD==42,1.0,if(NLCD==43,0.5,null())),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_LAI = if(forestFrac>0,if(NLCD==42,5.0,if(NLCD==43,3.5,null())),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious = if(forestFrac>0&&(NLCD==41||NLCD==43),2,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious_FFrac = if(forestFrac>0,if(NLCD==41,1.0,if(NLCD==43,0.5,null())),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious_LAI = if(forestFrac>0,if(NLCD==41,4.5,if(NLCD==43,3.0,null())),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shurb = if(forestFrac>0&&(NLCD==51||NLCD==52),6,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shurb_FFrac = if(forestFrac>0,if(NLCD==51||NLCD==52,1,null()),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shurb_LAI = if(forestFrac>0,if(NLCD==51||NLCD==52,3.5,null()),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1StratumID = if(lawnFrac>0,3,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1FFrac = if(lawnFrac>0,1.0,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1LAI = if(lawnFrac>0,1.5,null())"