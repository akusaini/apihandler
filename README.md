# Apihandler


## Prerequisite

Build the virtual environment in the root of project.
```python
virtualenv -p python3 .environment
source .environment/bin/activate
pip install -r requirement.txt
```

For simplicity settings for the development, production environment are put in the dev.py and prod.py
respectively at the path **_/apibuilder/apibuilder/<dev.py or prod.py>._** All the django related settings 
are maintained in the settings.py at the same location.

For running the project in the production environment. Use 
```commandline
export MODE == "DEVELOPMENT"
```

Replace the cache settings in the dev.py or prod.py accordingly.

## Http Rest response

All the rest request are sharing the common format as given in sample response.

```json
{
  "message": "Bad request.",
  "error": [{
      "error_code": "BAD_REQUEST",
      "message": "Given fields are not present. Hence aborting",
      "fields": [["country", "category"]]
      }],
  "success": false,
  "data": null
 }
```

Every rest response contains 4 field:-
* message : It is the most human readable format who want's to consumne the api.
* success : If any of the error is encountered success would be false else true otherwise.
* error : error is the array of object each containg 3 fields. **_error_code_** describe the HTTP error code returned by the api.
 **_message_** describe the error raised by the system else it can also be the custom error as handled
 by developers. **_fields_** describe the fields responsible for raising the error.
* data : data contains the payload returned by the API.

