from math import sqrt
import csv
import dicts
import logging

LOG_FILENAME = 'debug.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)


class House:
    # @initializer
    def __init__(self):
        # House Characteristics
        self.window_pct_wall = .15
        self.finished_floor_area = 1844  # (sq.ft.)
        self.stories = 1
        self.occupants = 4
        self.heating_setpoint = 68  # Farenheit
        self.heating_system_type = float(dicts.hEff["electricResistance"])
        self.wall_insulation = float(dicts.wallR['goodIns'])
        self.attic_insulation = float(dicts.atticR['highIns'])
        self.window_insulation = float(dicts.windowR['super'])
        self.window_sghc = float(dicts.windowsghc['super'])
        self.air_tightness = float(dicts.houseLeakage['fairlyTight'])
        self.foundation_type = float(dicts.fdnFactor['slab'])
        self.foundation_insulation = float(dicts.fdnR['none'])
        self.heating_is_not_forced_air = 0
        self.ducts_percent_in_attic = 0.0
        self.ducts_percent_in_slab = 0.0  # Contemptorary
        self.duct_leakiness = float(dicts.effDuctheat['average'])
        self.duct_insulation = float(dicts.ductInsul['none'])
        self.average_floor_size = self.finished_floor_area / self.stories
        self.wall_area = (1 - self.window_pct_wall) * self.stories * 35 * sqrt(self.average_floor_size)
        self.attic_area = self.average_floor_size
        self.windows_area = (self.window_pct_wall / (1 - self.window_pct_wall)) * self.wall_area
        self.effectiveFoundationArea = self.foundation_type *(self.wall_area + self.windows_area) / self.stories
        self.hdd65 = 0
        self.hdd60 = 0
        self.cdph65 = 0
        self.cdh74 = 0
        self.cool_solar = 0
        self.heat_solar = 0
        self.cool_hours74 = 0
        self.heat_days60 = 0

        # Cooling Info
        self.acseer = 21
        self.cooling_setpoint = 78
        self.window_shading = float(dicts.windowShading['typical'])
        self.cool_roof_o_rad_barrier_rafters = float(dicts.coolRoofnames['stdColor'])

        # Water Heating Info
        self.water_heater_type = float(dicts.dhwSb['stdGas'])
        self.water_heater_eff = float(dicts.dhwReceff['stdGas'])
        self.shower_estimate = float(dicts.showrGpdpp['average'])
        self.laundry_estimate = float(dicts.washerGpdpp['average'])
        self.other_estimate = float(dicts.otherGpdpp['average'])

        # All Else Info
        self.lighting_usage_intensity = float(dicts.lightFactor['average'])
        self.primaryre_frigerator = float(dicts.fridgeKWH['average'])
        self.extra_refrigerator_and_freezers = float(dicts.fridge2Name['none'])
        self.other_large_uses = 0  # (500 kWh)
        self.plug_and_other_loads = float(dicts.plug['average'])
        self.entertainment_load = float(dicts.entertaninment_val['average'])
        self.dryer_load = float(dicts.dryerFactor['gasAvguse'])
        self.cooking_load = float(dicts.cookingFactor['elecAvguse'])

        self.station = 0
        self.zip = 32043
        self.last_zip = 0
        self.current_row_zip = 0
        self.last_station = 0

    def dhw_uses_gas(self):
        if self.water_heater_type <= 70:
            return 1
        else:
            return 0

    def cooking_uses_gas(self):
        if self.cooking_load <= 8:
            return 1
        else:
            return 0

    def heating_uses_gas(self):
        if self.heating_system_type <= 1.0:
            return 1
        else:
            return 0

    def dryer_uses_gas(self):
        if self.dryer_load <= 12:
            return 1
        else:
            return 0

    def find_weather_station(self):

        # open the file in universal line ending mode
        with open('docs/zip.csv', 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            zipReader = csv.DictReader(infile)

            # Cycles through list of zipcodes until  inputted zipcode is equal to the correct weather self.station or
            # assuming the no exact match exits, is assigned to the previous weather self.station in the loop.
            for row in zipReader:
                self.current_row_zip = int(row['zip'])
                self.station = row['station']
                if self.zip == self.current_row_zip:
                    break
                elif self.zip > self.current_row_zip:
                    self.last_zip = self.current_row_zip
                    self.last_station = self.station
                else:
                    self.station = self.last_station
                    break
        logging.debug("CLOSEST STATION: %s" % self.station)
        return self.station;

    def gather_weather_station_data(self, station):

        # open the file in universal line ending mode
        with open('docs/tmy2BasedData.csv', 'rU') as infile:
            # read the file as a dictionary for each row ({header : value})
            dataReader = csv.DictReader(infile)

            for row in dataReader:
                currRowfile = row['file']

                if currRowfile == self.station:
                    self.hdd65 = int(row['HDD65'])
                    self.hdd60 = int(row['HDD60'])
                    self.cdph65 = int(row['CDPH65'])
                    self.cdh74 = int(row['CDH74'])
                    self.cool_solar = int(row['Solar Cl'])
                    self.heat_solar = int(row['Solar Ht'])
                    self.cool_hours74 = int(row['Cool Hrs 74'])
                    self.heat_days60 = int(row['Ht Days']) * 24
                    logging.debug("FOUND STATION: %s" % currRowfile)
                    logging.debug("hdd65 VALUE:%s" % self.hdd65)
                    logging.debug("hdd60 VALUE:%s" % self.hdd60)
                    logging.debug("cdph65 VALUE:%s" % self.cdph65)
                    logging.debug("cdh74 VALUE:%s" % self.cdh74)
                    logging.debug("cool_hours74 VALUE:%s" % self.cool_solar)
                    logging.debug("heat_solar VALUE:%s" % self.heat_solar)
                    logging.debug("cool_hours74 VALUE:%s" % self.cool_hours74)
                    logging.debug("heat_days60 VALUE:%s" % self.heat_days60)
                    break
                else:
                    pass
        return self.hdd60, self.hdd60, self.cdph65, self.cdh74, self.cool_solar, self.heat_solar, self.cool_hours74, self.heat_days60

    def adjusted_occupancy(self):
        return min(self.occupants, 2 + 0.5 * (self.occupants - 2))

    # Climate Calulations
    def hdd_per_degree(self):
        return min(0.1, 0.9 * (0.1993 + 0.0000175 * self.hdd60 - 0.003375 * sqrt(self.hdd60)))

    def heating_cfm2u_value(self):
        return 0.7 * (1.08 / (28 - (self.hdd65 / 1000)))

    def cooling_dt(self):
        return 0 if self.cool_hours74 < 10 else self.cdh74 / self.cool_hours74

    def cooling_cfm2u_value(self):
        return 0.024 + self.cooling_dt() / 1000

    def eer_multiplier(self):
        return 1 + (9 - self.cooling_dt()) * 0.018

    def latent_infil_multiplier(self):
        return 1 if self.cdh74 < 10 else min(1 + (self.cdph65 / self.cdh74) * 2.7, 4)

    def latent_cdh_multiplier(self):
        return 1 if self.cdh74 == 0 else min(1.5, 0.9 + 0.7 * self.cdph65 / self.cdh74)

    def latenteer_multiplier(self):
        return 1.06 - (0.15 / 0.6) * (self.latent_cdh_multiplier() - 0.9)

    def t_coldwater(self):
        return max(45, (6 + 70.6 + 0.0001732 * self.cdh74 - 0.00223 * self.hdd65 - 0.104 * sqrt(self.hdd65)))

    # Miscellaneous Calulations
    def cfm50_airleakage(self):
        return (self.wall_area + self.attic_area + self.windows_area) * self.air_tightness

    def heating_efficiency(self):
        if self.heating_system_type > 1.3:
            return self.heating_system_type + 0.35 - self.hdd65 / 10000
        else:
            return self.heating_system_type

    def gallons_o_hotwater_perday(self):
        return self.occupants * (self.shower_estimate + self.laundry_estimate + self.other_estimate)

    def lighting(self):
        return 0.3 * self.finished_floor_area + 300 * self.adjusted_occupancy() * self.lighting_usage_intensity

    def refridgeration(self):
        return self.primaryre_frigerator + self.extra_refrigerator_and_freezers

    def entertaninment_val(self):
        return 500 * self.adjusted_occupancy() * self.entertainment_load

    # Opted to use adjusted occupancy over occupancy

    def other_plug_loads(self):
        return (500 * self.adjusted_occupancy() +
            0.3 * self.finished_floor_area +
            500 * (1 - self.heating_is_not_forced_air)) * self.plug_and_other_loads

    def dryer(self):
        return self.adjusted_occupancy() * self.dryer_load

    def cooking(self):
        return self.adjusted_occupancy() * self.cooking_load

    # Normalized adjusted occupancy. (.5 used over .3)

    def electric_baseload_total(self):
        return sum([
            self.lighting(),
            self.refridgeration(),
            self.entertaninment_val(),
            self.other_plug_loads(),
            self.dryer_load * self.dryer_uses_gas(),
            self.cooking_load * self.cooking_uses_gas()
        ])

    # heating
    def heat_ua(self):
        return sum([
            self.wall_area / self.wall_insulation,
            self.attic_area / self.attic_insulation,
            self.windows_area / self.window_insulation,
            self.effectiveFoundationArea / self.foundation_insulation
        ])

    def heat_infil_ua(self):
        return max(
            15,
            self.finished_floor_area / 100,
            self.cfm50_airleakage() * (self.stories ** 0.3) * self.heating_cfm2u_value() * (
                0.9 if (self.foundation_insulation == 'None' and self.foundation_type == 'Basement') else 1)
        )

    def heating_total_ua(self):
        return self.heat_ua() + self.heat_infil_ua()

    # HOT WATER LOAD CALC
    def dhw_standby(self):
        return self.water_heater_type * 0.014 * sqrt(self.hdd65)

    def dhw_hotwater(self):
        return (
            self.gallons_o_hotwater_perday() *
            365 *
            8.3 *
            (125 - self.t_coldwater()) /
            (
                (100000 if self.dhw_uses_gas() == 1 else 3412) *
                self.water_heater_eff
            )
        )

    def dhw_total(self):
        return self.dhw_standby() + self.dhw_hotwater()

    # END HOT WATER CALC

    def internal_gain_btu_perhour(self):  # BTU/hour
        return (
                   (self.electric_baseload_total() * 3412 * 0.8 + self.dhw_total() *
                   (0.25 * 100000 if self.dhw_uses_gas() == 1 else 0.3 * 3412) + 0.8 *
                   self.cooking() *
                   (100000 if self.cooking_uses_gas() == 1 else 3412) + 1300000 *
                   self.occupants)
                   / 8760
        )

    def ht_window_solar(self):
        return 0.6 * self.windows_area * self.window_shading * self.heat_solar * self.window_sghc / self.heat_days60

    def t_float(self):
        return (1.1 * self.internal_gain_btu_perhour() + self.ht_window_solar()) / self.heating_total_ua() + min(
            3,
            max(
                0,
                (self.hdd65 - 4000) / 2000
            )
        )

    def t_bal(self):
        return self.heating_setpoint - self.t_float()

    def hdd_effective(self):
        return self.hdd60 * (1 - (60 - self.t_bal()) * self.hdd_per_degree())

    def duct_htg_regain(self):
            return (1-self.ducts_percent_in_attic-self.ducts_percent_in_slab)+0.1*self.ducts_percent_in_attic+self.ducts_percent_in_slab*self.foundation_insulation


    def duct_htg_delivery_eff(self):
        return self.duct_leakiness * self.duct_insulation

    def ht_dist_efficiency(self):
        return 0.95 if self.heating_is_not_forced_air else 1 - (1 - self.duct_htg_delivery_eff()) * (1 - self.duct_htg_regain())

    def heating_usage(self):
        return (self.heating_total_ua() /
            (self.heating_efficiency() * self.ht_dist_efficiency()) *
            24 * self.hdd_effective()) / (96588 * self.heating_uses_gas() + 3412)
    # Cooling
    def ua_shell(self):
        return sum([
            self.wall_area / self.wall_insulation,
            self.attic_area / self.attic_insulation,
            self.windows_area / self.window_insulation
        ])

    def infiltration(self):
        return max(
            15,
            self.finished_floor_area / 100,
            self.cfm50_airleakage() * self.cooling_cfm2u_value() * self.latent_infil_multiplier()
        )

    def roof_extra_gain(self):
        return self.attic_area / self.attic_insulation * self.cool_roof_o_rad_barrier_rafters

    def total_ua(self):
        return self.ua_shell() + self.infiltration() + self.roof_extra_gain()

    def cool_tstat_adjust(self):
        return 1 + (0 if self.cooling_dt() == 0 else min(
            0.1, (78 - self.cooling_setpoint) / self.cooling_dt()
        ))

    def cooling_ace_efficiency(self):
        return (
            self.eer_multiplier() *
            self.latenteer_multiplier() *
            (
                min(13, self.acseer) +
                0.4 * max(0, self.acseer - 13)
            ) / 3.412
        )

    def duct_clg_regain(self):
        return (
            (1 - self.ducts_percent_in_attic - self.ducts_percent_in_slab) +
            0.1 * self.ducts_percent_in_attic +
            0.4 * self.ducts_percent_in_slab * self.foundation_insulation
        )

    def duct_clg_delivery_efficiency(self):
        return 1 - (
            1.1 *
            (1 - self.duct_htg_delivery_eff()) *
            (1 + 0.8 * self.ducts_percent_in_attic * self.cool_roof_o_rad_barrier_rafters)
        )

    def cl_dist_efficiency(self):
        return 1 - (1 - self.duct_clg_delivery_efficiency()) * (1 - self.duct_clg_regain())

    def cool_efficiency(self):
        return self.cooling_ace_efficiency() * self.cl_dist_efficiency()

    def load_from_ua(self):
        return self.total_ua() * self.cdh74 * self.latent_cdh_multiplier()

    def internal_gains(self):
        return self.internal_gain_btu_perhour() * self.cool_hours74 * self.latent_cdh_multiplier()

    def window_ci_solar(self):
        return (0.45 * self.windows_area *
                self.window_shading *
                self.cool_solar *
                self.window_sghc)

    def cooling_usage(self):
        if self.cool_efficiency() <= 0:
            return 0
        else:
            return (self.load_from_ua() + self.internal_gains() +
                self.window_ci_solar()) * self.cool_tstat_adjust() / 3412 / self.cool_efficiency()
