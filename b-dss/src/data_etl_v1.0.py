import os
import glob
import random
import pandas as pd
import psycopg2 as pg

dir_path = './static/data/csv_20250930'
file_out = 'dss_vis_data_scenario1.csv'

# db connnection info
db_host = 'gistdrupaldev3.ornl.gov'
db_user = input("Enter username for db: ")
db_pw = input("Password: ")
db_name = 'bt23'
db_port = '5432'

# data info
table_budget = 'es.bsc090ctybudgetb_2030'
table_carbon = 'es.bsc090ctycarbon_2030'
table_economic = 'es.bsc090ctyeconomic_2030'
table_production = 'es.bsc090ctyproduction_2030'
table_quantity = 'es.bsc090ctyquantity_2030'

field_res_ins_proxy = 'insurance'
field_tot_seq = 'totalccc'
field_profit = 'avg_per_acre_profit'
field_efficiency = 'yeild'
field_prod = 'production'
field_energ_pot = 'btu_ton'
field_nutrient_pollution = 'lbs_n + lbs_p + lbs_k'

engine = pg.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_pw,
            port=db_port)

sql_budget = f"""SELECT subclass, fips, sum({field_res_ins_proxy}) as res_ins_proxy 
FROM {table_budget} bc
group by subclass, fips"""

sql_carbon = f"""SELECT subclass, fips, sum({field_tot_seq}) as tot_seq
FROM {table_carbon} bc  
group by subclass, fips"""

sql_economic = f"""SELECT subclass, fips, sum({field_profit}) as profit
FROM {table_economic} bc 
group by subclass, fips"""

sql_production = f"""SELECT subclass, fips, sum({field_energ_pot}) as prod, sum({field_efficiency}) as efficiency, sum({field_energ_pot} * {field_energ_pot}) as energ_pot
FROM {table_production} bc  
group by subclass, fips"""

sql_quantity = f"""SELECT subclass, fips, sum({field_nutrient_pollution}) as nutrient_pollution 
FROM {table_quantity} bc 
group by subclass, fips"""

sql_list = [sql_budget, sql_carbon, sql_economic, sql_production, sql_quantity]

# save sql output to local directory
for sql in sql_list:
    df = pd.read_sql_query(sql, con=engine)
    df.to_csv(os.path.join(dir_path, sql))

# load regions file
df_reg = pd.read_csv('./static/data/fips_regions.csv')

# iterate through local files, transform, and merge
df_all = pd.DataFrame()
count = 1
for file_path in os.listdir(dir_path):
    df = pd.read_csv(os.path.join(dir_path, file_path), dtype={'fips':int})
    if count == 1:
        df_all = pd.concat([df_all,df])
    else:
        df_all = df_all.merge(df, how='outer', on=['subclass','fips'])
    count += 1

# df_all = df_all.merge(df_reg, how='left', on='fips')

# Parameter not yet featured in models, so populate with placeholder data
df_all['Rural Prosperity'] = [random.randint(0, 100) for _ in range(len(df_all))]

# clean up data types
for col in list(df_all.columns.values):
    try:
        print(df[col].dtype)
        df[col] = df[col].astype(int)
        print(df[col].dtype)
    except:
        pass

# save output
df_all.to_csv(file_out,index=False)
    