# SMS-LogAlert

Allows a user to alert on keywords from alert genrated from logs like IPtables and sends a SMS message to users using SMTP.

[*] Logic:
- Performs simple check on supplied pass and user
- Opens up log and checks for keyword and strips out Source IP
- Sends SMS and clears log file
- Places the IP in a list so multiple SMS arnt sent on previous IP's
- Insures max SMS count has not been reached

[*] Features:
- Allows for custom log alerting
- Supports MIME / or even HTML based alerting
- Supports max SMS count
- Sets specfic log file and time between checks


[*]OPTIONS:

-t = Will tell how long between log checks in Secs, defaults to 10 Secs. 

-s = Max SMS texts that can recived before it shuts down, default is 100. 

-e = Set required email addr user, ex ale@email.com

-p = Set required email password

-log = Set a log to parse
