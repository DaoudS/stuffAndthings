#   "InsulType : Rattic
atticR = {
	'noIns': '5',
	'someIns': '11',
	'std10Inch': '23',
	'highIns': '34'
}
#    "InsulType : Rattic
coolRoofnames = {
	'stdColor': '0.80',
	'reflectiveOrlow': '0.30',
	'veryReflective': '0.05'
}

# DHW Table dicts
washerGpdpp = {
	'none': '0',
	'veryLow': '1',
	'low': '2',
	'average': '3',
	'high': '6'
}

showrGpdpp = {
	'none': '0',
	'veryLow': '2',
	'low': '4',
	'average': '6',
	'high': '10'
}

otherGpdpp = {
	'none': '0',
	'veryLow': '3',
	'low': '5',
	'average': '7',
	'high': '9'
}

# DHWType Table dicts

dhwSb = {
	'stdGas': '70',
	'tanklessGas': '8',
	'condensing': '15',
	'tankless': '200',
	'electic': '500',
}

dhwReceff = {
	'stdGas': '0.75',
	'tanklessGas': '0.80',
	'condensing': '0.92',
	'tankless': '1.00',
	'electic': '1.00',
}

# Dyer Table Dicts
dryerFactor = {
	'none': '0',
	'gadLowuse': '4',
	'gasAvguse': '8',
	'gasHighuse': '12',
	'elecLowUse': '100',
	'elecAvguse': '200',
	'elecHighuse': '350'
}

cookingFactor = {
	'none': '0',
	'gadLowuse': '2',
	'gasAvguse': '5',
	'gasHighuse': '8',
	'elecLowUse': '80',
	'elecAvguse': '180',
	'elecHighuse': '300',
}

# Duct Leak dicts
effDuctheat = {
	'veryLeaky': '0.72',
	'leaky': '0.80',
	'average': '0.86',
	'tight': '0.96',
}

effDuctcool = {
	'veryLeaky': '0.72',
	'leaky': '0.80',
	'average': '0.86',
	'tight': '0.96',
}

ductInsul = {
	'none': '0.72',
	'std': '.90',
	'high': '.95'
}

# Foundation Names
fdnFactor = {
	'basement': '0.5',
	'crawl': '0.25',
	'slab': '0.1'
}

#Foundation Insulation Names
fdnR = {
	'none': '6',
	'walls': '18',
	'ceiling': '12'
}

regain = {
	'none': '.70',
	'walls': '.89',
	'ceiling': '.30'
}

# Fridge Name Dicts
fridgeKWH = {
	'effecieint': '460',
	'average': '750',
	'1980sSBS': '1200',
	'1970sSBS': '1800'
}

fridge2Name = {
	'none': '0',
	'1990sOrnewer': '700',
	'1980sSBS': '1200',
	'60sSBSorGreaterthanOne': '2000'
}

# Heat Names dicts
hEff = {
	'oldOil63perGas': '0.63',  # Percent
	'stdOil80perGas': '0.80',  # Percent
	'oldGas72per': '0.72',  # Percent
	'stdGas80per': '0.80',  # Percent
	'condensingGas': '0.92',  # Percent
	'oldHeatPump': '1.8',
	'newerHeatpump': '2.3',
	'highEffheatPump': '2.6',
	'electricResistance': '1.05'
}

######################

# Window Shading
windowShading = {
	'veryLow': '0.75',
	'Low': '0.6',
	'typical': '0.5',
	'high': '0.25',
	'veryhigh': '0.1',
}

# Window to wall ratio
windowPctWall = {
	'windowPctWall': '0.15',
}

# Window Names, R value and SGHC
windowR = {
	'single': '1.4',
	'dblOrSglAndStorm': '2.1',
	'dblAndLowE': '2.6',
	'super': '3.2',
}

windowsghc = {
	'single': '0.8',
	'dblOrSglAndStorm': '0.6',
	'dblAndLowE': '0.4',
	'super': '0.3',
}

# Wall R values, WallNames
wallR = {
	'noIns': '5',
	'partialOrSemiIns': '8',
	'stdIns': '10',
	'goodIns': '14',
	'veryGoodOrFoam': '20',
}

# Light names, lighting load values
lightFactor = {
	'veryLow': '0.2',
	'Low': '0.6',
	'average': '1',
	'high': '1.5',
	'veryhigh': '2.0',
}

plug = {
	'veryLow': '0.2',
	'Low': '0.6',
	'average': '1',
	'high': '1.5',
	'veryhigh': '2.0',
}

entertaninment_val= {
	'veryLow': '0.2',
	'Low': '0.6',
	'average': '1',
	'high': '1.5',
	'veryhigh': '2.0',
}

# HomeLeakageNames, LeakyNames

houseLeakage = {
	'veryLeaky': '1.45',
	'leaky': '1.15',
	'average': '0.85',
	'fairlyTight': '0.75',
	'tight': '0.40',
	'HRV': '0.10',
}
