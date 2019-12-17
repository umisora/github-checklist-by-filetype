#!/bin/sh
JSONFILE=$1
echo $JSONFILE
curl -H X-Hub-Signature:dummy -X POST http://localhost:8000/webhook/github/pullrequest -d @${JSONFILE}
echo "RESULT=[$?]"