#!/bin/sh

echo "export SENDGRID_API_KEY='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'" > sendgrid.env
echo "sendgrid.env" >> .gitignore
. ./sendgrid.env