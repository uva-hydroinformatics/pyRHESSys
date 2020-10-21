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

# Forest Community
## define evergreen fraction using "forestFrac" and "NLCD 42(Evergreen Forest) & 43(Mixed Forest)"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen = if(forestFrac>0&&(NLCD==42||NLCD==43),1,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_Frac = if(forestFrac>0,if(NLCD==42,1.0,if(NLCD==43,0.5,null())),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_LAI = if(forestFrac>0,if(NLCD==42,5.0,if(NLCD==43,3.5,null())),null())" 
## define decidious fraction using "forestFrac" and "NLCD 41(Deciduous Forest) & 43(Mixed Forest)"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious = if(forestFrac>0&&(NLCD==41||NLCD==43),2,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious_FFrac = if(forestFrac>0,if(NLCD==41,1.0,if(NLCD==43,0.5,null())),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="decidious_LAI = if(forestFrac>0,if(NLCD==41,4.5,if(NLCD==43,3.0,null())),null())" 
## define shurb fraction using "forestFrac" and "NLCD 51(Dwarf Scrub:AK only) and 52(Shrub/Scrub)"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shurb = if(forestFrac>0&&(NLCD==51||NLCD==52),6,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shurb_FFrac = if(forestFrac>0,if(NLCD==51||NLCD==52,1,null()),null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="shurb_LAI = if(forestFrac>0,if(NLCD==51||NLCD==52,3.5,null()),null())" 
## define oak_canopy fraction using forestFrac
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="oak_canopy = if(forestFrac>0,102,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="oak_canopy_FFrac = if(forestFrac>0,0.8,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="oak_canopy_LAI = if(forestFrac>0,5.5,null())"
## define maple_canopy fraction using forestFrac
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="maple_canopy = if(forestFrac>0,111,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="maple_canopy_FFrac = if(forestFrac>0,0.2,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="maple_canopy_LAI = if(forestFrac>0,5.5,null())"
## define deciduous fraction using "NLCD 41(Deciduous Forest), 43(Mixed Forest), 90(Woody Wetlands), and 95(Emergent Herbaceous Wetlands)"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="deciduous = if(NLCD==41||NLCD==43||NLCD==90||NLCD==95,0,2,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="deciduous_FFrac = if(NLCD==41||NLCD==43||NLCD==90||NLCD==95,0.8,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="deciduous_LAI = if(NLCD==41||NLCD==43||NLCD==90||NLCD==95,4.0,null())"
## define evergreen fraction using "NLCD 42(Evergreen Forest) & 52(Shrub/Scrub)"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen = if(NLCD==42||NLCD==52,1,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_FFrac = if(NLCD==42||NLCD==52,0.8,null())" 
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="evergreen_LAI = if(NLCD==42||NLCD==52,4.0,null())"

# Lawn(GRASS) Community
## define grass fraction using lawnFrac
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1StratumID = if(lawnFrac>0,3,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1FFrac = if(lawnFrac>0,1.0,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1LAI = if(lawnFrac>0,1.5,null())"
## define grass fraction using "NLCD 71(Grasslands/Herbaceous), 72(Sedge/Herbaceous(AK Only)), 81(Pasture/Hay), and 82(Cultivated Crops)"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1StratumID = if(NLCD==71||NLCD==72||NLCD==81||NLCD==82,3,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1FFrac = if(NLCD==71||NLCD==72||NLCD==81||NLCD==82,1.0,null())"
$grassCMD "$LOCATION"/"$MAPSET" --exec r.mapcalc --overwrite expression="grass1LAI = if(NLCD==71||NLCD==72||NLCD==81||NLCD==82,1.5,null())"