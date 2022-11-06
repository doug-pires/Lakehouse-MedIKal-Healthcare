
-- Only Current Events to my Power BI Dashboard.
-- Other events are CAPTURED on Event Hub

WITH ndc_table AS (
    SELECT
    ndc
    ,qty
    ,CAST ( date_distribution AS DATETIME ) date_distribution
    ,CAST ( CONCAT ( DATEPART ( year, System.Timestamp() ) , '-' , DATEPART ( month, System.Timestamp() ), '-',DATEPART ( day, System.Timestamp() ) ) AS DATETIME ) t 
    FROM
        [eh-topicdemo-92]
 
    )

SELECT
n.ndc
,SUM(n.qty) TotalMedicines
INTO [query-medicines-powerbi] 
FROM ndc_table n
WHERE date_distribution = t
GROUP BY n.ndc, TumblingWindow(second,30)


