#!/usr/bin/env bash

# POST , with path of json_file
ab -n 1 -c 1 -v 4 -H "token: 123" -p api_data.json -T "application/json" {API}
ab -n 1000 -c 100 -H "token: 123" -p {file_path} -T "application/json" {API}



# POST with data
curl -d "{\"user_id\":1}" -H "Content-Type: application/json" -H "token: 123" -i -v {API}


# GET
ab -n 1 -c 1 -v 4 {API}
ab -n 1000 -c 100 -H "token: 123" -p {file_path} -T "application/json" {API}
