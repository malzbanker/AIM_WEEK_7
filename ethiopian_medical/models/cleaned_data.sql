
SELECT
    id,
    text,
    date,
    views,
    media_type
FROM raw_data
WHERE text IS NOT NULL