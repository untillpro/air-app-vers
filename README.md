# air-app-vers

- Ref. https://github.com/untillpro/airs-design/blob/main/uspecs/specs/devops/release/app-vers--td.md

## Run tests

```bash
# Install dependencies
pip install coverage pyyaml lingua-language-detector

# Run tests
python scripts/validate.py

# Or, run tests with coverage and generate a report
coverage run --source=scripts -m unittest discover scripts -v
coverage run --source=scripts -a scripts/validate.py
coverage html
```

## Manual validate

```bash
./validate.sh
```
