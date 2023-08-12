# Store Status and Historical Data Processing

This README provides an overview of the process used to manipulate and transform data from three tables: `store_status`, `menu_hours`, and `store_timezone`, to create a `store_status_within_hours` table and generate historical data for further analysis. The steps described below are designed to ensure data consistency, facilitate comparisons, and create a useful dataset.

## Table Descriptions

1. **store_status**: Contains information about the status of a store, including `store_id`, `status`, and `timestamp_utc`.

2. **menu_hours**: Stores the operating hours of a store, with fields `store_id`, `day`, `start_time_local`, and `end_time_local`.

3. **store_timezone**: Holds the time zone information for each store, denoted by `store_id` and `timezone_str`.

## Steps

### 1. Consistent Timestamps

To enable accurate comparisons across tables, the UTC timestamps in the `store_status` table are converted to local time using the table `store_timezone`

### 2. Day Number Calculation

For the purpose of comparison, the local datetime from `store_status` is used to calculate the day number, which is then saved in a new column.

### 3. Store Start and End Times

Matching records from `store_status` and `menu_hours` based on `store_id` and `day`, the store start and end times are extracted and stored in `store_status`.

### 4. Creating `store_status_within_hours`

A new table, `store_status_within_hours`, is generated using the following query:
```sql
CREATE TABLE store_status_within_hours AS
    SELECT store_id, status, local_time, start_time_local, end_time_local, custom_day_number
    FROM store_status
    WHERE local_time < end_time_local AND local_time > start_time_local;
```

### 5. Generating Historical Data

A `historical_data` table is constructed with fields `store_id`, `start_time`, `end_time`, and `status`. This table accounts for the logic that the initial entry's status from the start time to that point is considered, and subsequent entries' time intervals determine their respective statuses. The last entry for each day retains the status until the end time.

### 6. CSV Export

A CSV file can be generated from the `historical_data` table. The time limit for the dataset is '2023-01-25 14:13:22', ensuring that all data within this timeframe is captured.

### 7. Using Celery for API Trigger and Polling Architecture

Celery is utilized to facilitate API triggers and implement a polling architecture, allowing for efficient data processing and management.

## Conclusion

By following these steps, you can achieve consistent timestamp handling, effective data comparison, historical data generation, and CSV export. The process outlined here enhances data analysis capabilities and supports further exploration of store status and operating hours over time.