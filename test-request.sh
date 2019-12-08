#!/bin/sh
curl -H X-Hub-Signature:dummy -X POST http://localhost:8000/webhook/github/pullrequest -d @tests/sample-webhook/sample-pr-open.json
echo "RESULT=[$?]"