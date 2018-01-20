#!/bin/bash

export MEDICOVER_USERNAME=""        # Medicover card number
export MEDICOVER_PASSWORD=""        # Password for Medicover on-line
export MEDICOVER_REGION=""          # Appointment region code (number)
export MEDICOVER_SPECIALIZATION=""  # Appointment specialization code (number)
export MEDICOVER_CLINIC="-1"        # Appointment clinic code (number or -1 for any)
export MEDICOVER_DOCTOR="-1"        # Appointment doctor code (number or -1 for any)

# Makers webhook key for IFTTT notifications (https://ifttt.com/maker_webhooks)
export IFTTT_KEY=""
export CHECK_EVERY_SEC=66

watch -n "${CHECK_EVERY_SEC}" python 'medicover_slots.py'
