#!/bin/bash

API_URL="http://localhost:8000/api/logs/access/"
ACCESS_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ2MzEyMTM4LCJpYXQiOjE3NDYzMDg1MzgsImp0aSI6ImMxMTFmNGU1MGMyODRiMTU4YzBkNTEyZDVmZjMyZTEwIiwidXNlcl9pZCI6M30.voWXBWCvH0ylcCKBzagOFpJM44hjaz4fsCtNCDDfKbk"

curl -X POST "$API_URL" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2025-04-14T13:57:02Z",
    "username": "Mellisa Dsilva",
    "Dept_ID": 7,
    "Dept_Name": "IT",
    "access_level": "Manager",
    "system": "payroll database",
    "message": "File Download attempt on admin panel",
    "action": "Password Reset",
    "ip_address": "192.168.4.8",
    "device": "Laptop",
    "location": "Mumbai"
}'
