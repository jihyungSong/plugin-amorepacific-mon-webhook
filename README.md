# plugin-amorepacific-monitoring-webhook
Webhook Plugin for Amore-pacific
# Data Model

## Amore Pacific Raw Data Examples
~~~
{
   "metric_name": "Transaction Rollback",
   "summary": "summary",
   "status": "DOWN",
   "conditionlog": "[Wait For Element to Editable Time Out.\nPage Info ",
   "threshold": "igvnprd",
   "event_id": "32222039",
   "urgency": "2",
   "severity": "주의",
   "event_time": "2021-06-25 03:32:45",
   "metric_value": "Rollback > 0 Count/s, 0 Count/s]"
      
}
~~~

| Field 	| Type |Example |
| ---   	|---|   ---     |
| metric_name |str| Transaction Rollback | 
| summary   | str  | summary  |
| status  	| str   | UP / DOWN |
| conditionlog	|  str | Wait For Element to Editable Time Out.\nPage Info |
| event_id	|  str  | 32222039	|
| urgency	| str |	0 or 1 |
| severity	| str | 주의 / 해제 / 경고 / 심각 |
| event_time	| datetime | 2021-06-25 03:32:45 |
| metric_value	| str | "Rollback > 0 Count/s, 0 Count/s]" |
| resource_name	| str | WAS-xxx.xx.xxx.xxx |



## SpaceONE Event Model

| Field		| Type | Description	| Example	|
| ---      | ---     | ---           | ---           |
| event_id | str  | auto generation | event-1234556  |
| event_key | str | fingerprint | 469fd6fbb9dbabaa |
| event_type | str | RECOVERY , ALERT based on `raw_data.state` | RECOVERY	|
| title | str	| `raw_data.annotations.summary`	| Pod has been in a non-ready state for more than 15 minutes.	|
| description | str | `raw_data.annotations.description`	| Pod prometheus/prometheus-xxx has been in a non-ready state for longer than 15 minutes.|
| severity | str  | alert level based `raw_data.alert.labels.severity (critical : CRITICAL / error : ERROR / warning: WARNING / info: INFO ` | ERROR |
| resource | dict | resource which triggered this alert	| ` {'pod':'prometheus-prometheus-node-exporter-xp6jv','alertname': 'KubePodNotReady'}` |
| raw_data | dict | Prometheus webhook received  data structure | - |
| addtional_info | dict | `raw_data.alert.annotations` / `raw_data.alert.generatorURL`, `raw_data.alert.endsAt` | `{"org_id": "1.0", "rule_url" "https://...." }` |
| occured_at | datetime | prometheus alert triggered time , `alert.startsAt` | `2021-10-12T04:13:01.794Z`|
| alert_id | str | mapped alert_id	| alert-3243434343 |
| webhook_id | str  | webhook_id	| webhook-34324234234234 |
| project_id | str	| project_id	| project-12312323232    |
| domain_id | str	| domain_id	| domain-12121212121	|
| created_at | datetime | webhook alert created time | "2021-08-23T06:47:32.753Z"	|

