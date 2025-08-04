import numpy as np
import pandas as pd
import os


def CleanCsv(filepath:str):
        df=pd.read_csv(filepath)
        # Clean 'city'
        if 'city' in df.columns:
            df['city'] = df['city'].astype(str).str.lower()

        # Clean 'price'
        if 'price' in df.columns:
            df['price'] = df['price'].replace('Unpriced', np.nan)
            df['price'] = df['price'].astype(str).str.replace('[$,]', '', regex=True)
            df['price'] = pd.to_numeric(df['price'], errors='coerce')

        # Clean 'name'
        if 'name' in df.columns:
            df['name'] = df['name'].astype(str).str.lower()

        # Clean 'address'
        if 'address' in df.columns:
            df['address'] = df['address'].astype(str).str.replace(r'[\n\r]', ' ', regex=True).str.strip()

        # Clean 'asking_price'
        if 'asking_price' in df.columns:
            df['asking_price'] = df['asking_price'].replace(['Unpriced', ''], np.nan)
            df['asking_price'] = df['asking_price'].astype(str).str.replace('[$,]', '', regex=True)
            df['asking_price'] = pd.to_numeric(df['asking_price'], errors='coerce')

        # Clean 'date_added'
        if 'date_added' in df.columns:
            df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')

        # Clean 'days_on_market'
        if 'days_on_market' in df.columns:
            df['days_on_market'] = df['days_on_market'].astype(str).str.replace(' days', '', regex=False)
            df['days_on_market'] = pd.to_numeric(df['days_on_market'], errors='coerce')

        # Clean 'property_type'
        if 'property_type' in df.columns:
            df['property_type'] = df['property_type'].astype(str).str.lower()

        # Clean 'subtype'
        if 'subtype' in df.columns:
            df['subtype'] = df['subtype'].astype(str).str.lower()

        # Clean 'tenancy' and 'brand_tenant'
        for col in ['tenancy', 'brand_tenant']:
            if col in df.columns:
                df[col] = df[col].astype(str).str.lower()
                df[col] = df[col].replace('nan', '')  # Replace string "nan" with empty string

        # Clean 'remaining_term' → 'remaining_term_year'
        if 'remaining_term' in df.columns:
            df['remaining_term_year'] = df['remaining_term'].astype(str).str.replace(' years', '', regex=False)
            df['remaining_term_year'] = pd.to_numeric(df['remaining_term_year'], errors='coerce')
            df.drop('remaining_term', axis=1, inplace=True)

        # Clean 'square_footage'
        if 'square_footage' in df.columns:
            def parse_square_footage(val):
                val = str(val).replace(',', '')
                if '-' in val:
                    try:
                        parts = val.split('-')
                        return (float(parts[0]) + float(parts[1])) / 2
                    except:
                        return np.nan
                try:
                    return float(val)
                except:
                    return np.nan


            df['square_footage'] = df['square_footage'].apply(parse_square_footage)

        # Clean 'net_rentable_sqft'
        if 'net_rentable_sqft' in df.columns:
            df['net_rentable_sqft'] = df['net_rentable_sqft'].astype(str).str.replace(',', '', regex=False)
            df['net_rentable_sqft'] = pd.to_numeric(df['net_rentable_sqft'], errors='coerce')

        # cap_rate → cap_rate_percentage
        if 'cap_rate' in df.columns:
            df.rename(columns={'cap_rate': 'cap_rate_percentage'}, inplace=True)
        if 'cap_rate_percentage' in df.columns:
            df['cap_rate_percentage'] = df['cap_rate_percentage'].astype(str).str.replace('%', '', regex=False)
            df['cap_rate_percentage'] = pd.to_numeric(df['cap_rate_percentage'], errors='coerce')

        # occupancy → occupancy_percentage
        if 'occupancy' in df.columns:
            df.rename(columns={'occupancy': 'occupancy_percentage'}, inplace=True)
        if 'occupancy_percentage' in df.columns:
            df['occupancy_percentage'] = df['occupancy_percentage'].replace('Vacant', np.nan)
            df['occupancy_percentage'] = df['occupancy_percentage'].astype(str).str.replace('%', '', regex=False)
            df['occupancy_percentage'] = pd.to_numeric(df['occupancy_percentage'], errors='coerce')

        # cap_rate → cap_rate_percentage
        if 'pro_forma_cap_rate' in df.columns:
            df.rename(columns={'pro_forma_cap_rate': 'pro_forma_cap_rate_percentage'}, inplace=True)
        if 'pro_forma_cap_rate_percentage' in df.columns:
            df['pro_forma_cap_rate_percentage'] = df['pro_forma_cap_rate_percentage'].astype(str).str.replace('%', '',
                                                                                                              regex=False)
            df['pro_forma_cap_rate_percentage'] = pd.to_numeric(df['pro_forma_cap_rate_percentage'], errors='coerce')

        # Clean 'occupancy_date'
        if 'occupancy_date' in df.columns:
            df['occupancy_date'] = pd.to_datetime(df['occupancy_date'], errors='coerce')

        # Clean 'noi'
        if 'noi' in df.columns:
            df['noi'] = df['noi'].astype(str).str.replace('$', '', regex=False).str.replace(',', '', regex=False)
            df['noi'] = pd.to_numeric(df['noi'], errors='coerce')

        # Clean 'pro_forma_noi'
        if 'pro_forma_noi' in df.columns:
            df['pro_forma_noi'] = df['pro_forma_noi'].astype(str).str.replace('$', '', regex=False).str.replace(',', '',
                                                                                                                regex=False)
            df['pro_forma_noi'] = pd.to_numeric(df['pro_forma_noi'], errors='coerce')

        # Clean 'price_sqft'
        if 'price_sqft' in df.columns:
            df['price_sqft'] = df['price_sqft'].astype(str).str.replace('$', '', regex=False)
            df['price_sqft'] = pd.to_numeric(df['price_sqft'], errors='coerce')

        # lease_term → lease_term_year
        if 'lease_term' in df.columns:
            df.rename(columns={'lease_term': 'lease_term_year'}, inplace=True)
        if 'lease_term_year' in df.columns:
            df['lease_term_year'] = df['lease_term_year'].astype(str).str.replace('years', '', case=False,
                                                                                  regex=False).str.strip()
            df['lease_term_year'] = pd.to_numeric(df['lease_term_year'], errors='coerce')

        # remaining_term_years (already handled above if 'remaining_term' was present)

        # lease_expiration
        if 'lease_expiration' in df.columns:
            df['lease_expiration'] = pd.to_datetime(df['lease_expiration'], errors='coerce')

        # lease_commencement
        if 'lease_commencement' in df.columns:
            df['lease_commencement'] = pd.to_datetime(df['lease_commencement'], errors='coerce')

        # Clean 'price_acre_land_value' → keep only numeric value, remove $ and text, convert to float
        if 'price_acre_land_value' in df.columns:
            df['price_acre_land_value'] = (
                df['price_acre_land_value']
                .astype(str)
                .str.extract(r'([\d,\.]+)')[0]  # Extract the numeric part
                .str.replace(',', '', regex=False)
            )
            df['price_acre_land_value'] = pd.to_numeric(df['price_acre_land_value'], errors='coerce')

        # Clean 'price_sqft_land_value' → remove $, /SqFt, convert to float
        if 'price_sqft_land_value' in df.columns:
            df['price_sqft_land_value'] = (
                df['price_sqft_land_value']
                .astype(str)
                .str.extract(r'([\d,\.]+)')[0]
                .str.replace(',', '', regex=False)
            )
            df['price_sqft_land_value'] = pd.to_numeric(df['price_sqft_land_value'], errors='coerce')

        # Clean 'air_rights_sqft' → remove commas, convert to float
        if 'air_rights_sqft' in df.columns:
            df['air_rights_sqft'] = df['air_rights_sqft'].astype(str).str.replace(',', '', regex=False)
            df['air_rights_sqft'] = pd.to_numeric(df['air_rights_sqft'], errors='coerce')

        # print("storing in csv")
        # df.to_csv(f'data/Cleaned_{filepath}', index=False)
        print("storing in csv")
        filename_only = os.path.basename(filepath)
        cleaned_path = os.path.join("data", f"Cleaned_{filename_only}")
        df.to_csv(cleaned_path, index=False)
