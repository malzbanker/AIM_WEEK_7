{{ config(schema='staging', materialized='view') }}

SELECT
    message_id,
    channel,
    date::TIMESTAMP AS message_date,
    TRIM(text) AS text,
    image_path
FROM public.raw_messages
WHERE text IS NOT NULL