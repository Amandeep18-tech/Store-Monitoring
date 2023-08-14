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

## Future Scope

As the project evolves, there are opportunities for further enhancement and refinement. One key area of focus for future development is the handling of continuous data updates.

### Incremental Data Updates

Currently, the initial data load has been successfully implemented. However, as the dataset undergoes updates on an hourly basis, there is a need to incorporate a mechanism for efficiently updating the database with the most recent data.

To address this, the following approach will be taken:

1. **Hourly Data Updates:** Implement a scheduled job or script that runs at regular intervals (e.g., every hour) to fetch and process the latest data changes.

2. **SQL Insert Ignore:** Utilize the `INSERT IGNORE` SQL statement to insert new data rows into the database. This statement will ensure that only unique rows are inserted, preventing duplicate entries.

3. **Primary Key and Uniqueness:** Define a set of columns as a composite primary key or unique constraint. This selection should be based on the characteristics of the data that ensure uniqueness and accurate identification of rows.

By following these steps, the system will be able to efficiently manage the ongoing updates to the dataset without compromising data integrity or database performance.

### Benefits of Future Enhancements

Implementing the above future scope will provide several benefits:

- **Real-time Updates:** The system will stay up-to-date with the latest data changes, enabling users to access the most current information.

- **Efficient Utilization:** By employing `INSERT IGNORE` and well-defined primary key constraints, the database updates will be streamlined, reducing the processing time and resources required for data updates.

- **Data Integrity:** The chosen unique identifier columns will ensure that the correct data is being updated while maintaining data integrity.

- **Scalability:** With a well-structured update mechanism, the system can easily accommodate increased data volumes and update frequencies in the future.

Incorporating these enhancements will further solidify the system's ability to handle continuous data updates, providing a robust and reliable foundation for ongoing data management and analysis.
