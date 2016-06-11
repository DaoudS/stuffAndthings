from functools import wraps
from math import sqrt
import inspect
import csv


def floatIfPercent(string):
    return float(string) if '%' not in string else float(string.strip('%')) / 100

'''
# load tables
# variable/filename refer to the first and second columns in lookups.csv
for variable, filename in csv.reader(open('lookups.csv', 'r')):
    try:
        csvfile = csv.reader(open(filename, 'r'))  ##csvfile is the object
        #rint("%s loaded" % filename)
    except IOError:
        print("Failed to open file %a" % filename)
    #columnNames = csvfile.__next__()
    #print (csvfile)
'''
# stuff = {'name': 'Zed', 'age': 39, 'height': 6 * 12 + 2}

#   "InsulType : Rattic
atticNames = {
    'noIns': '5',
    'someIns': '11',
    'std10Inch': '23',
    'highIns': '34'
}
#    "InsulType : Rattic
coolRoofnames = {
    'stdColor': '0.80',
    'reflectiveOrlow': '0.30',
    'veryReflective': 'o.o5'
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

dhWsb = {
    'stdGas'            : '70',
    'tanklessGas'       : '8',
    'condensing'        : '15',
    'tankless'          : '200',
    'electic'           : '500',
}

dhWreceff = {
    'stdGas'            : '0.75',
    'tanklessGas'       : '0.80',
    'condensing'        : '0.92',
    'tankless'          : '1.00',
    'electic'           : '1.00',
}

# Dyer Table Dicts
dryerFactor = {
    'none'            : '0',
    'gadLowuse'       : '4',
    'gasAvguse'       : '8',
    'gasHighuse'      : '12',
    'elecLowUse'      : '100',
    'elecAvguse'      : '200',
    'elecHighuse'     : '350'
}

cookingFactor = {
    'none'            : '0',
    'gadLowuse'       : '2',
    'gasAvguse'       : '5',
    'gasHighuse'      : '8',
    'elecLowUse'      : '80',
    'elecAvguse'      : '180',
    'elecHighuse'     : '300',
}

# percent values
ductInsul = {
    'none'            : '0.72',
    'std'             : '.90',
    'high'            : '.95'
}

# Duct Leak dicts
effDuctheat = {
    'veryLeaky' : '0.72',
    'leaky' : '0.80',
    'average' : '0.86',
    'tight' : '0.96',
}

effDuctcool = {
    'veryLeaky' : '0.72',
    'leaky' : '0.80',
    'average' : '0.86',
    'tight' : '0.96',
}

# Foundation Names
fdnFactor = {
    'basement' : '0.5',
    'crawl' : '0.25',
    'stab' : '0.1'
}

fdnR = {
    'none' : '6',
    'walls' : '18',
    'ceiling' : '12'
}

regain = {
    'none' : '.70',
    'walls' : '.89',
    'ceiling' : '.30'
}

# Fridge Name Dicts
fridgeKWH = {
    'effecieint' : '460',
    'average' : '750',
    '1980sSBS' : '1200',
    '1970sSBS' : '1800'
}
fridge2Name = {
    'none' : '0',
    '1990sOrnewer': '700',
    '1980sSBS' : '1200',
    '60sSBSorGreaterthanOne' : '2000'
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


class House:
    # @initializer
    def __init__(self,
                 # House Characteristics
                 finishedFloorArea,  # (sq.ft.)
                 stories,
                 occupants,
                 heatingSetpoint,  # Farenheit
                 heatingSystemType,
                 wallInsulation,
                 atticInsulation,
                 windows,
                 airTightness,
                 foundationType,
                 foundationInsulation,
                 heatingIsNotForcedAir,
                 ductsPercentInAttic,
                 ductsPercentInSlab,  # Contemptorary
                 ductLeakiness,
                 ductInsulation,
                 # Cooling Info
                 ACSEER,
                 coolingSetpoint,
                 windowShading,
                 coolRoofOrRadBarrierRafters,

                 # Water Heating Info
                 waterHeaterType,
                 showeringUse,  # In Flow And Time
                 laundryUse,
                 otherHotWaterUse,

                 # All Else Info
                 lightingUsageIntensity,
                 primaryrefrigerator,
                 extraRefrigeratorsAndFreezers,
                 entertainment,  # TVs and PCs
                 otherLargeUses,  # (500 kWh)
                 plugAndOtherLoads,
                 clothesDryer,
                 cooking,
                 closestWeatherStation
                 ):
        averageFloorSize = self.finishedFloorArea / self.stories
        self.wallArea = (1 - WindowPctWall) * self.stories * 35 * sqrt(averageFloorSize)
        self.atticArea = averageFloorSize
        self.windowsArea = (WindowPctWall / (1 - WindowPctWall)) * self.wallArea
        self.effectiveFoundationArea = fdn[self.foundationType]['FndnFactor'] * (
        self.wallArea + self.windowsArea) / self.stories
        self.HDD65 = tmy2BasedData[self.closestWeatherStation]['HDD65']
        self.HDD60 = tmy2BasedData[self.closestWeatherStation]['HDD60']
        self.CDPH65 = tmy2BasedData[self.closestWeatherStation]['CDPH65']
        self.CDH74 = tmy2BasedData[self.closestWeatherStation]['CDH74']
        self.coolSolar = tmy2BasedData[self.closestWeatherStation]['Solar Cl']
        self.heatSolar = tmy2BasedData[self.closestWeatherStation]['Solar Ht']
        self.coolHours74 = tmy2BasedData[self.closestWeatherStation]['Cool Hrs 74']
        self.heatDays60 = tmy2BasedData[self.closestWeatherStation]['Ht Days']

    # print windowShading

    def adjustedOccupancy(self):
        return min(self.occupants, 2 + 0.5 * (self.occupants - 2))

    # Climate Calulations
    def HDDPerDegree(self):
        return min(0.1, 0.9 * (0.1993 + 0.0000175 * self.HDD60 - 0.003375 * sqrt(self.HDD60)))

    def heatingCFM2UValue(self):
        return 0.7 * (1.08 / (28 - (self.HDD65 / 1000)))

    def coolingCFM2UValue(self):
        return 0.024 + self.coolingDT() / 1000

    def coolingDT(self):
        return 0 if self.coolHours74 < 10 else self.CDH74 / self.coolHours74

    def EERMultiplier(self):
        return 1 + (9 - self.coolingDT()) * 0.018

    def latentInfilMultiplier(self):
        return 1 if self.CDH74 < 10 else min(1 + (self.CDPH65 / self.CDH74) * 2.7, 4)

    def latentCDHMultiplier(self):
        return 1 if self.CDH74 == 0 else min(1.5, 0.9 + 0.7 * self.CDPH65 / self.CDH74)

    def latentEERMultiplier(self):
        return 1.06 - (0.15 / 0.6) * (self.latentCDHMultiplier() - 0.9)

    def tColdWater(self):
        return max(45, (6 + 70.6 + 0.0001732 * self.CDH74 - 0.00223 * self.HDD65 - 0.104 * sqrt(self.HDD65)))

    # Miscellaneous Calulations
    def CFM50AirLeakage(self):
        return self.wallArea + self.atticArea + self.windowsArea

    def heatingEfficiency(self):
        if heat[self.heatingSystemType]['Heff'] > 1.3:
            return heat[self.heatingSystemType]['Heff'] + 0.35 - self.HDD65 / 10000
        else:
            return heat[self.heatingSystemType]['Heff']

    def gallonsOfHotWaterPerDay(self):
        showerEstimate = DHW[self.showeringUse]['shwrgpdpp']
        laundryEstimate = DHW[self.laundryUse]['Washergpdpp']
        otherEstimate = DHW[self.otherHotWaterUse]['othergpdpp']
        return self.occupants * (showerEstimate + laundryEstimate + otherEstimate)

    def lighting(self):
        return 0.3 * self.finishedFloorArea + 300 * self.adjustedOccupancy() * light[self.lightingUseIntensity][
            'LightFactor']

    def refridgeration(self):
        return fridge[self.primaryRefridgeration]['fridgekwh'] + fridge2[self.extraRefrigeratorsAndFreezers][
            'fridge2kwh']

    def entertainment(self):
        return self.adjustedOccupancy() * 500 * light[self.entertainment]['Entertainment']

    def otherPlugLoads(self):
        return sum(
            500 * self.adjustedOccupancy(),
            0.3 * self.finishedFloorArea,
            500 * (1 - self.heatingIsNotForcedAir) * light[self.plugAndOtherLoads]['Plug']
        )

    def dryer(self):
        return self.adjustedOccupancy() * dryer[self.clothesDryer]['DryerFactor']

    def cooking(self):
        return self.adjustedOccupancy() * dryer[self.cooking]['CookingFactor']

    def electricBaseloadTotal(self):
        return sum(
            self.lighing(),
            self.refridgeration(),
            self.entertainment(),
            self.otherPlugLoads(),
            self.dryer() * usesGas(self.clothesDryer),
            self.cooking() * usesGas(self.cooking)
        )

    # heating
    def heatUA(self):
        return sum(
            self.wallArea / wall[self.wallInsulation]['Rwall'],
            self.atticArea / attic[self.atticInsulation]['Rattic'],
            self.windowArea / window[self.windowInsulation]['Rwindow'],
            self.effectiveFoundationArea / fdnIn[self.foundationInsulation]['FndnR']
        )

    def heatInfilUA(self):
        return max(
            15,
            self.finishedFloorArea / 100,
            self.CFM50AirLeakage * (self.stories ** 0.3) * self.heatingCFM2UValue() * (
            0.9 if (self.foundationInsulation == 'None' and self.foundationType == 'Basement') else 1)
        )

    def heatTotalUA(self):
        return self.heatUA() + self.heatInfilUA()

    def internalGainsBTUPerhour(self):  # BTU/hour
        return (
                   self.electricBaseloadTotal() * 3412 * 0.8 +
                   usesGas(self.cooking) * (25 * 1000 if usesGas(self.waterHeaterType) else 0.3 * 3412) +
                   0.8 * self.cooking() * (100 * 1000 if usesGas(self.cooking) else 3412) +
                   1300 * 1000 * self.occupants
               ) / 8760

    def htWindowSolar(self):
        return 0.6 * self.windowArea * window[self.windowShading][''] * self.heatSolar * window[self.windows][
            'RWindow'] / self.heatDays60

    def tFloat(self):
        return (1.1 * self.internalGainsBTUPerhour() + self.htWindowSolar()) / self.heatTotalUA() + min(
            3,
            max(
                0,
                (self.HDD65 - 4000) / 2000
            )
        )

    def tBal(self):
        return self.heatingSetpoint - self.tFloat()

    def HDDEffective(self):
        return self.HDD60 * (1 - (60 - self.tBal()) * self.HDDPerDegree())


    def htDistEfficiency(self):
        return 0.95 if self.heatingIsNotForcedAir else 1 - (1 - self.ductHtgDeliveryEff()) * (1 - self.ductHtgRegain())

    def ductHtgRegain(self):
        return (
               1 - self.ductsPercentInAttic - self.ductsPercentInSlab) + 0.1 * self.ductsPercentInAttic + self.ductsPercentInSlab * \
                                                                                                          FdnIns[
                                                                                                              self.foundationInsulation][
                                                                                                              'regain']

    def ductHtgDeliveryEff(self):
        return ductLeak[self.ductLeakiness]['EffDuctHeat'] * ductIns[self.ductInsulation]['Efficiency']

    def heatingUsage(self):
        return (24 * self.heatingTotalUA * self.HDDEffective()) / (
            self.heatingEfficiency() *
            self.htDistEfficiency() *
            (96588 * usesGas(self.heatingSystemType) + 3412)
        )

    # Cooling
    def UAShell(self):
        return sum(
            self.wallArea / wall[self.wallInsulation]['Rwall'],
            self.atticArea / attic[self.atticInsulation]['Rattic'],
            self.windowArea / window[self.windowInsulation]['Rwindow']
        )

    def infiltration(self):
        return max(
            15,
            self.finishedFLoorArea / 100,
            self.CFM50AirLeakage() * self.coolingCFM2UValue() * self.latentInfilMultiplier()
        )

    def roofExtraGain(self):
        return self.atticArea / attic[self.atticInsulation]['Rattic'] * coolRoof[self.coolRoofOrRadBarrierRafters]['']

    def totalUA(self):
        return self.UAShell() + self.infiltraion() + self.roofExtraGain()

    def coolingUsage(self):
        loadFromUA = self.totalUA() * self.CDH74 * self.latentCDHMultiplier()
        internalGains = self.internalGainsBTUPerhour() * self.coolHours74 * self.latentCDHMultiplier()
        windowCISolar = (
            0.45 * self.electricBaseloadTotal() *
            windowShading[self.windowShading][''] *
            self.coolSolar *
            window[self.windows]['SHGC']
        )
        if self.coolEfficiency() <= 0:
            return 0
        else:
            return (loadFromUA + internalGains + windowCISolar) * self.coolTStatAdjust() / 3412 / self.coolEfficiency()
    # Other
    def coolTStatAdjust(self):
        return 1 + 0 if self.coolingDT() == 0 else min(
            0.1,
            (78 - self.coolingSetpoint) / self.coolingDT()
        )

    def coolingACEfficiency(self):
        return (
            self.EERMultiplier() *
            self.latentEERMultiplier() *
            (
                min(13, self.ACSEER) +
                0.4 * max(0, self.ACSEER - 13)
            ) / 3.412
        )

    def ductCLGRegain(self):
        return (
            (1 - self.ductsPercentInAttic - self.ductsPercentInSlab) +
            0.1 * self.ductsPercentInAttic +
            0.4 * self.ductsPercentInSlab * fdnIns[self.foundationInsulation]['regain']
        )

    def ductCLGDeliveryEfficiency(self):
        return 1 - (
            1.1 *
            (1 - self.ductHTGDeliveryEff()) *
            (1 + 0.8 * self.ductsPercentInAttic * coolRoof[self.coolRoofOrRadBarrierRafters][''])
        )

    def CLDistEfficiency(self):
        return 1 - (1 - self.ductCLGDeliveryEfficiency()) * (1 - self.ductCLGRegain())

    def coolEfficiency(self):
        return self.coolingEfficency() * self.CLDistEfficiency()

    def DHWStandby(self):
        return DHWType[self.waterHeaterType]['DHWsb'] * 0.014 * sqrt(self.HDD65)

    def DHWHotWater(self):
        return (
            self.gallonsOfHotWaterPerDay() *
            365 *
            8.3 *
            (125 - self.tColdWater()) /
            (
                (100 * 1000 if usesGas(self.waterHeaterType) else 3412) *
                DHWType[self.waterHeaterType]['DHWreceff']
            )
        )

    def DHWTotal(self):
        return self.DHWStandby() + self.DHWHotWater()
