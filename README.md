# air-app-vers

- Ref. https://github.com/untillpro/airs-design/blob/main/uspecs/specs/devops/release/app-vers--td.md

## Run tests

```bash
python -m unittest discover scripts -v
pip install coverage
coverage run -m unittest discover scripts
coverage html
```
