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

# define forest fraction 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="urban1Canopy = if(forestFrac>0&&(NLCD==21||NLCD==22),2,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="urban1Canopy_FFrac = if(forestFrac>0,if(NLCD==21||NLCD==22,1,null()),null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="urban1Canopy_LAI = if(forestFrac>0,if(NLCD==21||NLCD==22,3.5,null()),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="urban2Canopy = if(forestFrac>0&&(NLCD==21||NLCD==23),2,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="urban2Canopy_FFrac = if(forestFrac>0,if(NLCD==21||NLCD==23,1,null()),null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="urban2Canopy_LAI = if(forestFrac>0,if(NLCD==21||NLCD==23,3.5,null()),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious = if(forestFrac>0&&(NLCD==41||NLCD==43),2,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious_FFrac = if(forestFrac>0,if(NLCD==41,1.0,if(NLCD==43,0.5,null())),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious_LAI = if(forestFrac>0,if(NLCD==41,4.5,if(NLCD==43,3.0,null())),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen = if(forestFrac>0&&(NLCD==42||NLCD==43),1,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_Frac = if(forestFrac>0,if(NLCD==42,1.0,if(NLCD==43,0.5,null())),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_LAI = if(forestFrac>0,if(NLCD==42,5.0,if(NLCD==43,3.5,null())),null())" 

# define shrub fraction 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub1StratumID = if(shrubFrac>0&&(NLCD==21||NLCD==22),6,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub1_FFrac = if(shrubFrac>0,if(NLCD==21||NLCD==22,1,null()),null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub1_LAI = if(shrubFrac>0,if(NLCD==21||NLCD==22,3.5,null()),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub2StratumID = if(shrubFrac>0&&(NLCD==21||NLCD==23),6,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub2_FFrac = if(shrubFrac>0,if(NLCD==21||NLCD==23,1,null()),null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub2_LAI = if(shrubFrac>0,if(NLCD==21||NLCD==23,3.5,null()),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub3StratumID  = if(shrubFrac>0&&(NLCD==51||NLCD==52),6,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub3_FFrac = if(shrubFrac>0,if(NLCD==51||NLCD==52,1,null()),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub3_LAI = if(shrubFrac>0,if(NLCD==51||NLCD==52,3.5,null()),null())" 

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub4StratumID  = if(shrubFrac>0&&(NLCD==45||NLCD==90),6,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub4_FFrac = if(shrubFrac>0,if(NLCD==45||NLCD==90,1,null()),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shrub4_LAI = if(shrubFrac>0,if(NLCD==45||NLCD==90,3.5,null()),null())" 

# define crop fraction 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="crop1StratumID = if(cropFrac>0&&(NLCD==31||NLCD==46),7,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="crop1FFrac  = if(cropFrac>0,if(NLCD==31||NLCD==46,1,null()),null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="crop1LAI = if(cropFrac>0,if(NLCD==31||NLCD==46,3.5,null()),null())"

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="crop2StratumID = if(cropFrac>0&&(NLCD==81||NLCD==82),7,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="crop2FFrac  = if(cropFrac>0,if(NLCD==81||NLCD==82,1,null()),null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="crop2LAI = if(cropFrac>0,if(NLCD==81||NLCD==82,3.5,null()),null())"

# define lawn fraction 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1StratumID = if(lawnFrac>0&&(NLCD==31||NLCD==71),3,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1FFrac = if(lawnFrac>0&&(NLCD==31||NLCD==71),1.0,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1LAI = if(lawnFrac>0&&(NLCD==31||NLCD==71),1.5,null())"

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass2StratumID = if(lawnFrac>0&&(NLCD==72||NLCD==73),3,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass2FFrac = if(lawnFrac>0&&(NLCD==72||NLCD==73),1.0,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass2LAI = if(lawnFrac>0&&(NLCD==72||NLCD==73),1.5,null())"

$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass3StratumID = if(lawnFrac>0&&(NLCD==74||NLCD==95),3,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass3FFrac = if(lawnFrac>0&&(NLCD==74||NLCD==95),1.0,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass3LAI = if(lawnFrac>0&&(NLCD==74||NLCD==95),1.5,null())"