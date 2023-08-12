# Store Status and Historical Data Processing

This README provides a comprehensive guide to manipulating and transforming data from three tables: `store_status`, `menu_hours`, and `store_timezone`. The aim is to create a `store_status_within_hours` table and generate historical data for more in-depth analysis. Each step is meticulously designed to ensure data consistency, streamline comparisons, and generate a valuable dataset.

## Table Descriptions

1. **store_status**: This table contains vital information about the status of a store, including fields such as `store_id`, `status`, and `timestamp_utc`.

2. **menu_hours**: Crucial operating hours for each store are stored in this table, featuring columns like `store_id`, `day`, `start_time_local`, and `end_time_local`.

3. **store_timezone**: Pertinent time zone details for each store are captured here, indicated by `store_id` and `timezone_str`.

## Steps

### 1. Addressing Missing Store Timezones

To ensure data completeness, we address any missing entries in the `store_timezone` table. By comparing `store_status` and `store_timezone`, we identify distinct `store_id` values that are absent in the latter. These missing `store_id` entries are then inserted into the `store_timezone` table with the default time zone 'America/Chicago'.

### 2. Handling Missing Store Operating Hours

Similarly, for data integrity, we handle any missing records in the `menu_hours` table. Through a comparison of `store_status` and `menu_hours`, we identify unique `store_id` values that are not present in the `menu_hours` table. These missing `store_id` entries are inserted into the `menu_hours` table, reflecting a 24/7 availability timeframe.

### 3. Consistent Timestamps

To facilitate accurate comparisons across tables, the UTC timestamps in the `store_status` table are converted to local time using `store_timezone`. 

### 4. Day Number Calculation

For effective comparison, the local datetime from `store_status` is employed to calculate the day number, which is subsequently saved in a new column.

### 5. Store Start and End Times

Records from `store_status` and `menu_hours` are matched based on `store_id` and `day`, extracting and storing store start and end times within the `store_status` table.

### 6. Creating `store_status_within_hours`

A new table, `store_status_within_hours`, is created using the query:
```sql
CREATE TABLE store_status_within_hours AS
    SELECT store_id, status, local_time, start_time_local, end_time_local, custom_day_number
    FROM store_status
    WHERE local_time < end_time_local AND local_time > start_time_local;
```

### 7. Generating Historical Data

A `historical_data` table is generated, featuring fields such as `store_id`, `start_time`, `end_time`, and `status`. This table adheres to the logic that the initial entry's status from the start time until the next entry is considered, while the time interval between successive entries determines their respective statuses. The last entry for each day retains its status until the end time. Since we are only considering, successive timelines, the overlapping would be not an issue.

### 8. CSV Export

A CSV file can be efficiently generated from the `historical_data` table. The dataset's time limit is set at '2023-01-25 14:13:22' to ensure comprehensive data capture.

### 9. Celery for API Trigger and Polling Architecture

The implementation of Celery streamlines API triggers and enforces a polling architecture, optimizing data processing and management.

## Conclusion

Following these meticulously outlined steps empowers you to achieve uniform timestamp handling, streamlined data comparison, comprehensive historical data generation, and efficient CSV export. This process significantly enhances data analysis capabilities, supporting deeper exploration of store status and operating hours over a specified timeframe.
