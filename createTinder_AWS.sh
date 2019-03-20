#!/usr/bin/env bash

aws lambda invoke --function-name CreateTinderPDF --invocation-type Event \
--payload file://inputfile_createtinder.txt outfile_createTinderPDF.txt
