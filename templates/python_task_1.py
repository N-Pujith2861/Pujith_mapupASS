import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    data=pd.read_csv('dataset-1.csv')
    df = pd.DataFrame(data)
    car_matrix = df.pivot_table(index='id_1', columns='id_2', values='car')
    car_matrix.fillna(0, inplace=True)
    for i in range(len(car_matrix)):
        car_matrix.iloc[i, i] = 0
    return car_matrix

def get_type_count(df)->dict:
    df['car_type'] = pd.cut(df['car'], bins=[0, 15, 25, 100], labels=['low', 'medium', 'high'])
    car_type_count = df['car_type'].value_counts().sort_index()
    return car_type_count.to_dict()


def get_bus_indexes(df)->list:
    mean_bus = df['bus'].mean()
    twice_mean_bus = 2 * mean_bus
    bus_indexes = df[df['bus'] > twice_mean_bus].index.to_list()
    bus_indexes.sort()
    return bus_indexes


def filter_routes(df)->list:
    avg_truck_by_route = df.groupby('route')['truck'].mean()
    routes_with_high_avg_truck = avg_truck_by_route[avg_truck_by_route > 7].index.to_list()
    routes_with_high_avg_truck.sort()
    return routes_with_high_avg_truck

def multiply_matrix(matrix)->pd.DataFrame:
    df[df > 20] *= 0.75
    df[df <= 20] *= 1.25
    return df.round(1)

def time_check(df)->pd.Series:
    expected_duration = timedelta(days=7, hours=24)
    expected_days = set(range(7))

    def is_valid_time(row):
        # Convert timestamps to datetime objects
        start_time = datetime.strptime(f"{row['startDay']} {row['startTime']}", "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(f"{row['endDay']} {row['endTime']}", "%Y-%m-%d %H:%M:%S")

        # Check duration and days covered
        duration = end_time - start_time
        covered_days = set(range(start_time.weekday(), (end_time + timedelta(days=1)).weekday()))

        return duration == expected_duration and covered_days == expected_days

    # Apply the check to each row and return a boolean series with multi-index
    return df.apply(is_valid_time, axis=1).rename('incorrect_timestamps')
df = pd.read_csv("dataset-2.csv")
incorrect_timestamps = time_check(df.copy())
print(incorrect_timestamps)
