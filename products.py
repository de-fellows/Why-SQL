import sqlite3
import random as rd
import numpy as np


specialized_sizes = [' S1', ' S2', ' S3', ' S4', ' S5', ' S6']

specialized_bikes = ['2023 Specialized Enduro Comp', '2023 Specialized Enduro Expert', '2023 Specialized Stumpjumper Evo Expert', '2023 Specialized Stumpjumper Evo Comp']

specialized_msrps = [6999.00, 8999.00, 8499.00, 6499.00]    # Source: https://www.specialized.com/ca/en/shop/bikes/mountain-bikes/trail-bikes/c/mountaintrail

all_specialized_msrps = list(np.repeat(specialized_msrps, len(specialized_sizes)))

all_specialized_assumed_costs = [round(0.55 * i, 2) for i in all_specialized_msrps]

all_specialized_bikes = [bike + size for bike in specialized_bikes for size in specialized_sizes]   # Computing the Cartesian Product to get all bikes in all sizes 


bike_sizes = [' XS', ' S', ' M', ' L', ' XL', ' XXL']

rocky_spec_levels = [' A30', ' A50', ' C50', ' C70']

rocky_mountain_bike = '2023 Rocky Mountain Altitude'

rocky_mountain_msrps = [4499.00, 5219.00, 6819.00, 8529.00]     # Source: https://ca.bikes.com/collections/altitude

all_rocky_mountain_msrps = list(np.repeat(rocky_mountain_msrps, max(len(bike_sizes), len(rocky_spec_levels))))

all_rocky_mountain_costs = [round(0.55 * i, 2) for i in all_rocky_mountain_msrps]

all_rocky_mountain_bikes = [rocky_mountain_bike + spec + size for spec in rocky_spec_levels for size in bike_sizes] # Computing the cartesian product for all bikes of all spec levels in all sizes


trek_spec_levels = [' 7', ' 8', ' 9.7', ' 9.8', ' 9.9']

trek = '2023 Trek Slash'

all_trek_bikes = [trek + spec + size for spec in trek_spec_levels for size in bike_sizes] # Computing the cartesian product for all bikes of all spec levels in all sizes]

trek_msrps = [4499.99, 4549.99, 5449.99, 7999.99, 10999.99]     # Source: https://www.trekbikes.com/ca/en_CA/bikes/mountain-bikes/trail-mountain-bikes/slash/c/B341/

all_trek_msrps = list(np.repeat(trek_msrps, max(len(bike_sizes), len(trek_spec_levels))))

all_trek_costs = [round(0.55 * i, 2) for i in all_trek_msrps]

all_bikes = all_specialized_bikes + all_rocky_mountain_bikes + all_trek_bikes


# Now Accessories 

accessory_colours = [' Black', ' Silver', ' Red', ' Orange', ' Green', ' Blue', ' Purple']

accessories = ['Bicycle Bell', 'Pedals', 'Water Bottle', 'Water Bottle Cage']

accessory_msrps = [19.99, 75.00, 14.99, 21.99]

all_accessory_msrps = list(np.repeat(accessory_msrps, max(len(accessories), len(accessory_colours))))

all_accessory_costs = [round(0.4 * i, 2) for i in all_accessory_msrps]

all_accessories = [accessory + colour for accessory in accessories for colour in accessory_colours]

all_products = all_bikes + all_accessories

all_msrps = all_specialized_msrps + all_rocky_mountain_msrps + all_trek_msrps + all_accessory_msrps

all_costs = all_specialized_assumed_costs + all_rocky_mountain_costs + all_trek_costs + all_accessory_costs

universal_product_codes = []
quantities = []

for i in range(len(all_products)):
    upc = rd.randint(100000000000, 999999999999)    # Unique 12 digit product code
    quantity = rd.randint(0, 10)    # Quantity of Item

    while upc in universal_product_codes:           # Ensures uniqueness
        upc = rd.randint(100000000000, 999999999999)

    universal_product_codes.append(upc)

    quantities.append(quantity)
    
connection = sqlite3.connect('bikeshop.sqlite')

cursor = connection.cursor()


cursor.execute("DROP TABLE Products")
cursor.execute("CREATE TABLE Products(UPC INT, Description TEXT,Quantity INT, MSRP REAL, Cost REAL, PRIMARY KEY (UPC))")

for i in range(len(all_products)):
    cursor.execute("INSERT INTO Products VALUES(?,?,?,?,?)", (universal_product_codes[i], all_products[i], quantities[i], all_msrps[i], all_costs[i]))

connection.commit()
connection.close()