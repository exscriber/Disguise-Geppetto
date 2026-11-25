## Disguise Python API typing stubs

For VS Code use there settings to suppress PyLance whine:

```json
"python.analysis.diagnosticSeverityOverrides": {
    "reportInvalidTypeForm": "none",
    "reportMissingModuleSource": "none",
}
```

### Sidenotes

- Module `.py` files that gets uploaded into `d3 py27 host` can't use type hints nor f-strings:  
  [@disguise-one/designer-pythonapi](https://github.com/disguise-one/designer-pythonapi)
  vite loader sends them as-is without any cleanup...

- Keep track of API changes: https://developer.disguise.one/python-api/api-changes

- Download link for the `d3.pyi` file: https://developer.disguise.one/assets/d3.pyi
