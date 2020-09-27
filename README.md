# information_extraction

# Information extraction using rule_based_method

## Request

API is at /api/v1/extract/
It requires multipart form data

Refer to testscript.py for clarification.

## Response
Response is of the format:

```json
{
    "data": <data>,
    "message": "",
    "status_code": 200,
    "meta_data": {"deltatime": <deltatime>},
}
```

The data is a list of json with each json of the format:

```json
{
    "date": {
        "text": "2012/12/12",
        "bbox": [x0, y0, x2, y2],        
    },
    "email":{
        "text": "sample@mail.com",
        "bbox": [x0, y0, x2, y2],
    }
}
``` 

## Example
```json
{
    "data": [
        {
            "email": {
                "bbox": [60,391,119,13
                ],
                "text": "client@example.net"
            }
        },
        {
            "email": {
                "bbox": [60,507,120,13
                ],
                "text": "office@example.net"
            }
        },
        {
            "date": {
                "bbox": [634,353,69,13
                ],
                "text": "12/12/2001"
            }
        }
    ],
    "message": "data found",
    "meta_data": {
        "deltatime": 2.44
    },
    "status_code": 200
}

```