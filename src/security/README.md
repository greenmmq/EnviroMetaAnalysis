`creds.json` is ignored, but should live here on the localhost machine since it provides URI credentials for the MongoDB. It also provides an email to adhere to the polite request rules of OpenAlex. 

`creds.json` has the following schema:

```json
{
  "email":"str",
  "uid":"str",
  "pwd":"str",
  "server":"str"
}
```
