#!/usr/bin/env python

echo 'Start batch process'
python3 /UtuberPickup/manage.py regularGetYoutubeComments $1
date
echo 'End batch process'
