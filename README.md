# Store Status and Historical Data Processing

This README serves as a comprehensive guide to manipulating and transforming data from three key tables: `store_status`, `menu_hours`, and `store_timezone`. The goal is to generate a `store_status_within_hours` table and derive historical data for more comprehensive analysis. Each step has been thoughtfully crafted to ensure data consistency, facilitate comparisons, and yield an informative dataset.

## Table Descriptions

1. **store_status**: This table contains crucial information about the status of each store, including fields such as `store_id`, `status`, and `timestamp_utc`.

2. **menu_hours**: Essential operating hours for every store are stored within this table, featuring columns such as `store_id`, `day`, `start_time_local`, and `end_time_local`.

3. **store_timezone**: Vital time zone details for each store are captured here, indicated by `store_id` and `timezone_str`.

## Steps

### 1. Addressing Missing Store Timezones

To ensure data completeness, we address any gaps in the `store_timezone` table. By comparing `store_status` and `store_timezone`, we identify distinct `store_id` values that are absent in the latter. These missing `store_id` entries are then inserted into the `store_timezone` table, with the default time zone set to 'America/Chicago'.

### 2. Handling Missing Store Operating Hours

In a similar vein, we address any missing records in the `menu_hours` table. By comparing `store_status` and `menu_hours`, we pinpoint unique `store_id` values that are absent in the `menu_hours` table. These missing `store_id` entries are added to the `menu_hours` table, indicating 24/7 availability.

### 3. Consistent Timestamps

To facilitate accurate cross-table comparisons, the UTC timestamps in the `store_status` table are converted to local time using `store_timezone`

### 4. Day Number Calculation

For effective comparisons, the local datetime from `store_status` is harnessed to calculate the day number, which is subsequently stored in a new column.

### 5. Store Start and End Times

Records from `store_status` and `menu_hours` are matched based on `store_id` and `day`, enabling the extraction and storage of store start and end times within the `store_status` table.

### 6. Creating `store_status_within_hours`

A new table, `store_status_within_hours`, is forged using the following query:
```sql
CREATE TABLE store_status_within_hours AS
    SELECT store_id, status, local_time, start_time_local, end_time_local, custom_day_number
    FROM store_status
    WHERE local_time < end_time_local AND local_time > start_time_local;
```

### 7. Generating Historical Data

A `historical_data` table is generated, equipped with fields like `store_id`, `start_time`, `end_time`, and `status`. This table adheres to the logic that the initial entry's status from the start time until the next entry is considered, while the time interval between successive entries determines their respective statuses. The last entry for each day retains its status until the end time. This method returns the status for each interval without any overlapping intervals.

### 8. CSV Export with Uptime and Downtime Calculation

A CSV file can be efficiently generated from the `historical_data` table. Additionally, the following query can be executed to calculate the uptime and downtime within a specified interval for a particular status:
```sql
SELECT 
    store_id,
    SUM(TIMESTAMPDIFF(SECOND, GREATEST({time_interval}, start_time), LEAST(end_time, "{current_time}"))) AS uptime 
FROM historical_data
WHERE status = "{status}"
AND start_time < "{current_time}"
AND end_time > {time_interval}
GROUP BY store_id;
```

### 9. Celery for API Trigger and Polling Architecture

The implementation of Celery streamlines API triggers and enforces a polling architecture, optimizing data processing and management.

## Conclusion

Following these meticulously outlined steps empowers you to achieve uniform timestamp handling, streamlined data comparison, comprehensive historical data generation, and efficient CSV export. This process significantly enhances data analysis capabilities, supporting deeper exploration of store status and operating hours over a specified timeframe, alongside uptime and downtime calculations for a specific status.