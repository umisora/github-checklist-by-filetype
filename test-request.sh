#!/bin/sh
JSONFILE=$1
echo $JSONFILE
curl -H X-Hub-Signature:dummy -H X-GitHub-Event:pull_request -X POST http://localhost:8000/webhook/github?token=dummy -d @${JSONFILE}
echo "RESULT=[$?]"
