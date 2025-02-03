# Subdomain Extraction Script

## Overview

**New features will be added gradually. Continuous updates in progress!**

#### Usage

````bash
python test.py --domain DOMAIN -m {1,2} [-o OUTPUT_FILE]
````



#### Arguments

````bash
--domain DOMAINSpecify the domain to query, e.g., baidu.com.

-m {1,2}Choose the extraction mode:

1 - Returns full URLs (e.g., http://example.example.com).

2 - Returns only subdomain prefixes (e.g., example).

-o OUTPUT_FILE (Optional)Specify an output file to save the results.
````



#### Example Usage

**Extract full URLs:**

````bash
python test.py --domain baidu.com -m 1

Extract subdomain prefixes and save to a file:

python test.py --domain baidu.com -m 2 -o output.txt
````

#### Error Handling

If the script encounters an issue fetching data, it will display a Failed message.

Ensure you have internet access and that the specified domain is valid.
