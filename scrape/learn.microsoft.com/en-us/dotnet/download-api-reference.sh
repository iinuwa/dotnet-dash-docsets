#!/bin/sh

wget --recursive --no-clobber --page-requisites  --html-extension --convert-links --domains learn.microsoft.com --no-parent 'https://learn.microsoft.com/en-us/dotnet/api/'
