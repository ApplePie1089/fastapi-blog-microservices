#!/bin/bash
while ! </dev/tcp/localhost/80; do sleep 1; done;