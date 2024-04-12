# Type Inferencing

The type inference in this project is built based on `BaseConvertStrategy`, which has the following methods:

- `is_applicable`: quickly checks if the strategy is applicable for the given column before running the conversion
- `get_compatibles`: this method is cached and returns the compatible types for the given column
  after running the conversion
- `convert`: converts the column to the inferred type or return cached data
- `get_type`: returns the inferred type of the column

The process will run through all the available strategies and return the highest compatible type. Furthermore,
the datatypes will be downcasted to the lowest possible type to ensure the performance and memory usage.

**NOTE**: For large datasets, an extra step of chunking the data is added to ensure the performance and reliability
of the system.

## Techniques Used

The following table shows the techniques used for type inferencing:

| Data Types  | Pre-check                        | Techniques                           | Description                                                                   |
|-------------|----------------------------------|--------------------------------------|-------------------------------------------------------------------------------|
| `int`       | Already int or str               | `pandas.to_numeric`                  | [numeric.py](../../apps/backend/type_inference/strategies/numeric.py)         |
| `float`     | Already float or str             | `pandas.to_numeric`                  | [numeric.py](../../apps/backend/type_inference/strategies/numeric.py)         |
| `bool`      | Contains truthy and falsy values | prepare custom binary data, then map | [boolean.py](../../apps/backend/type_inference/strategies/boolean.py)         |
| `datetime`  | Try to convert head              | `pandas.to_datetime`                 | [datetime.py](../../apps/backend/type_inference/strategies/datetime.py)       |
| `category`  | Count uniques and not datetime   | `pandas.Categorical`                 | [categorical.py](../../apps/backend/type_inference/strategies/categorical.py) |
| `complex`   | Try to convert head              | `pandas.astype(complex)`             | [complex.py](../../apps/backend/type_inference/strategies/complex.py)         |
| `timedelta` | Try to convert head              | `pandas.to_timedelta`                | [timedelta.py](../../apps/backend/type_inference/strategies/timedelta.py)     |
| `object`    | Last option                      |                                      | Converts the column to object type                                            |