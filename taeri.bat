@echo off
if "%1" == "" (
    python taeri__taeri.py
) else (
    python taeri__taeri.py %1 %2 %3 %4 %5 %6 %7 %8 %9
)